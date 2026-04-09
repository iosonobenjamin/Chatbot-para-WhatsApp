# 📋 Guía Completa de Instalación - Chatbot WhatsApp

**Autor:** Chatbot WhatsApp Team  
**Versión:** 1.0.0  
**Última actualización:** Abril 2026  

---

## 📑 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación Local (Desarrollo)](#instalación-local-desarrollo)
3. [Instalación en Servidores](#instalación-en-servidores)
4. [Recomendaciones de Servidores](#recomendaciones-de-servidores)
5. [Configuración WhatsApp Business API](#configuración-whatsapp-business-api)
6. [Verificación y Pruebas](#verificación-y-pruebas)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Requisitos Previos

### Hardware Mínimo Recomendado
- **CPU**: 1 vCore (2+ vCore recomendado)
- **RAM**: 512 MB (1-2 GB recomendado)
- **Disco**: 1 GB disponible
- **Conexión**: Estable (1 Mbps upload/download)

### Software Necesario
- **Python 3.10+** (3.11 recomendado)
- **pip** (gestor de paquetes Python)
- **Redis** (opcional pero recomendado para caché)
- **Git** (para clonar el repositorio)

---

## 🖥️ Instalación Local (Desarrollo)

### Opción 1: Windows (PowerShell)

#### Paso 1: Verificar Python
```powershell
# Abrir PowerShell como Administrador
python --version
pip --version
```

Si no está instalado, descargarlo desde https://www.python.org/

#### Paso 2: Clonar el Repositorio
```powershell
# Navegar a la carpeta deseada
cd "C:\Users\YourUsername\Documents"

# Clonar el proyecto
git clone https://github.com/tu-usuario/chatbot-whatsapp.git
cd chatbot-whatsapp
```

#### Paso 3: Crear Entorno Virtual
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si aparece error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Paso 4: Instalar Dependencias
```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar requirements
pip install -r requirements.txt

# Instalar modelo de NLP (~ 50MB, primera vez)
python -m spacy download es_core_news_sm
```

#### Paso 5: Configurar Variables de Entorno
```powershell
# Crear archivo .env
New-Item -Path ".env" -Type File

# Editar con tu editor favorito (Notepad++, VS Code, etc.)
```

Contenido del archivo `.env`:
```
WHATSAPP_TOKEN=tu_token_de_whatsapp
VERIFY_TOKEN=tu_verify_token
PHONE_NUMBER_ID=tu_numero_de_telefono_id
REDIS_HOST=localhost
REDIS_PORT=6379
```

#### Paso 6: Ejecutar el Servidor
```powershell
# Opción A: Ejecución directa
python main.py

# Opción B: Con uvicorn (recomendado)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Salida esperada:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

### Opción 2: Linux/Ubuntu (Bash)

#### Paso 1: Actualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```

#### Paso 2: Clonar y Configurar
```bash
cd ~
git clone https://github.com/tu-usuario/chatbot-whatsapp.git
cd chatbot-whatsapp

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
```

#### Paso 3: Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

#### Paso 4: Crear Archivo .env
```bash
cat > .env << EOF
WHATSAPP_TOKEN=tu_token_de_whatsapp
VERIFY_TOKEN=tu_verify_token
PHONE_NUMBER_ID=tu_numero_de_telefono_id
REDIS_HOST=localhost
REDIS_PORT=6379
EOF
```

#### Paso 5: Ejecutar
```bash
# Opción A: Ejecución simple
python main.py

# Opción B: Con uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Opción C: En background con nohup
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > chatbot.log 2>&1 &
```

---

### Opción 3: Instalación Rápida con Script

#### Windows (Si existe `install_and_run.sh`):
```powershell
# Convertir a ejecutable o ejecutar manualmente:
.\install_and_run.sh
```

#### Linux:
```bash
chmod +x install_and_run.sh
./install_and_run.sh
```

---

## ☁️ Instalación en Servidores

### Opción 1: Servidor VPS (Recomendado para Producción)

#### Paso 1: Crear Droplet en DigitalOcean / Linode / AWS
- **OS**: Ubuntu 22.04 LTS
- **RAM**: 2GB mínimo
- **CPU**: 2 vCore
- **Disco**: 20GB SSD

#### Paso 2: Acceder al Servidor
```bash
ssh root@tu_ip_servidor

# Primera vez: actualizar
apt update && apt upgrade -y
```

#### Paso 3: Instalar Dependencias Base
```bash
apt install python3-pip python3-venv git redis-server nginx -y

# Iniciar Redis
systemctl start redis-server
systemctl enable redis-server

# Verificar Redis
redis-cli ping
```

#### Paso 4: Desplegar Aplicación
```bash
cd /var/www
git clone https://github.com/tu-usuario/chatbot-whatsapp.git
cd chatbot-whatsapp

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

#### Paso 5: Crear Archivo de Servicio
```bash
sudo cat > /etc/systemd/system/chatbot.service << 'EOF'
[Unit]
Description=WhatsApp Chatbot
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/chatbot-whatsapp
Environment="PATH=/var/www/chatbot-whatsapp/venv/bin"
ExecStart=/var/www/chatbot-whatsapp/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Activar servicio
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot
sudo systemctl status chatbot
```

#### Paso 6: Configurar Nginx como Proxy Inverso
```bash
sudo cat > /etc/nginx/sites-available/chatbot << 'EOF'
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Paso 7: SSL con Let's Encrypt (Gratuito)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

---

### Opción 2: Docker (Contenedores)

#### Crear Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download es_core_news_sm

# Copiar aplicación
COPY . .

# Expoñer puerto
EXPOSE 8000

# Ejecutar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Crear docker-compose.yml
```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "8000:8000"
    environment:
      - WHATSAPP_TOKEN=${WHATSAPP_TOKEN}
      - VERIFY_TOKEN=${VERIFY_TOKEN}
      - PHONE_NUMBER_ID=${PHONE_NUMBER_ID}
      - REDIS_HOST=redis
    depends_on:
      - redis
    restart: always

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: always

volumes:
  redis_data:
```

#### Desplegar con Docker
```bash
# Crear .env con credenciales
cat > .env << EOF
WHATSAPP_TOKEN=tu_token
VERIFY_TOKEN=tu_verify_token
PHONE_NUMBER_ID=tu_numero_id
EOF

# Ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f chatbot
```

---

### Opción 3: Plataforma Serverless (Bajo Presupuesto)

#### Google Cloud Run
```bash
# 1. Crear proyecto en Google Cloud
# 2. Instalar Google Cloud SDK
gcloud init

# 3. Desplegar
gcloud run deploy chatbot-whatsapp \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### AWS Lambda + API Gateway
```bash
# 1. Usar framework Serverless
npm install -g serverless
serverless create --template aws-python

# 2. Configurar serverless.yml
# 3. Desplegar
serverless deploy
```

---

## 🎯 Recomendaciones de Servidores

### Comparativa por Caso de Uso

| Caso de Uso | Servidor Recomendado | Especificaciones | Costo Mensual |
|---|---|---|---|
| **Desarrollo Local** | Tu PC / Laptop | Python 3.10+ | $0 |
| **Testing Inicial** | Heroku Free | 512MB RAM | $0-7 |
| **Producción - Bajo Tráfico** | DigitalOcean Droplet | 2GB RAM, 2vCore | $12-18 |
| **Producción - Medio Tráfico** | Linode Nanode+ | 4GB RAM, 2vCore | $18-24 |
| **Producción - Alto Tráfico** | AWS EC2 t3.medium | 4GB RAM, 2vCore | $30-40 |
| **Escalabilidad Máxima** | Kubernetes (EKS/GKE) | Personalizado | $50+ |
| **Máxima Economía** | Oracle Cloud Free | 4GB RAM Gratis | $0 |

---

### Opción 1: DigitalOcean (⭐ MÁS RECOMENDADO)

**Ventajas:**
- ✅ Interfaz simple e intuitiva
- ✅ Excelente documentación
- ✅ Buena relación precio-rendimiento
- ✅ Deploy fácil con App Platform

**Pasos Rápidos:**
1. Crear cuenta en https://digitalocean.com
2. Crear Droplet Ubuntu 22.04 ($5-12/mes)
3. Seguir pasos de "Servidor VPS" arriba
4. Alternativa: Usar **App Platform** para deploy automático

**Costo: $5-15/mes** (excelente valor)

---

### Opción 2: Oracle Cloud (⭐ MÁS GRATUITO)

**Ventajas:**
- ✅ Nivel gratuito generoso (4GB RAM perpetuo)
- ✅ Instancia siempre activa sin tiempo límite
- ✅ 1 TB almacenamiento
- ✅ Banda ancha ilimitada

**Pasos Rápidos:**
1. Crear cuenta en https://www.oracle.com/cloud/free/
2. Crear instancia Compute (Ampere A1)
3. Instalar Ubuntu 22.04
4. Seguir pasos de "Servidor VPS"

**Costo: $0** (puede costar si excedes límites)

---

### Opción 3: Railway.app (Iniciantes)

**Ventajas:**
- ✅ Deploy super fácil desde GitHub
- ✅ Variables de ambiente gráficas
- ✅ Automático con cada push

**Pasos:**
1. Conectar GitHub
2. Seleccionar repositorio
3. Railway detecta Python automáticamente
4. Configurar variables .env
5. ¡Listo! Actualiza automáticamente

**Costo: $5/mes créditos gratis + después $0.50/GB uso**

---

### Opción 4: Amazon AWS (Para Escalabilidad)

**Ventajas:**
- ✅ Nivel gratuito 12 meses
- ✅ Excelente escalabilidad
- ✅ Servicios complementarios (S3, CloudWatch, etc.)

**Pasos:**
1. Crear cuenta AWS Free Tier
2. EC2 t2.micro (gratis 12 meses)
3. RDS para base de datos
4. ElastiCache para Redis

**Costo: Gratis primer año, luego $10-30+/mes**

---

### Opción 5: Heroku (Deprecado - NO RECOMENDADO)

❌ Heroku eliminó su opción gratuita en 2022  
⚠️ Costo mínimo $7/mes sin características

---

## 🔐 Configuración WhatsApp Business API

### Paso 1: Crear Cuenta Empresarial en Meta/Facebook

1. Ir a https://www.facebook.com/business
2. Crear empresa (si no existe)
3. Agregar aplicación WhatsApp Business

### Paso 2: Obtener Credenciales

```
WHATSAPP_TOKEN = 
  [Token de acceso de la app]
  Ubicación: App → Settings → Basic → App Secret

VERIFY_TOKEN = 
  Token personalizado (tú lo creas, ejm: "mi_token_super_secreto")

PHONE_NUMBER_ID = 
  Número de teléfono empresarial registrado
  Formato: 34600123456 (sin +)
```

### Paso 3: Configurar Webhook

En tu servidor:
```
URL del Webhook: https://tu-dominio.com/webhook
Token de Verificación: El que creaste arriba
```

En admin.facebook.com:
1. App → Configuration → Webhooks
2. Agregar URL del webhook
3. Seleccionar eventos: `messages`, `message_template_status_update`

### Paso 4: Probar Conexión

```bash
# Desde terminal
curl -X GET "https://tu-dominio.com/webhook?hub.mode=subscribe&hub.challenge=TEST&hub.verify_token=tu_verify_token"

# Deberá retornar: TEST
```

---

## ✅ Verificación y Pruebas

### Verificar Instalación

```bash
# 1. Python y dependencias
python --version
pip list | grep -E "fastapi|redis|spacy"

# 2. Base de datos y Redis
ls -la chatbot.db
redis-cli ping

# 3. Modelo de NLP
python -c "import spacy; nlp = spacy.load('es_core_news_sm'); print('✓ spaCy OK')"

# 4. Servidor corriendo
curl http://localhost:8000/docs
# Deberá abrir Swagger UI
```

### Prueba de Mensaje

```bash
# Enviar mensaje POST
curl -X POST "http://localhost:8000/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "whatsapp_business_account",
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "34600123456",
            "id": "test_123",
            "text": {"body": "Hola, ¿cómo estás?"},
            "timestamp": "'$(date +%s)'"
          }]
        }
      }]
    }]
  }'
```

---

## 🆘 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'spacy'"

**Solución:**
```bash
source venv/bin/activate  # o .\venv\Scripts\Activate.ps1 en Windows
pip install spacy
python -m spacy download es_core_news_sm
```

---

### Problema: "Redis connection refused"

**Solución:**
```bash
# Linux: Instalar Redis
sudo apt install redis-server
sudo systemctl start redis-server

# Windows: Descargar de https://github.com/microsoftarchive/redis/releases
# O usar WSL: wsl --install -d Ubuntu
```

**Alternativa:** Comentar Redis en `config.py` (usará caché en memoria)

---

### Problema: "Port 8000 already in use"

**Solución:**
```bash
# Cambiar puerto
uvicorn main:app --port 8001

# O matar proceso (Linux/Mac)
lsof -i :8000
kill -9 <PID>

# O en Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

---

### Problema: Timeout en webhook de WhatsApp

**Solución:**
1. Aumentar límite de tiempo en config (`MAX_RESPONSE_TIME`)
2. Ejecutar procesamiento asíncrono (`BackgroundTasks`)
3. Usar respuesta inmediata (HTTP 200) y resolver después

---

## 📊 Monitoreo en Producción

### Ver Logs
```bash
# Sistema
sudo journalctl -u chatbot -f

# Docker
docker-compose logs -f chatbot

# Uvicorn
tail -f chatbot.log
```

### Métricas Importantes
```bash
# CPU y RAM
top
# o
htop

# Conexiones
netstat -tulpn | grep 8000

# Base de datos
du -sh chatbot.db
```

---

## 📚 Próximos Pasos

1. ✅ Instalación completada
2. 📖 Leer documentación de arquitectura
3. 🧪 Entrenar modelo con tus intenciones
4. 🔄 Configurar autoaprendizaje
5. 📈 Monitorear rendimiento
6. 🚀 Escalar según necesidad

---

## 📞 Soporte

- 📧 Email: tu-email@ejemplo.com
- 🐛 Issues: GitHub Issues
- 💬 Comunidad: Telegram/Discord
- 📚 Docs: README.md + Arquitectura.md

---

**¡Listo para chatear con WhatsApp! 🚀**
