#!/bin/sh
set -e

# Update image tag in values-dev.yaml
# Usage: ./update-image-tag-dev.sh <component> <image-tag>
# Example: ./update-image-tag-dev.sh backend dev-abc1234

COMPONENT="$1"
IMAGE_TAG="$2"

if [ -z "$COMPONENT" ] || [ -z "$IMAGE_TAG" ]; then
  echo "Usage: $0 <component> <image-tag>"
  echo "Example: $0 backend dev-abc1234"
  exit 1
fi

echo "Updating $COMPONENT tag in values-dev.yaml to: $IMAGE_TAG"

case "$COMPONENT" in
  backend)
    sed -i "/^backend:/,/^frontend:/ s#tag: dev.*#tag: ${IMAGE_TAG}#" charts/voting-system/values-dev.yaml
    ;;
  frontend)
    sed -i "/^frontend:/,/^cockroachdb:/ s#tag: dev.*#tag: ${IMAGE_TAG}#" charts/voting-system/values-dev.yaml
    ;;
  *)
    echo "Error: Unknown component '$COMPONENT'. Use 'backend' or 'frontend'"
    exit 1
    ;;
esac

echo "$COMPONENT tag updated successfully"
