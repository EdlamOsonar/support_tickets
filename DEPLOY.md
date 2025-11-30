# Guía de Despliegue en Producción

Esta guía explica cómo desplegar la aplicación de tickets de soporte en un VPS usando Docker.

## Requisitos Previos

- VPS con Docker y Docker Compose instalados
- Acceso SSH al servidor
- Dominio o IP pública (opcional, para acceso externo)

## Paso 1: Preparar el Servidor

### Instalar Docker y Docker Compose

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt install docker-compose-plugin -y

# Agregar usuario al grupo docker (opcional, para no usar sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verificar instalación
docker --version
docker compose version
```

## Paso 2: Subir el Código al Servidor

### Opción A: Usando Git (Recomendado)

```bash
# En el servidor
cd /opt  # o el directorio que prefieras
git clone <tu-repositorio> support-tickets
cd support-tickets
git checkout <tag-o-branch-de-produccion>
```

### Opción B: Usando SCP

```bash
# Desde tu máquina local
scp -r /ruta/local/support_tickets usuario@servidor:/opt/support-tickets
```

## Paso 3: Configurar Variables de Entorno

```bash
# En el servidor, dentro del directorio del proyecto
cp .env.example .env

# Editar el archivo .env con valores de producción
nano .env
```

**Configuración mínima requerida:**

```env
# Generar una SECRET_KEY segura
SECRET_KEY=$(openssl rand -hex 32)

# Configurar DATABASE_URL (ajustar según tu configuración)
DATABASE_URL=postgresql://postgres:TU_PASSWORD_SEGURO@db:5432/postgres

# Configurar credenciales de PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=TU_PASSWORD_SEGURO
POSTGRES_DB=postgres

# Puerto de la aplicación (opcional, por defecto 8000)
APP_PORT=8000
```

**⚠️ IMPORTANTE:**
- Cambia `SECRET_KEY` por una clave aleatoria segura (usa `openssl rand -hex 32`)
- Cambia `POSTGRES_PASSWORD` por una contraseña fuerte
- No compartas el archivo `.env` ni lo subas al repositorio

## Paso 4: Construir y Ejecutar la Aplicación

### Construir la imagen Docker

```bash
# Construir la imagen
docker compose -f docker-compose.prod.yml build

# O construir y ejecutar en un solo paso
docker compose -f docker-compose.prod.yml up -d --build
```

### Verificar que los contenedores estén corriendo

```bash
docker compose -f docker-compose.prod.yml ps
```

Deberías ver dos contenedores corriendo:
- `support-tickets-api` (web)
- `support-tickets-db` (db)

### Ver los logs

```bash
# Ver logs de todos los servicios
docker compose -f docker-compose.prod.yml logs -f

# Ver logs solo de la API
docker compose -f docker-compose.prod.yml logs -f web

# Ver logs solo de la base de datos
docker compose -f docker-compose.prod.yml logs -f db
```

## Paso 5: Verificar que la Aplicación Funciona

```bash
# Health check
curl http://localhost:8000/health

# Debería responder: {"status":"ok"}

# Verificar documentación de la API
curl http://localhost:8000/docs
```

## Paso 6: Configurar Firewall (Opcional pero Recomendado)

```bash
# Permitir puerto 8000 (si quieres acceso directo)
sudo ufw allow 8000/tcp

# O mejor aún, usar un reverse proxy (Nginx) en el puerto 80/443
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## Paso 7: Configurar Nginx como Reverse Proxy (Recomendado)

### Instalar Nginx

```bash
sudo apt install nginx -y
```

### Configurar Nginx

Crear archivo de configuración:

```bash
sudo nano /etc/nginx/sites-available/support-tickets
```

Contenido:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;  # O tu IP pública

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilitar el sitio:

```bash
sudo ln -s /etc/nginx/sites-available/support-tickets /etc/nginx/sites-enabled/
sudo nginx -t  # Verificar configuración
sudo systemctl reload nginx
```

### Configurar SSL con Let's Encrypt (Recomendado)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# El certificado se renovará automáticamente
```

## Comandos Útiles

### Detener la aplicación

```bash
docker compose -f docker-compose.prod.yml down
```

### Reiniciar la aplicación

```bash
docker compose -f docker-compose.prod.yml restart
```

### Actualizar la aplicación

```bash
# 1. Detener contenedores
docker compose -f docker-compose.prod.yml down

# 2. Actualizar código (si usas Git)
git pull origin main

# 3. Reconstruir y levantar
docker compose -f docker-compose.prod.yml up -d --build
```

### Ver estado de las migraciones

```bash
docker compose -f docker-compose.prod.yml exec web alembic current
```

### Aplicar migraciones manualmente (si es necesario)

```bash
docker compose -f docker-compose.prod.yml exec web alembic upgrade head
```

### Acceder a la base de datos

```bash
docker compose -f docker-compose.prod.yml exec db psql -U postgres -d postgres
```

### Hacer backup de la base de datos

```bash
docker compose -f docker-compose.prod.yml exec db pg_dump -U postgres postgres > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restaurar backup

```bash
cat backup_20240101_120000.sql | docker compose -f docker-compose.prod.yml exec -T db psql -U postgres postgres
```

## Monitoreo y Mantenimiento

### Ver uso de recursos

```bash
docker stats
```

### Limpiar recursos no utilizados

```bash
# Limpiar imágenes, contenedores y volúmenes no utilizados
docker system prune -a --volumes

# ⚠️ CUIDADO: Esto eliminará todo lo no utilizado, incluyendo volúmenes
```

### Ver logs persistentes

Los logs se guardan en `/var/lib/docker/containers/` por defecto. Puedes configurar un sistema de logging centralizado si lo necesitas.

## Solución de Problemas

### La aplicación no inicia

1. Verificar logs:
   ```bash
   docker compose -f docker-compose.prod.yml logs web
   ```

2. Verificar que las variables de entorno estén correctas:
   ```bash
   docker compose -f docker-compose.prod.yml exec web env | grep -E "DATABASE_URL|SECRET_KEY"
   ```

3. Verificar que la base de datos esté lista:
   ```bash
   docker compose -f docker-compose.prod.yml exec db pg_isready -U postgres
   ```

### Error de conexión a la base de datos

1. Verificar que el contenedor de la base de datos esté corriendo:
   ```bash
   docker compose -f docker-compose.prod.yml ps db
   ```

2. Verificar la URL de conexión en `.env`

3. Verificar logs de la base de datos:
   ```bash
   docker compose -f docker-compose.prod.yml logs db
   ```

### Las migraciones no se aplican

1. Aplicar manualmente:
   ```bash
   docker compose -f docker-compose.prod.yml exec web alembic upgrade head
   ```

2. Ver estado actual:
   ```bash
   docker compose -f docker-compose.prod.yml exec web alembic current
   ```

## Seguridad en Producción

1. ✅ Cambiar `SECRET_KEY` por una clave aleatoria segura
2. ✅ Usar contraseñas fuertes para PostgreSQL
3. ✅ Configurar firewall (UFW)
4. ✅ Usar HTTPS con Let's Encrypt
5. ✅ No exponer el puerto de PostgreSQL (5432) públicamente
6. ✅ Mantener Docker y el sistema operativo actualizados
7. ✅ Hacer backups regulares de la base de datos
8. ✅ Monitorear logs para detectar actividad sospechosa

## Actualización a Nueva Versión

1. Hacer backup de la base de datos
2. Detener la aplicación
3. Actualizar el código
4. Reconstruir las imágenes
5. Aplicar migraciones si es necesario
6. Reiniciar la aplicación
7. Verificar que todo funcione correctamente

