
# Configuración de WhatsApp Business API - Guía Completa

## 1. Crear Cuenta de WhatsApp Business

### Paso 1: Registrarse en Meta for Developers
1. Ve a [developers.facebook.com](https://developers.facebook.com)
2. Crea una cuenta o inicia sesión con tu cuenta de Facebook
3. Acepta los términos de desarrollador

### Paso 2: Crear una App
1. Haz clic en "Mis Apps" → "Crear App"
2. Selecciona "Empresa" como tipo de app
3. Completa la información:
   - **Nombre de la app**: "Mi Chatbot WhatsApp"
   - **Email de contacto**: tu email
   - **Propósito**: "Atención al cliente"

### Paso 3: Configurar WhatsApp Business API
1. En el dashboard de tu app, busca "WhatsApp"
2. Haz clic en "Configurar" en WhatsApp Business API
3. Selecciona o crea una cuenta comercial de Meta

## 2. Configuración Inicial (GRATUITA)

### Obtener Credenciales
1. **Token de Acceso Temporal** (24 horas):
   - Ve a "API Setup" en tu app de WhatsApp
   - Copia el token temporal que aparece
   - **IMPORTANTE**: Este token expira en 24 horas

2. **Phone Number ID**:
   - En la misma página, encontrarás "From phone number ID"
   - Copia este ID (será algo como: 123456789012345)

3. **Webhook Verify Token**:
   - Puedes usar cualquier string, por ejemplo: "whatsapp_verify_token_2024"

### Configurar Variables de Entorno
Crea un archivo `.env` con:

```bash
# WhatsApp Business API
WHATSAPP_TOKEN=tu_token_temporal_aqui
PHONE_NUMBER_ID=tu_phone_number_id_aqui
VERIFY_TOKEN=whatsapp_verify_token_2024

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Redis (opcional, para mejor rendimiento)
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 3. Configurar Webhook

### Opción A: Usando ngrok (Para desarrollo local)

1. **Instalar ngrok**:
   ```bash
   # Windows
   choco install ngrok
   
   # macOS
   brew install ngrok
   
   # Linux
   wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
   unzip ngrok-stable-linux-amd64.zip
   ```

2. **Ejecutar el chatbot**:
   ```bash
   python main.py
   ```

3. **Exponer con ngrok** (en otra terminal):
   ```bash
   ngrok http 8000
   ```

4. **Configurar webhook en Meta**:
   - Copia la URL de ngrok (ej: `https://abc123.ngrok.io`)
   - Ve a tu app de WhatsApp → "Configuration"
   - En "Webhook", pega: `https://abc123.ngrok.io/webhook`
   - Verify token: `whatsapp_verify_token_2024`
   - Haz clic en "Verify and save"

### Opción B: Usando Railway (Hosting gratuito)

1. **Crear cuenta en Railway**:
   - Ve a [railway.app](https://railway.app)
   - Regístrate con GitHub

2. **Desplegar el proyecto**:
   ```bash
   # Instalar Railway CLI
   npm install -g @railway/cli
   
   # Login
   railway login
   
   # Inicializar proyecto
   railway init
   
   # Desplegar
   railway up
   ```

3. **Configurar variables de entorno en Railway**:
   - Ve a tu proyecto en Railway
   - Pestaña "Variables"
   - Agrega todas las variables del archivo `.env`

4. **Configurar webhook**:
   - Usa la URL de Railway: `https://tu-proyecto.railway.app/webhook`

## 4. Verificación y Pruebas

### Verificar Configuración
1. **Test del webhook**:
   ```bash
   curl -X GET "https://tu-url.com/webhook?hub.mode=subscribe&hub.verify_token=whatsapp_verify_token_2024&hub.challenge=123"
   ```

2. **Test de salud**:
   ```bash
   curl https://tu-url.com/health
   ```

### Probar el Bot
1. **Número de prueba**:
   - Meta te proporciona un número de WhatsApp de prueba
   - Agrega este número a tus contactos
   - Envía un mensaje de prueba

2. **Mensajes de prueba**:
   - "Hola" → Debería responder con saludo
   - "Precios" → Debería preguntar por producto específico
   - "Gracias" → Debería despedirse

## 5. Obtener Token Permanente (Para producción)

### Verificación de Negocio
1. **Verificar tu negocio**:
   - Ve a "Business Settings" en Meta Business
   - Completa la verificación comercial
   - Proporciona documentos legales de tu empresa

2. **Generar token permanente**:
   - Una vez verificado, puedes generar tokens que no expiran
   - Ve a "System Users" → "Add" → "System User"
   - Asigna permisos de WhatsApp Business Management

### Configuración de Producción
```bash
# Token permanente
WHATSAPP_TOKEN=tu_token_permanente_aqui

# Webhook URL de producción
WEBHOOK_URL=https://tu-dominio.com/webhook
```

## 6. Límites Gratuitos

### Tier Gratuito de WhatsApp Business API
- **1,000 conversaciones gratis por mes**
- **Conversación** = intercambio de mensajes en 24 horas
- **Después de 1,000**: $0.005 - $0.009 USD por conversación

### Optimización de Costos
- **Respuestas rápidas**: Evita múltiples mensajes
- **Sesiones eficientes**: Resuelve consultas en una conversación
- **Caché inteligente**: Reduce procesamiento repetitivo

## 7. Monitoreo y Mantenimiento

### Logs y Métricas
```bash
# Ver logs en tiempo real
tail -f chatbot.log

# Estadísticas del bot
curl https://tu-url.com/stats
```

### Backup de Base de Datos
```bash
# Backup automático diario
sqlite3 chatbot.db ".backup backup_$(date +%Y%m%d).db"
```

## 8. Solución de Problemas Comunes

### Error: "Token inválido"
- Verifica que el token no haya expirado
- Regenera el token en Meta for Developers

### Error: "Webhook no verificado"
- Verifica que la URL sea accesible públicamente
- Confirma que el verify_token coincida

### Error: "Mensajes no llegan"
- Verifica que el webhook esté configurado correctamente
- Revisa los logs del servidor
- Confirma que el número esté en la lista de prueba

### Rendimiento lento
- Verifica la conexión a Redis
- Optimiza las consultas a la base de datos
- Considera usar un servidor más potente

## 9. Próximos Pasos

1. **Personalizar respuestas** según tu negocio
2. **Agregar más intenciones** al clasificador
3. **Implementar análisis de sentimientos**
4. **Integrar con CRM** o base de datos de productos
5. **Configurar notificaciones** para el equipo de ventas

¡Tu chatbot está listo para funcionar con tiempo de respuesta menor a 1 segundo! 🚀
