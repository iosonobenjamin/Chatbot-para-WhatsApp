#!/bin/bash

# Script para ejecutar el Chatbot WhatsApp
# Optimizado para tiempo de respuesta <1s

echo "🚀 Iniciando Chatbot WhatsApp..."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta primero: ./install_and_run.sh"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar archivo .env
if [ ! -f .env ]; then
    echo "❌ Archivo .env no encontrado. Ejecuta primero: ./install_and_run.sh"
    exit 1
fi

# Cargar variables de entorno
export $(cat .env | grep -v '^#' | xargs)

# Verificar credenciales críticas
if [ -z "$WHATSAPP_TOKEN" ] || [ "$WHATSAPP_TOKEN" = "tu_token_aqui" ]; then
    echo "❌ WHATSAPP_TOKEN no configurado en .env"
    echo "   Consulta setup_whatsapp.md para obtener el token"
    exit 1
fi

if [ -z "$PHONE_NUMBER_ID" ] || [ "$PHONE_NUMBER_ID" = "tu_phone_number_id_aqui" ]; then
    echo "❌ PHONE_NUMBER_ID no configurado en .env"
    echo "   Consulta setup_whatsapp.md para obtener el Phone Number ID"
    exit 1
fi

# Verificar Redis (opcional)
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis conectado"
    else
        echo "⚠️ Redis no responde. Iniciando servidor..."
        redis-server --daemonize yes
        sleep 2
    fi
else
    echo "⚠️ Redis no disponible. Usando caché en memoria."
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Función para manejar señales de interrupción
cleanup() {
    echo ""
    echo "🛑 Deteniendo chatbot..."
    kill $SERVER_PID 2>/dev/null
    exit 0
}

# Configurar trap para limpieza
trap cleanup SIGINT SIGTERM

# Mostrar información de inicio
echo "📊 Configuración:"
echo "   Puerto: ${PORT:-8000}"
echo "   Host: ${HOST:-0.0.0.0}"
echo "   Debug: ${DEBUG:-False}"
echo "   Log Level: ${LOG_LEVEL:-INFO}"
echo ""

# Verificar que el puerto esté disponible
if lsof -Pi :${PORT:-8000} -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Puerto ${PORT:-8000} ya está en uso"
    echo "   Cambia el puerto en .env o detén el proceso que lo usa"
    exit 1
fi

# Ejecutar el chatbot
echo "🤖 Chatbot iniciado en http://${HOST:-0.0.0.0}:${PORT:-8000}"
echo "📡 Webhook URL: http://tu-dominio.com/webhook"
echo "🔍 Health check: http://${HOST:-0.0.0.0}:${PORT:-8000}/health"
echo "📈 Estadísticas: http://${HOST:-0.0.0.0}:${PORT:-8000}/stats"
echo ""
echo "💡 Presiona Ctrl+C para detener el servidor"
echo "📖 Consulta setup_whatsapp.md para configurar el webhook"
echo ""

# Iniciar servidor con logging
python main.py 2>&1 | tee logs/chatbot_$(date +%Y%m%d_%H%M%S).log &
SERVER_PID=$!

# Esperar a que el servidor termine
wait $SERVER_PID