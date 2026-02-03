#!/bin/bash

# Script de instalación y ejecución del Chatbot WhatsApp
# Optimizado para tiempo de respuesta <1s

echo "🚀 Instalando Chatbot WhatsApp..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Descargar modelos de spaCy
echo "🧠 Descargando modelos de IA..."
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm

# Verificar instalación de Redis (opcional)
echo "🔍 Verificando Redis..."
if command -v redis-server &> /dev/null; then
    echo "✅ Redis encontrado. Iniciando servidor..."
    redis-server --daemonize yes
else
    echo "⚠️ Redis no encontrado. El bot funcionará con caché en memoria."
    echo "Para mejor rendimiento, instala Redis:"
    echo "  Ubuntu/Debian: sudo apt-get install redis-server"
    echo "  macOS: brew install redis"
    echo "  Windows: https://redis.io/download"
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo de configuración..."
    cat > .env << EOL
# WhatsApp Business API - CONFIGURA ESTOS VALORES
WHATSAPP_TOKEN=tu_token_aqui
PHONE_NUMBER_ID=tu_phone_number_id_aqui
VERIFY_TOKEN=whatsapp_verify_token_2024

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379

# Logging
LOG_LEVEL=INFO
EOL
    echo "⚠️ IMPORTANTE: Edita el archivo .env con tus credenciales de WhatsApp"
    echo "   Consulta setup_whatsapp.md para obtener las credenciales"
fi

# Crear directorio de logs
mkdir -p logs

# Verificar configuración
echo "🔧 Verificando configuración..."
python -c "from config import Config; Config.validate_config()" || {
    echo "❌ Error en la configuración. Revisa el archivo .env"
    exit 1
}

echo "✅ Instalación completada!"
echo ""
echo "🚀 Para ejecutar el chatbot:"
echo "   1. Edita el archivo .env con tus credenciales de WhatsApp"
echo "   2. Ejecuta: ./run.sh"
echo ""
echo "📖 Consulta setup_whatsapp.md para configurar WhatsApp Business API"