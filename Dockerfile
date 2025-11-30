FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

COPY . .

# Hacer el script ejecutable
RUN chmod +x start.sh

CMD ["./start.sh"]
