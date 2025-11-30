#!/bin/bash
# Script para construir y etiquetar la imagen Docker para producción
# Uso: ./build-and-push.sh [version] [registry]

set -e

VERSION=${1:-"1.0.0"}
REGISTRY=${2:-""}  # Opcional: tu-registry.com/namespace

IMAGE_NAME="support-tickets"
FULL_IMAGE_NAME="${REGISTRY}${IMAGE_NAME}:${VERSION}"
LATEST_TAG="${REGISTRY}${IMAGE_NAME}:latest"

echo "🔨 Construyendo imagen Docker..."
docker build -t "${FULL_IMAGE_NAME}" -t "${LATEST_TAG}" .

echo "✅ Imagen construida exitosamente"
echo "   - ${FULL_IMAGE_NAME}"
echo "   - ${LATEST_TAG}"

if [ -n "$REGISTRY" ]; then
    echo ""
    echo "📤 Para subir la imagen al registry, ejecuta:"
    echo "   docker push ${FULL_IMAGE_NAME}"
    echo "   docker push ${LATEST_TAG}"
fi

echo ""
echo "🚀 Para usar la imagen localmente:"
echo "   docker run -p 8000:8000 --env-file .env ${FULL_IMAGE_NAME}"

