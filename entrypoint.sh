#!/bin/sh
set -e

# echo "Ejecutando migraciones de Alembic..."
# alembic upgrade head

echo "Iniciando servidor..."
exec gunicorn src.main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
