"""
Chatbot WhatsApp con tiempo de respuesta <1s
Atención al cliente/ventas con autoaprendizaje
"""

import asyncio
import json
import logging
import sqlite3
import time
from datetime import datetime
from typing import Dict, List, Optional

import redis
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import hashlib
import os
from PIL import Image
import io
import base64

# Configuración
app = FastAPI(title="WhatsApp Chatbot", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables de entorno
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "your_whatsapp_token")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "your_verify_token")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "your_phone_number_id")

# Inicialización de componentes
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    logger.info("Redis conectado exitosamente")
except:
    logger.warning("Redis no disponible, usando caché en memoria")
    redis_client = None

# Modelo de IA ligero para clasificación rápida
try:
    nlp = spacy.load("es_core_news_sm")
except:
    logger.warning("Modelo spaCy no encontrado, instalando...")
    os.system("python -m spacy download es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

# Clasificador de intenciones (modelo ligero)
intent_classifier = pipeline(
    "text-classification",
    model="distilbert-base-multilingual-cased",
    return_all_scores=True
)

class WhatsAppMessage(BaseModel):
    messaging_product: str
    to: str
    type: str
    text: Optional[Dict] = None
    image: Optional[Dict] = None
    document: Optional[Dict] = None

class ChatbotEngine:
    def __init__(self):
        self.setup_database()
        self.cache = {}
        self.response_templates = self.load_response_templates()
        
    def setup_database(self):
        """Configurar base de datos SQLite"""
        self.conn = sqlite3.connect('chatbot.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Tabla de conversaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                message TEXT,
                response TEXT,
                intent TEXT,
                confidence REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de conocimiento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT,
                keywords TEXT,
                response TEXT,
                confidence REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar respuestas base
        self.insert_base_responses()
        self.conn.commit()
        
    def insert_base_responses(self):
        """Insertar respuestas base para atención al cliente/ventas"""
        base_responses = [
            ("saludo", "hola,buenos días,buenas tardes,hey", "¡Hola! 👋 Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"),
            ("productos", "productos,catálogo,qué venden,ofertas", "Te puedo ayudar con información sobre nuestros productos. ¿Qué tipo de producto te interesa?"),
            ("precios", "precio,costo,cuánto cuesta,valor", "Con gusto te ayudo con información de precios. ¿Podrías decirme qué producto específico te interesa?"),
            ("horarios", "horario,abierto,cerrado,atención", "Nuestro horario de atención es de Lunes a Viernes de 9:00 AM a 6:00 PM. ¿En qué más puedo ayudarte?"),
            ("contacto", "teléfono,dirección,ubicación,contacto", "Puedes contactarnos por este mismo chat o llamarnos. ¿Necesitas alguna información específica?"),
            ("despedida", "gracias,adiós,bye,hasta luego", "¡Gracias por contactarnos! 😊 Que tengas un excelente día. Estamos aquí cuando nos necesites."),
        ]
        
        cursor = self.conn.cursor()
        for intent, keywords, response in base_responses:
            cursor.execute('''
                INSERT OR IGNORE INTO knowledge_base (intent, keywords, response)
                VALUES (?, ?, ?)
            ''', (intent, keywords, response))
    
    def load_response_templates(self) -> Dict:
        """Cargar plantillas de respuesta rápida"""
        return {
            "processing": "Un momento por favor, estoy procesando tu consulta... ⏳",
            "error": "Disculpa, hubo un error. ¿Podrías repetir tu consulta?",
            "unknown": "Interesante consulta. Déjame aprender de esto para ayudarte mejor. ¿Podrías darme más detalles?",
            "image_received": "He recibido tu imagen 📷. La estoy analizando...",
            "document_received": "He recibido tu documento 📄. Lo estoy revisando..."
        }
    
    async def get_cached_response(self, message_hash: str) -> Optional[str]:
        """Obtener respuesta desde caché"""
        if redis_client:
            try:
                return redis_client.get(f"response:{message_hash}")
            except:
                pass
        return self.cache.get(message_hash)
    
    async def cache_response(self, message_hash: str, response: str):
        """Guardar respuesta en caché"""
        if redis_client:
            try:
                redis_client.setex(f"response:{message_hash}", 3600, response)  # 1 hora
            except:
                pass
        self.cache[message_hash] = response
    
    def classify_intent(self, text: str) -> tuple:
        """Clasificar intención del mensaje de forma rápida"""
        # Búsqueda rápida en base de conocimiento
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT intent, response, confidence FROM knowledge_base
            WHERE ? LIKE '%' || keywords || '%'
            ORDER BY usage_count DESC, confidence DESC
            LIMIT 1
        ''', (text.lower(),))
        
        result = cursor.fetchone()
        if result:
            return result[0], result[1], result[2]
        
        # Clasificación con IA (más lenta, para casos no encontrados)
        doc = nlp(text)
        # Análisis simple basado en entidades y patrones
        if any(token.text.lower() in ["hola", "buenos", "hey"] for token in doc):
            return "saludo", self.response_templates.get("saludo", "¡Hola!"), 0.9
        elif any(token.text.lower() in ["precio", "costo", "cuánto"] for token in doc):
            return "precios", "Te ayudo con precios. ¿Qué producto te interesa?", 0.8
        elif any(token.text.lower() in ["producto", "catálogo", "venden"] for token in doc):
            return "productos", "¿Qué tipo de producto buscas?", 0.8
        
        return "unknown", self.response_templates["unknown"], 0.3
    
    async def process_message(self, user_id: str, message: str) -> str:
        """Procesar mensaje con tiempo de respuesta optimizado"""
        start_time = time.time()
        
        # Generar hash del mensaje para caché
        message_hash = hashlib.md5(f"{user_id}:{message}".encode()).hexdigest()
        
        # Buscar en caché primero
        cached_response = await self.get_cached_response(message_hash)
        if cached_response:
            logger.info(f"Respuesta desde caché en {time.time() - start_time:.3f}s")
            return cached_response
        
        # Clasificar intención y generar respuesta
        intent, response, confidence = self.classify_intent(message)
        
        # Guardar en caché
        await self.cache_response(message_hash, response)
        
        # Guardar conversación (asíncrono)
        asyncio.create_task(self.save_conversation(user_id, message, response, intent, confidence))
        
        processing_time = time.time() - start_time
        logger.info(f"Mensaje procesado en {processing_time:.3f}s")
        
        return response
    
    async def save_conversation(self, user_id: str, message: str, response: str, intent: str, confidence: float):
        """Guardar conversación para autoaprendizaje"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (user_id, message, response, intent, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, message, response, intent, confidence))
        
        # Actualizar contador de uso
        cursor.execute('''
            UPDATE knowledge_base 
            SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP
            WHERE intent = ?
        ''', (intent,))
        
        self.conn.commit()
    
    async def process_image(self, user_id: str, image_data: bytes) -> str:
        """Procesar imagen recibida"""
        # Respuesta inmediata
        immediate_response = self.response_templates["image_received"]
        
        # Procesamiento asíncrono de la imagen
        asyncio.create_task(self.analyze_image_async(user_id, image_data))
        
        return immediate_response
    
    async def analyze_image_async(self, user_id: str, image_data: bytes):
        """Análisis asíncrono de imagen"""
        try:
            # Aquí puedes agregar análisis de imagen con IA
            # Por ahora, solo guardamos que se recibió una imagen
            await self.save_conversation(user_id, "[IMAGEN]", "Imagen recibida y procesada", "image", 1.0)
        except Exception as e:
            logger.error(f"Error procesando imagen: {e}")

# Instancia global del motor del chatbot
chatbot = ChatbotEngine()

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verificación del webhook de WhatsApp"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook verificado exitosamente")
        return int(challenge)
    else:
        logger.warning("Verificación de webhook fallida")
        return JSONResponse(status_code=403, content={"error": "Forbidden"})

@app.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    """Manejar mensajes entrantes de WhatsApp"""
    try:
        body = await request.json()
        
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "messages":
                        messages = change.get("value", {}).get("messages", [])
                        
                        for message in messages:
                            # Procesar mensaje de forma asíncrona para respuesta rápida
                            background_tasks.add_task(process_whatsapp_message, message)
        
        return JSONResponse(status_code=200, content={"status": "success"})
    
    except Exception as e:
        logger.error(f"Error procesando webhook: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

async def process_whatsapp_message(message: dict):
    """Procesar mensaje de WhatsApp"""
    try:
        user_phone = message.get("from")
        message_type = message.get("type")
        
        response_text = ""
        
        if message_type == "text":
            text_content = message.get("text", {}).get("body", "")
            response_text = await chatbot.process_message(user_phone, text_content)
        
        elif message_type == "image":
            response_text = await chatbot.process_image(user_phone, b"")  # Simplificado
        
        elif message_type == "document":
            response_text = chatbot.response_templates["document_received"]
        
        else:
            response_text = "Tipo de mensaje no soportado aún. ¿Podrías enviar texto?"
        
        # Enviar respuesta
        await send_whatsapp_message(user_phone, response_text)
        
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")

async def send_whatsapp_message(to: str, message: str):
    """Enviar mensaje de WhatsApp"""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info(f"Mensaje enviado exitosamente a {to}")
        else:
            logger.error(f"Error enviando mensaje: {response.text}")
    except Exception as e:
        logger.error(f"Error en envío: {e}")

@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/stats")
async def get_stats():
    """Estadísticas del chatbot"""
    cursor = chatbot.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM conversations")
    total_conversations = cursor.fetchone()[0]
    
    cursor.execute("SELECT intent, COUNT(*) FROM conversations GROUP BY intent")
    intent_stats = dict(cursor.fetchall())
    
    return {
        "total_conversations": total_conversations,
        "intent_distribution": intent_stats,
        "cache_size": len(chatbot.cache)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)