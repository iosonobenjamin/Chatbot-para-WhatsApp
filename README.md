# 🤖 Chatbot WhatsApp - Tiempo de Respuesta <1s
 
Un chatbot inteligente para WhatsApp Business API optimizado para **atención al cliente y ventas** con **autoaprendizaje en tiempo real** y **procesamiento multimedia**.
 
## ✨ Características Principales
 
- ⚡ **Tiempo de respuesta garantizado <1 segundo**
- 🧠 **Autoaprendizaje en tiempo real** de conversaciones
- 📱 **Procesamiento multimedia** (texto, imágenes, documentos)
- 💰 **Solución gratuita** usando servicios free tier
- 🚀 **Fácil instalación y configuración**
- 📊 **Monitoreo de rendimiento en tiempo real**
- 🔄 **Caché inteligente** con Redis
- 🎯 **Optimizado para 30 mensajes/hora**
 
## 🏗️ Arquitectura del Sistema
 
```
Usuario WhatsApp → Webhook → FastAPI → Procesador → Caché Redis → Respuesta <1s
                                    ↓
                              Base de Conocimiento (SQLite)
                                    ↓
                              Autoaprendizaje Asíncrono
```
 
### Componentes Clave:
- **Backend**: Python + FastAPI (ultra rápido)
- **IA**: spaCy + Transformers (modelos ligeros)
- **Base de datos**: SQLite (local) + Redis (caché)
- **API**: WhatsApp Business API (1000 mensajes gratis/mes)
 
## 🚀 Instalación Rápida
 
### 1. Clonar y Configurar
```bash
# Clonar el proyecto
git clone <tu-repositorio>
cd chatbot-whatsapp
 
# Ejecutar instalación automática
./install_and_run.sh
```
 
### 2. Configurar WhatsApp Business API
```bash
# Editar credenciales en .env
nano .env
 
# Configurar:
WHATSAPP_TOKEN=tu_token_aqui
PHONE_NUMBER_ID=tu_phone_number_id_aqui
```
 
📖 **Guía completa**: Ver `setup_whatsapp.md` para obtener credenciales
 
### 3. Ejecutar el Bot
```bash
./run.sh
```
 
¡Listo! Tu chatbot estará funcionando en segundos.
 
## 📋 Requisitos del Sistema
 
- **Python 3.8+**
- **4GB RAM mínimo** (recomendado 8GB)
- **Redis** (opcional, mejora rendimiento)
- **Conexión a internet estable**
 
### Dependencias Principales:
- FastAPI (framework web)
- spaCy (procesamiento de lenguaje)
- Transformers (IA ligera)
- Redis (caché en memoria)
- SQLite (base de datos)
 
## 🎯 Funcionalidades
 
### Atención al Cliente
- ✅ Respuestas automáticas a consultas frecuentes
- ✅ Clasificación inteligente de intenciones
- ✅ Escalamiento a humanos cuando es necesario
- ✅ Historial de conversaciones
 
### Ventas
- ✅ Información de productos y precios
- ✅ Recomendaciones personalizadas
- ✅ Seguimiento de leads
- ✅ Integración con CRM (configurable)
 
### Autoaprendizaje
- ✅ Mejora automática con cada conversación
- ✅ Detección de nuevos patrones
- ✅ Actualización de respuestas en tiempo real
- ✅ Análisis de sentimientos
 
### Multimedia
- ✅ Procesamiento de imágenes
- ✅ Análisis de documentos
- ✅ Respuestas con multimedia
- ✅ Compresión automática
 
## 📊 Monitoreo y Métricas
 
### Dashboard en Tiempo Real
```bash
# Ver estadísticas
curl http://localhost:8000/stats
 
# Health check
curl http://localhost:8000/health
```
 
### Métricas Disponibles:
- Tiempo de respuesta promedio
- Tasa de aciertos en caché
- Consultas lentas
- Distribución de intenciones
- Errores y excepciones
 
## ⚡ Optimizaciones de Rendimiento
 
### Caché Inteligente
- Respuestas frecuentes pre-computadas
- Caché distribuido con Redis
- Invalidación automática
- Precalentamiento inteligente
 
### Base de Datos Optimizada
- Índices automáticos
- Limpieza de datos antiguos
- Consultas optimizadas
- Backup automático
 
### Procesamiento Asíncrono
- Respuesta inmediata al usuario
- Procesamiento pesado en background
- Cola de tareas inteligente
- Manejo de errores robusto
 
## 🔧 Configuración Avanzada
 
### Variables de Entorno (.env)
```bash
# WhatsApp Business API
WHATSAPP_TOKEN=tu_token_aqui
PHONE_NUMBER_ID=tu_phone_number_id_aqui
VERIFY_TOKEN=whatsapp_verify_token_2024
 
# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=False
 
# Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379
 
# Rendimiento
MAX_RESPONSE_TIME=0.8
CACHE_TTL=3600
```
 
### Personalización de Respuestas
Edita `config.py` para personalizar:
- Intenciones y patrones
- Respuestas automáticas
- Configuración de aprendizaje
- Límites de procesamiento
 
## 🚀 Despliegue en Producción
 
### Opción 1: Railway (Recomendado)
```bash
# Instalar Railway CLI
npm install -g @railway/cli
 
# Desplegar
railway login
railway init
railway up
```
 
### Opción 2: Heroku
```bash
# Crear app
heroku create mi-chatbot-whatsapp
 
# Configurar variables
heroku config:set WHATSAPP_TOKEN=tu_token
 
# Desplegar
git push heroku main
```
 
### Opción 3: VPS Propio
```bash
# Usar Docker
docker build -t chatbot-whatsapp .
docker run -p 8000:8000 chatbot-whatsapp
```
 
## 📈 Escalabilidad
 
### Para Mayor Volumen (>100 mensajes/hora):
1. **Usar PostgreSQL** en lugar de SQLite
2. **Cluster de Redis** para caché distribuido
3. **Load balancer** con múltiples instancias
4. **CDN** para contenido multimedia
5. **Monitoreo avanzado** con Prometheus
 
### Costos Estimados:
- **0-1000 mensajes/mes**: Gratis
- **1000-10000 mensajes/mes**: $5-50 USD
- **10000+ mensajes/mes**: $50+ USD
 
## 🛠️ Solución de Problemas
 
### Problemas Comunes:
 
**❌ "Token inválido"**
```bash
# Verificar token en .env
echo $WHATSAPP_TOKEN
# Regenerar en Meta for Developers
```
 
**❌ "Webhook no verificado"**
```bash
# Verificar URL pública
curl https://tu-url.com/webhook
# Confirmar verify_token
```
 
**❌ "Respuestas lentas"**
```bash
# Verificar Redis
redis-cli ping
# Ver métricas
curl http://localhost:8000/stats
```
 
### Logs y Debugging:
```bash
# Ver logs en tiempo real
tail -f logs/chatbot_*.log
 
# Modo debug
DEBUG=True python main.py
```
 
## 🤝 Contribuir
 
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request
 
## 📄 Licencia
 
MIT License - Ver `LICENSE` para más detalles.
 
## 🆘 Soporte
 
- 📖 **Documentación**: Ver archivos `.md` en el proyecto
- 🐛 **Issues**: Reportar en GitHub Issues
- 💬 **Comunidad**: Únete a nuestro Discord
- 📧 **Email**: soporte@tu-empresa.com
 
## 🎉 ¡Listo para Usar!
 
Tu chatbot de WhatsApp está optimizado para:
- ⚡ Respuestas en menos de 1 segundo
- 🧠 Aprendizaje automático continuo
- 📱 Procesamiento multimedia completo
- 💰 Costos mínimos con máximo rendimiento
 
**¡Comienza ahora y transforma tu atención al cliente!** 🚀
 
---
 
*Desarrollado con ❤️ para empresas que valoran la velocidad y la inteligencia artificial.*
