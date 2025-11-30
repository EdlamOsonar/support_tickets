#!/bin/bash
set -e

echo "Esperando a que la base de datos esté lista..."

# Esperar a que PostgreSQL esté listo usando SQLAlchemy
until python -c "
from sqlalchemy import create_engine, text
import os
engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres'))
try:
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print('Base de datos lista.')
    exit(0)
except Exception as e:
    exit(1)
" 2>/dev/null; do
  echo "Esperando a PostgreSQL..."
  sleep 2
done

echo "Verificando estado de las migraciones..."

# Verificar si la tabla alembic_version existe
ALEMBIC_EXISTS=$(python -c "
from sqlalchemy import create_engine, text, inspect
import os
engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres'))
inspector = inspect(engine)
tables = inspector.get_table_names()
print('alembic_version' in tables)
" 2>/dev/null || echo "False")

if [ "$ALEMBIC_EXISTS" = "False" ]; then
  echo "La base de datos está vacía. Aplicando todas las migraciones desde el principio..."
else
  echo "Migraciones existentes detectadas. Verificando estado actual..."
  alembic current
fi

echo "Aplicando migraciones de Alembic..."

# Aplicar migraciones de Alembic (esto es idempotente)
alembic upgrade head

echo "Verificando que las tablas se hayan creado correctamente..."

# Verificar que las tablas principales existan
python -c "
from sqlalchemy import create_engine, text, inspect
import os
import sys
engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres'))
inspector = inspect(engine)
tables = inspector.get_table_names()
required_tables = ['items', 'users', 'items_status', 'alembic_version']
missing = [t for t in required_tables if t not in tables]
if missing:
    print(f'ERROR: Faltan las siguientes tablas: {missing}', file=sys.stderr)
    print(f'Tablas existentes: {tables}', file=sys.stderr)
    sys.exit(1)
else:
    print(f'✓ Todas las tablas requeridas existen: {required_tables}')
"

if [ $? -ne 0 ]; then
  echo "ERROR: Las migraciones no se aplicaron correctamente."
  exit 1
fi

echo "Migraciones aplicadas correctamente. Iniciando servidor..."

# Iniciar el servidor
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

