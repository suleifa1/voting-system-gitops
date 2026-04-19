#!/bin/sh
set -e

# Update image tag in values-staging.yaml
# Usage: ./update-image-tag-staging.sh <component> <image-tag>
# Example: ./update-image-tag-staging.sh backend staging-abc1234

COMPONENT="$1"
IMAGE_TAG="$2"

if [ -z "$COMPONENT" ] || [ -z "$IMAGE_TAG" ]; then
  echo "Usage: $0 <component> <image-tag>"
  echo "Example: $0 backend staging-abc1234"
  exit 1
fi

echo "Updating $COMPONENT tag in values-staging.yaml to: $IMAGE_TAG"

case "$COMPONENT" in
  backend)
    sed -i "/^backend:/,/^frontend:/ s#tag: staging.*#tag: ${IMAGE_TAG}#" charts/voting-system/values-staging.yaml
    ;;
  frontend)
    sed -i "/^frontend:/,/^cockroachdb:/ s#tag: staging.*#tag: ${IMAGE_TAG}#" charts/voting-system/values-staging.yaml
    ;;
  *)
    echo "Error: Unknown component '$COMPONENT'. Use 'backend' or 'frontend'"
    exit 1
    ;;
esac

echo "$COMPONENT tag updated successfully"
