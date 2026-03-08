#!/bin/bash

# Smoke Tests for Voting System
# Quick health checks for any environment
# Usage: ./scripts/smoke-tests.sh <environment>
# Example: ./scripts/smoke-tests.sh staging

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
ENVIRONMENT=${1:-dev}
API_URL="http://${ENVIRONMENT}.voting.local/api"
MAX_RETRIES=10
RETRY_DELAY=10

echo "🔍 Smoke Tests for $ENVIRONMENT"
echo "API URL: $API_URL"
echo ""

# Health check with retries
echo "Testing health endpoint..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -f -s "$API_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check passed${NC}"
        break
    else
        if [ $i -eq $MAX_RETRIES ]; then
            echo -e "${RED}❌ Health check failed after $MAX_RETRIES retries${NC}"
            exit 1
        fi
        echo "Retry $i/$MAX_RETRIES..."
        sleep $RETRY_DELAY
    fi
done

# Basic endpoints
echo "Testing API root..."
if curl -f -s "$API_URL/" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API root accessible${NC}"
else
    echo -e "${RED}❌ API root not accessible${NC}"
    exit 1
fi

echo "Testing surveys list..."
if curl -f -s "$API_URL/surveys/" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Surveys endpoint accessible${NC}"
else
    echo -e "${RED}❌ Surveys endpoint not accessible${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All smoke tests passed!${NC}"
