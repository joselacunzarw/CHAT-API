# ChatBot API con FastAPI y Google OAuth

API REST para un chatbot con autenticación Google OAuth2, auditoría de uso y persistencia en SQLite.

## Características

- 🔐 Autenticación con Google OAuth2
- 📝 Auditoría automática de todas las llamadas a la API
- 🗄️ Persistencia en SQLite con volumen Docker
- 🚀 FastAPI para alto rendimiento
- 📚 Documentación automática con Swagger/OpenAPI

## Requisitos

- Docker y Docker Compose
- Credenciales de Google OAuth2 (Client ID y Client Secret)

## Configuración Inicial

1. Clona el repositorio:
```bash
git clone <repositorio>
cd <directorio>
```

2. Copia el archivo de ejemplo de variables de entorno:
```bash
cp .env.example .env
```

3. Edita `.env` con tus credenciales:
```env
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret
SECRET_KEY=tu_clave_secreta
```

## Ejecución en Producción

1. Construye y levanta los contenedores:
```bash
docker compose up --build
```

2. Para ejecutar en segundo plano:
```bash
docker compose up -d --build
```

3. Para detener los servicios:
```bash
docker compose down
```

La API estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

## Ejecución en Desarrollo

1. Crea y activa un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
export GOOGLE_CLIENT_ID=tu_client_id
export GOOGLE_CLIENT_SECRET=tu_client_secret
export SECRET_KEY=tu_clave_secreta
```

4. Ejecuta el servidor de desarrollo:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Estructura del Proyecto

```
.
├── app/
│   ├── api/
│   │   └── audit.py          # Lógica de auditoría
│   ├── auth/
│   │   └── oauth.py          # Autenticación Google
│   ├── models/
│   │   ├── database.py       # Configuración DB
│   │   └── models.py         # Modelos SQLAlchemy
│   ├── utils/
│   │   └── init_setup.py     # Inicialización
│   ├── core.py              # Lógica del chatbot
│   └── main.py              # Endpoints FastAPI
├── data/                    # Volumen para SQLite
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Endpoints

### POST /recuperar_documentos
Recupera documentos relevantes para una pregunta.
- Requiere autenticación
- Parámetros:
  - `question`: string (requerido)

### POST /consultar
Consulta al LLM con contexto e historial.
- Requiere autenticación
- Parámetros:
  - `question`: string (requerido)
  - `history`: list (opcional)

## Base de Datos

La base de datos SQLite se almacena en `./data/app.db` y persiste fuera del contenedor.

### Modelos
- **Users**: Almacena usuarios autenticados con Google
- **AuditLog**: Registra todas las llamadas a la API

## Logs y Monitoreo

Para ver los logs en producción:
```bash
# Ver logs de todos los servicios
docker compose logs -f

# Ver logs específicos de la API
docker compose logs -f api
```

## Mantenimiento

Para actualizar la aplicación en producción:
```bash
git pull                     # Actualiza el código
docker compose down          # Detiene los servicios
docker compose up -d --build # Reconstruye y levanta los servicios
```

## Solución de Problemas

1. Si la API no inicia:
   - Verifica que el puerto 8000 esté disponible
   - Comprueba los logs con `docker compose logs api`
   - Verifica las variables de entorno en `.env`

2. Si hay problemas de permisos en la base de datos:
   - Verifica que el directorio `data/` tenga los permisos correctos
   - Ejecuta: `chmod 755 data/`

3. Si la autenticación falla:
   - Verifica las credenciales de Google OAuth2
   - Comprueba que las URLs de redirección estén configuradas en Google Console