#!/bin/bash

# E2E Tests for Voting System
# Usage: ./scripts/e2e-tests.sh <environment>
# Example: ./scripts/e2e-tests.sh dev

set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-dev}
API_URL="http://${ENVIRONMENT}.voting.local/api"
TIMESTAMP=$(date +%s)
TEST_EMAIL="e2e-${TIMESTAMP}@test.com"
TEST_USERNAME="e2e${TIMESTAMP}"
TEST_PASSWORD="test123456"

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_test() {
    echo -e "${YELLOW}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((TESTS_PASSED++))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    ((TESTS_FAILED++))
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Perform HTTP request with error handling
http_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local headers=$4
    
    local url="${API_URL}${endpoint}"
    local response
    local http_code
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            ${headers:+-H "$headers"} \
            -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            ${headers:+-H "$headers"})
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    echo "$http_code|$body"
}

# Test functions
test_health_check() {
    print_test "Testing health endpoint..."
    
    local result=$(http_request "GET" "/health" "" "")
    local http_code=$(echo "$result" | cut -d'|' -f1)
    local body=$(echo "$result" | cut -d'|' -f2-)
    
    if [ "$http_code" = "200" ]; then
        local status=$(echo "$body" | jq -r '.status' 2>/dev/null || echo "")
        if [ "$status" = "healthy" ]; then
            print_success "Health check passed (status: $status)"
            return 0
        fi
    fi
    
    print_error "Health check failed (HTTP $http_code)"
    echo "Response: $body"
    return 1
}

test_api_root() {
    print_test "Testing API root endpoint..."
    
    local result=$(http_request "GET" "/" "" "")
    local http_code=$(echo "$result" | cut -d'|' -f1)
    
    if [ "$http_code" = "200" ]; then
        print_success "API root endpoint accessible"
        return 0
    fi
    
    print_error "API root endpoint failed (HTTP $http_code)"
    return 1
}

test_surveys_list() {
    print_test "Testing surveys list endpoint..."
    
    local result=$(http_request "GET" "/surveys/" "" "")
    local http_code=$(echo "$result" | cut -d'|' -f1)
    local body=$(echo "$result" | cut -d'|' -f2-)
    
    if [ "$http_code" = "200" ]; then
        # Check if response is a valid JSON array
        if echo "$body" | jq -e 'type == "array"' >/dev/null 2>&1; then
            local count=$(echo "$body" | jq 'length')
            print_success "Surveys list retrieved ($count surveys)"
            return 0
        fi
    fi
    
    print_error "Surveys list failed (HTTP $http_code)"
    return 1
}

test_user_registration() {
    print_test "Testing user registration..."
    
    local data="{\"email\":\"$TEST_EMAIL\",\"username\":\"$TEST_USERNAME\",\"password\":\"$TEST_PASSWORD\"}"
    local result=$(http_request "POST" "/auth/register" "$data" "")
    local http_code=$(echo "$result" | cut -d'|' -f1)
    local body=$(echo "$result" | cut -d'|' -f2-)
    
    if [ "$http_code" = "200" ]; then
        ACCESS_TOKEN=$(echo "$body" | jq -r '.access_token')
        
        if [ "$ACCESS_TOKEN" != "null" ] && [ -n "$ACCESS_TOKEN" ]; then
            print_success "User registration successful"
            print_info "Token: ${ACCESS_TOKEN:0:20}..."
            return 0
        fi
    fi
    
    print_error "User registration failed (HTTP $http_code)"
    echo "Response: $body"
    return 1
}

test_token_verification() {
    print_test "Testing token verification..."
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available"
        return 1
    fi
    
    local result=$(http_request "GET" "/auth/verify" "" "Authorization: Bearer $ACCESS_TOKEN")
    local http_code=$(echo "$result" | cut -d'|' -f1)
    local body=$(echo "$result" | cut -d'|' -f2-)
    
    if [ "$http_code" = "200" ]; then
        local valid=$(echo "$body" | jq -r '.valid' 2>/dev/null || echo "false")
        if [ "$valid" = "true" ]; then
            local username=$(echo "$body" | jq -r '.user.username' 2>/dev/null || echo "")
            print_success "Token verification passed (user: $username)"
            return 0
        fi
    fi
    
    print_error "Token verification failed (HTTP $http_code)"
    return 1
}

test_get_current_user() {
    print_test "Testing get current user profile..."
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available"
        return 1
    fi
    
    local result=$(http_request "GET" "/auth/me" "" "Authorization: Bearer $ACCESS_TOKEN")
    local http_code=$(echo "$result" | cut -d'|' -f1)
    local body=$(echo "$result" | cut -d'|' -f2-)
    
    if [ "$http_code" = "200" ]; then
        local email=$(echo "$body" | jq -r '.email' 2>/dev/null || echo "")
        if [ "$email" = "$TEST_EMAIL" ]; then
            print_success "User profile retrieved correctly"
            return 0
        fi
    fi
    
    print_error "Get current user failed (HTTP $http_code)"
    return 1
}

# Main execution
main() {
    print_section "E2E Tests for $ENVIRONMENT Environment"
    
    print_info "API URL: $API_URL"
    print_info "Test User: $TEST_EMAIL"
    print_info "Timestamp: $TIMESTAMP"
    
    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        print_error "jq is not installed. Please install jq to run these tests."
        exit 1
    fi
    
    # Smoke Tests
    print_section "Smoke Tests"
    test_health_check || true
    test_api_root || true
    test_surveys_list || true
    
    # Authentication Flow
    print_section "Authentication Flow"
    test_user_registration || exit 1  # Critical test
    test_token_verification || true
    test_get_current_user || true
    
    # Summary
    print_section "Test Summary"
    
    local total=$((TESTS_PASSED + TESTS_FAILED))
    echo "Total tests: $total"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    
    if [ $TESTS_FAILED -gt 0 ]; then
        echo -e "${RED}Failed: $TESTS_FAILED${NC}"
        echo ""
        print_error "Some tests failed!"
        exit 1
    else
        echo -e "${RED}Failed: 0${NC}"
        echo ""
        print_success "All tests passed! 🎉"
        exit 0
    fi
}

# Run main function
main
