"""
Configuración del Chatbot WhatsApp
Optimizado para tiempo de respuesta <1s
"""

import os
from typing import Dict, Any

class Config:
    """Configuración centralizada del chatbot"""
    
    # WhatsApp Business API
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "whatsapp_verify_token_2024")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "")
    WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"
    
    # Base de datos
    DATABASE_URL = os.getenv("DATABASE_URL", "chatbot.db")
    
    # Redis (caché)
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    
    # Configuración de rendimiento
    CACHE_TTL = 3600  # 1 hora
    MAX_RESPONSE_TIME = 0.8  # 800ms objetivo
    MAX_CACHE_SIZE = 1000
    
    # Configuración de IA
    NLP_MODEL = "es_core_news_sm"
    INTENT_MODEL = "distilbert-base-multilingual-cased"
    CONFIDENCE_THRESHOLD = 0.7
    
    # Límites de procesamiento
    MAX_MESSAGE_LENGTH = 1000
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Respuestas por defecto
    DEFAULT_RESPONSES: Dict[str, str] = {
        "welcome": "¡Hola! 👋 Soy tu asistente virtual. ¿En qué puedo ayudarte?",
        "processing": "Un momento por favor... ⏳",
        "error": "Disculpa, hubo un error. ¿Podrías repetir tu consulta?",
        "unknown": "Interesante. Déjame aprender de esto. ¿Podrías darme más detalles?",
        "image_received": "📷 Imagen recibida. Analizando...",
        "document_received": "📄 Documento recibido. Procesando...",
        "goodbye": "¡Gracias por contactarnos! 😊 Que tengas un excelente día.",
        "timeout": "La consulta está tomando más tiempo del esperado. Te responderé pronto.",
    }
    
    # Configuración de logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración del servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validar configuración requerida"""
        required_vars = ["WHATSAPP_TOKEN", "PHONE_NUMBER_ID"]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
            return False
        
        print("✅ Configuración validada correctamente")
        return True

# Configuración de intenciones y respuestas
INTENT_PATTERNS = {
    "saludo": {
        "keywords": ["hola", "buenos días", "buenas tardes", "buenas noches", "hey", "hi", "saludos"],
        "responses": [
            "¡Hola! 👋 ¿En qué puedo ayudarte hoy?",
            "¡Buenos días! Soy tu asistente virtual. ¿Cómo te puedo ayudar?",
            "¡Hola! Estoy aquí para ayudarte. ¿Qué necesitas?"
        ]
    },
    "productos": {
        "keywords": ["producto", "catálogo", "qué venden", "ofertas", "disponible", "stock"],
        "responses": [
            "Te puedo ayudar con información sobre nuestros productos. ¿Qué tipo de producto te interesa?",
            "Tenemos varios productos disponibles. ¿Podrías ser más específico sobre lo que buscas?",
            "¡Perfecto! ¿Qué producto en particular te gustaría conocer?"
        ]
    },
    "precios": {
        "keywords": ["precio", "costo", "cuánto cuesta", "valor", "tarifa", "cotización"],
        "responses": [
            "Con gusto te ayudo con información de precios. ¿Qué producto específico te interesa?",
            "Para darte el precio exacto, ¿podrías decirme qué producto necesitas?",
            "Los precios varían según el producto. ¿Cuál te interesa en particular?"
        ]
    },
    "horarios": {
        "keywords": ["horario", "abierto", "cerrado", "atención", "cuando", "hora"],
        "responses": [
            "Nuestro horario de atención es de Lunes a Viernes de 9:00 AM a 6:00 PM. ¿En qué más puedo ayudarte?",
            "Estamos disponibles de Lunes a Viernes, 9:00 AM a 6:00 PM. ¿Necesitas algo más?",
            "Horario: L-V 9:00 AM - 6:00 PM. ¿Hay algo específico en lo que pueda ayudarte?"
        ]
    },
    "contacto": {
        "keywords": ["teléfono", "dirección", "ubicación", "contacto", "dónde", "llamar"],
        "responses": [
            "Puedes contactarnos por este mismo chat o llamarnos. ¿Necesitas alguna información específica?",
            "Estoy aquí para ayudarte por WhatsApp. ¿Qué información de contacto necesitas?",
            "Por este medio puedo resolver tus dudas. ¿En qué te puedo ayudar?"
        ]
    },
    "despedida": {
        "keywords": ["gracias", "adiós", "bye", "hasta luego", "nos vemos", "chao"],
        "responses": [
            "¡Gracias por contactarnos! 😊 Que tengas un excelente día.",
            "¡Hasta luego! Estamos aquí cuando nos necesites. 👋",
            "¡Que tengas un gran día! No dudes en escribirnos si necesitas algo más."
        ]
    },
    "ayuda": {
        "keywords": ["ayuda", "help", "no entiendo", "cómo", "qué puedes hacer"],
        "responses": [
            "Puedo ayudarte con información sobre productos, precios, horarios y más. ¿Qué necesitas saber?",
            "Estoy aquí para asistirte con tus consultas. ¿En qué área necesitas ayuda?",
            "Te puedo ayudar con consultas sobre nuestros servicios. ¿Qué te gustaría saber?"
        ]
    }
}

# Configuración de autoaprendizaje
LEARNING_CONFIG = {
    "min_confidence": 0.6,
    "learning_rate": 0.1,
    "max_learning_samples": 1000,
    "retrain_threshold": 50,  # Nuevas conversaciones antes de reentrenar
    "feedback_weight": 1.5,   # Peso de feedback positivo del usuario
}