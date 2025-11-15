FROM fedora:38

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar requirements antes para aprovechar la cache de docker
COPY requirements.txt .

# Instalar Python y dependencias del sistema necesarias para compilar extensiones
# y para psycopg2; luego instalar dependencias Python y limpiar paquetes pesados.
RUN dnf -y update \
	&& dnf -y install --setopt=tsflags=nodocs \
	   python3 \
	   python3-pip \
	   python3-devel \
	   gcc \
	   make \
	   libpq-devel \
	&& python3 -m pip install --upgrade pip setuptools wheel \
	&& python3 -m pip install --no-cache-dir -r requirements.txt \
	&& dnf -y remove gcc make \
	&& dnf -y autoremove \
	&& dnf clean all

COPY . .

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
