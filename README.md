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

**Nota:** Las migraciones de base de datos se aplican automáticamente al iniciar el contenedor. El script de inicio espera a que PostgreSQL esté listo y luego ejecuta `alembic upgrade head` antes de iniciar el servidor.

Si necesitas ejecutar las migraciones manualmente:

```sh
docker compose exec web alembic upgrade head
```

Para detener los servicios:

```sh
docker compose down

# Para eliminar también los datos de la base de datos
docker compose down -v
```

#### Solución de problemas

**Problema: "PostgreSQL Database directory appears to contain a database; Skipping initialization"**

Si ves este mensaje y la base de datos está vacía (sin tablas), significa que el volumen de Docker tiene datos antiguos pero la base de datos no está inicializada correctamente. Soluciones:

1. **Limpiar el volumen y reiniciar (recomendado):**
   ```sh
   docker compose down -v
   docker compose up --build
   ```

2. **Forzar la aplicación de migraciones:**
   ```sh
   docker compose exec web alembic upgrade head
   ```

3. **Verificar el estado de las migraciones:**
   ```sh
   docker compose exec web alembic current
   docker compose exec web alembic history
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
En Fedora
```sh
sudo dnf update
sudo dnf group install -y development-tools && sudo dnf install -y libpq-devel python3-devel
```



#### Configuración

1. **Crear y activar entorno virtual:**

```sh
python -m venv .venv
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
# Usando Docker
docker compose exec db psql -U postgres -c "CREATE DATABASE tickets_db;"
```

5. **Aplicar migraciones:**

```sh
docker compose exec web alembic upgrade head

```
Otros comandos alembic utiles
```sh
# Ver el estado actual de las migraciones
docker compose exec web alembic current

# Ver el historial de migraciones
docker compose exec web alembic history

# Crear una nueva migración
docker compose exec web alembic revision -m "descripcion de la migracion"
```

6. **Arrancar el servidor:**

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verificar que funciona

La API quedará accesible en `http://localhost:8000`.

- **Swagger UI (docs interactivos):** `http://localhost:8000/docs`
- **Api yml:** `http://localhost:8000/openapi.json`
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

### Una vez funcionando la aplicacion puedes verificar que todo esté correcto accediendo a:
```sh
API Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/health
```

## Diseño Técnico

### Arquitectura Hexagonal (Puertos y Adaptadores)

La aplicación está estructurada siguiendo el patrón de **Arquitectura Hexagonal** (también conocida como Arquitectura de Puertos y Adaptadores), que separa la lógica de negocio de los detalles de implementación técnica, facilitando el mantenimiento, la testabilidad y la escalabilidad.

#### Estructura de Directorios

#### Capas de la Arquitectura

##### 1. Domain (Dominio)
- **Responsabilidad**: Contiene la lógica de negocio pura, independiente de frameworks y tecnologías.
- **Componentes**:
  - **Entities**: Entidades de dominio que representan los conceptos del negocio (User, Item, ItemStatus).
  - **Repositories (Puertos)**: Interfaces abstractas que definen los contratos para acceder a datos, sin depender de implementaciones concretas.

##### 2. Application (Aplicación)
- **Responsabilidad**: Orquesta los casos de uso y coordina las operaciones de negocio.
- **Componentes**:
  - **Use Cases**: Cada caso de uso encapsula una operación de negocio específica (crear item, autenticar usuario, etc.).
  - **Services**: Servicios de aplicación que proporcionan funcionalidad compartida (autenticación, autorización).

##### 3. Infrastructure (Infraestructura)
- **Responsabilidad**: Implementa los adaptadores que conectan la aplicación con sistemas externos.
- **Componentes**:
  - **Database/Models**: Modelos SQLAlchemy que representan las tablas de la base de datos.
  - **Repositories (Implementaciones)**: Implementaciones concretas de los repositorios que usan SQLAlchemy para persistir datos.
  - **Mappers**: Funciones que convierten entre entidades de dominio y modelos de infraestructura.
  - **Security**: Implementaciones de servicios de seguridad (JWT, hash de contraseñas).

##### 4. Interfaces (Interfaces)
- **Responsabilidad**: Adaptadores de entrada que exponen la aplicación al mundo exterior.
- **Componentes**:
  - **API/Routes**: Endpoints REST de FastAPI que reciben peticiones HTTP.
  - **Schemas**: DTOs (Data Transfer Objects) de Pydantic para validación y serialización.
  - **Converters**: Funciones que convierten entre entidades de dominio y schemas de la API.

#### Flujo de Datos


#### Principios Aplicados

1. **Inversión de Dependencias**: El dominio define interfaces (puertos) que la infraestructura implementa (adaptadores).
2. **Separación de Concerns**: Cada capa tiene una responsabilidad clara y bien definida.
3. **Independencia del Framework**: El dominio no depende de FastAPI, SQLAlchemy u otras tecnologías.
4. **Testabilidad**: Las interfaces permiten mockear fácilmente las dependencias en los tests.

#### Beneficios

- ✅ **Mantenibilidad**: Código organizado y fácil de navegar.
- ✅ **Escalabilidad**: Fácil agregar nuevas funcionalidades sin afectar el código existente.
- ✅ **Testabilidad**: Cada capa puede probarse de forma independiente.
- ✅ **Flexibilidad**: Cambiar la base de datos o el framework web sin afectar la lógica de negocio.
- ✅ **Claridad**: La estructura refleja claramente las responsabilidades de cada componente.