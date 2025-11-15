# Backend REST con FastAPI y PostgreSQL (Docker)

Este proyecto es un ejemplo mínimo de un backend en Python que expone una API REST usando FastAPI, almacena datos en PostgreSQL y se orquesta con Docker Compose.

Servicios:
- `web`: FastAPI ejecutándose con Uvicorn
- `db`: PostgreSQL

Arrancar los servicios:

```sh
docker compose up --build
```

La API quedará accesible en `http://localhost:8000`.

Endpoints de ejemplo (items):
- `POST /items/` - crear item (JSON `{"name": "foo", "description": "..."}`)
- `GET /items/` - listar items
- `GET /items/{id}` - obtener item
- `PUT /items/{id}` - actualizar item
- `DELETE /items/{id}` - borrar item

Docs automáticos: `http://localhost:8000/docs`

Notas para desarrollo local (sin Docker):

- En distribuciones Debian/Ubuntu es necesario instalar las dependencias de compilación para `psycopg2`:

```sh
sudo apt update
sudo apt install -y build-essential libpq-dev python3-dev
```

- Alternativamente, ejecutar la aplicación y tests dentro de Docker evita necesitar estas dependencias en tu máquina local.

