FROM python:3.11-slim

# Metadatos de la imagen
LABEL maintainer="support-tickets"
LABEL description="API REST para gestión de tickets de soporte"
LABEL version="1.0.0"

WORKDIR /app

# Variables de entorno de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar requirements antes para aprovechar la cache de docker
COPY requirements.txt .

# Instalar dependencias del sistema necesarias para compilar extensiones
# y para psycopg2; luego instalar dependencias Python y limpiar paquetes pesados.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   gcc \
	   libpq-dev \
	&& pip install --upgrade pip setuptools wheel \
	&& pip install --no-cache-dir -r requirements.txt \
	&& apt-get purge -y gcc \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Copiar el código de la aplicación
COPY . .

# Hacer el script ejecutable
RUN chmod +x start.sh

# Cambiar propiedad de los archivos al usuario no-root
RUN chown -R appuser:appuser /app

# Cambiar al usuario no-root
USER appuser

# Exponer el puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Comando por defecto
CMD ["./start.sh"]
