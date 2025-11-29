# Backend REST con FastAPI y PostgreSQL (Docker)

Este proyecto es un backend en Python para gestionar tickets de soporte. Expone una API REST usando FastAPI, almacena datos en PostgreSQL y se orquesta con Docker Compose.

## Servicios

- `web`: FastAPI ejecutándose con Uvicorn
- `db`: PostgreSQL

## Arrancar la aplicación

### Opción 1: Con Docker (recomendado)

```sh
# Construir y arrancar los servicios
docker compose up --build

# O en segundo plano
docker compose up --build -d
```

Después de arrancar, aplica las migraciones de base de datos:

```sh
docker compose exec web alembic upgrade head
```

Para detener los servicios:

```sh
docker compose down

# Para eliminar también los datos de la base de datos
docker compose down -v
```

### Opción 2: En local (sin Docker)

#### Requisitos previos

- Python 3.10+
- PostgreSQL 15+ instalado y corriendo
- Dependencias de compilación (Debian/Ubuntu):

```sh
sudo apt update
sudo apt install -y build-essential libpq-dev python3-dev
```

#### Configuración

1. **Crear y activar entorno virtual:**

```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o en Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**

```sh
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**

Crea un archivo `.env` en la raíz del proyecto o exporta las variables:

```sh
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/tickets_db"
export SECRET_KEY="tu-clave-secreta-segura"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

4. **Crear la base de datos:**

```sh
# Conectar a PostgreSQL y crear la base de datos
psql -U postgres -c "CREATE DATABASE tickets_db;"
```

5. **Aplicar migraciones:**

```sh
alembic upgrade head
```

6. **Arrancar el servidor:**

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verificar que funciona

La API quedará accesible en `http://localhost:8000`.

- **Swagger UI (docs interactivos):** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Health check:** `http://localhost:8000/health`

```sh
# Verificar que el servidor responde
curl http://localhost:8000/health
# Respuesta: {"status":"ok"}
```

## Autenticación y Autorización

La API utiliza **JWT (JSON Web Tokens)** con OAuth2 Password Flow para autenticación.

### Endpoints de autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/auth/register` | Registrar nuevo usuario |
| `POST` | `/auth/login` | Iniciar sesión (obtener token) |
| `GET` | `/auth/me` | Obtener información del usuario actual |

### Roles de usuario

El sistema soporta tres roles con diferentes niveles de permisos:

| Rol | Descripción |
|-----|-------------|
| `user` | Usuario básico, puede crear y ver tickets |
| `agent` | Agente de soporte, puede cambiar estados de tickets |
| `admin` | Administrador, acceso completo incluyendo eliminación |

### Permisos por endpoint

| Endpoint | `user` | `agent` | `admin` |
|----------|:------:|:-------:|:-------:|
| Crear ticket | ✅ | ✅ | ✅ |
| Listar tickets | ✅ | ✅ | ✅ |
| Ver ticket | ✅ | ✅ | ✅ |
| Actualizar ticket | ✅ | ✅ | ✅ |
| Cambiar estado | ❌ | ✅ | ✅ |
| Eliminar ticket | ❌ | ❌ | ✅ |

### Uso de la autenticación

#### 1. Registrar un usuario

```sh
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "mipassword", "full_name": "Mi Nombre"}'
```

#### 2. Iniciar sesión (obtener token)

```sh
curl -X POST http://localhost:8000/auth/login \
  -d "username=usuario@ejemplo.com&password=mipassword"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### 3. Usar endpoints protegidos

Incluye el token en el header `Authorization`:

```sh
curl http://localhost:8000/items/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Variables de entorno de seguridad

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Clave secreta para firmar tokens JWT | (cambiar en producción) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token | `30` |

## Endpoints de tickets

Todos los endpoints de tickets requieren autenticación (token JWT).

| Método | Endpoint | Descripción | Rol mínimo |
|--------|----------|-------------|------------|
| `POST` | `/items/` | Crear ticket | `user` |
| `GET` | `/items/` | Listar tickets | `user` |
| `GET` | `/items/{id}` | Obtener ticket | `user` |
| `PUT` | `/items/{id}` | Actualizar ticket | `user` |
| `PATCH` | `/items/{id}/status` | Cambiar estado | `agent` |
| `DELETE` | `/items/{id}` | Eliminar ticket | `admin` |

### Ejemplo: Crear ticket

```sh
curl -X POST http://localhost:8000/items/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Error en login",
    "description": "El usuario no puede acceder",
    "ticket_url": "https://jira.example.com/TICK-123",
    "reported_user": "cliente@ejemplo.com"
  }'
```

## Otros endpoints

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `GET` | `/statuses/` | Listar estados disponibles | Requerida |
| `GET` | `/health` | Health check | No requerida |

## Migraciones de base de datos

El proyecto usa Alembic para gestionar migraciones:

```sh
# Aplicar todas las migraciones
docker compose exec web alembic upgrade head

# Ver estado actual
docker compose exec web alembic current

# Crear nueva migración
docker compose exec web alembic revision -m "descripcion"
```

## Tests

### Ejecutar tests con Docker

```sh
docker compose exec web pytest -v
```

### Ejecutar tests en local

```sh
# Asegúrate de tener el entorno virtual activado
pytest -v
```
