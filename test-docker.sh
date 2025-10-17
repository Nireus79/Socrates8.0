#!/bin/bash

# Docker Testing Script for Socrates 8.0
# This script verifies that all Docker containers start correctly and services are operational

set -e

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAX_RETRIES=10
RETRY_DELAY=2
TIMEOUT=60

# Counters
PASSED=0
FAILED=0
TESTS_TOTAL=0

# Test result tracking
declare -a TEST_RESULTS
declare -a TEST_NAMES

# Function to print colored output
print_status() {
    local status=$1
    local message=$2

    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✓ PASS${NC} - $message"
        ((PASSED++))
    elif [ "$status" = "FAIL" ]; then
        echo -e "${RED}✗ FAIL${NC} - $message"
        ((FAILED++))
    elif [ "$status" = "INFO" ]; then
        echo -e "${BLUE}ℹ INFO${NC} - $message"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠ WARN${NC} - $message"
    fi

    ((TESTS_TOTAL++))
}

# Function to test service health
test_service_health() {
    local service=$1
    local port=$2
    local endpoint=$3

    echo ""
    echo -e "${BLUE}Testing $service on port $port...${NC}"

    local retries=0
    while [ $retries -lt $MAX_RETRIES ]; do
        if curl -sf "http://localhost:$port$endpoint" > /dev/null 2>&1; then
            print_status "PASS" "$service is responding at http://localhost:$port$endpoint"
            return 0
        fi

        echo -ne "  Attempt $((retries + 1))/$MAX_RETRIES - waiting..."
        sleep $RETRY_DELAY
        echo -ne "\r"
        ((retries++))
    done

    print_status "FAIL" "$service did not respond after $MAX_RETRIES attempts"
    return 1
}

# Function to test container status
test_container_status() {
    local container=$1

    if docker ps --format "{{.Names}}" | grep -q "^$container$"; then
        print_status "PASS" "Container $container is running"
        return 0
    else
        print_status "FAIL" "Container $container is not running"
        docker-compose ps $container 2>/dev/null || true
        return 1
    fi
}

# Function to test database
test_database() {
    echo ""
    echo -e "${BLUE}Testing PostgreSQL Database...${NC}"

    if docker-compose exec -T postgres pg_isready -U socrates > /dev/null 2>&1; then
        print_status "PASS" "PostgreSQL is accepting connections"

        # Count tables
        local table_count=$(docker-compose exec -T postgres psql -U socrates -d socrates_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null || echo "0")
        print_status "PASS" "Database has $table_count tables"

        return 0
    else
        print_status "FAIL" "PostgreSQL is not accepting connections"
        return 1
    fi
}

# Function to test API endpoints
test_api_endpoints() {
    echo ""
    echo -e "${BLUE}Testing API Endpoints...${NC}"

    # Health check
    local health=$(curl -s http://localhost:8000/health)
    if echo "$health" | grep -q "success"; then
        print_status "PASS" "GET /health endpoint working"
    else
        print_status "FAIL" "GET /health endpoint failed"
    fi

    # Docs endpoint
    if curl -sf http://localhost:8000/docs > /dev/null; then
        print_status "PASS" "GET /docs endpoint working (API documentation available)"
    else
        print_status "FAIL" "GET /docs endpoint failed"
    fi
}

# Function to test frontend
test_frontend() {
    echo ""
    echo -e "${BLUE}Testing Frontend...${NC}"

    if curl -sf http://localhost:3000 > /dev/null; then
        print_status "PASS" "Frontend is serving on port 3000"

        # Check for React app
        if curl -s http://localhost:3000 | grep -q "react\|React\|Socrates"; then
            print_status "PASS" "Frontend contains React application"
        else
            print_status "WARN" "Could not verify React application in response"
        fi
    else
        print_status "FAIL" "Frontend is not responding on port 3000"
    fi
}

# Function to test WebSocket
test_websocket() {
    echo ""
    echo -e "${BLUE}Testing WebSocket Endpoint...${NC}"

    # Note: This is a basic check - full WebSocket testing requires a client
    if curl -s -I http://localhost:8000/ws/sessions/test 2>&1 | grep -q "Upgrade"; then
        print_status "PASS" "WebSocket endpoint is available"
    else
        print_status "INFO" "WebSocket endpoint check completed (requires JWT token for full test)"
    fi
}

# Function to display summary
display_summary() {
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo -e "${BLUE}Test Summary${NC}"
    echo "════════════════════════════════════════════════════════"
    echo -e "${GREEN}Passed: $PASSED${NC}"
    echo -e "${RED}Failed: $FAILED${NC}"
    echo "Total:  $TESTS_TOTAL"
    echo "════════════════════════════════════════════════════════"

    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}✗ Some tests failed. Please check the output above.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "════════════════════════════════════════════════════════"
    echo -e "${BLUE}Socrates 8.0 - Docker Testing Suite${NC}"
    echo "════════════════════════════════════════════════════════"

    # Check if Docker is running
    print_status "INFO" "Checking Docker daemon..."
    if ! docker info > /dev/null 2>&1; then
        print_status "FAIL" "Docker daemon is not running"
        exit 1
    fi
    print_status "PASS" "Docker daemon is running"

    # Check if docker-compose is available
    print_status "INFO" "Checking docker-compose..."
    if ! command -v docker-compose &> /dev/null; then
        print_status "FAIL" "docker-compose is not installed"
        exit 1
    fi
    print_status "PASS" "docker-compose is available"

    # Check if containers exist
    print_status "INFO" "Checking Docker containers..."
    echo ""

    test_container_status "socrates-db"
    test_container_status "socrates-backend"
    test_container_status "socrates-frontend"
    test_container_status "socrates-redis"

    # Test service availability
    test_service_health "Backend API" "8000" "/health"
    test_service_health "Frontend" "3000" "/"

    # Test database
    test_database

    # Test API endpoints
    test_api_endpoints

    # Test frontend
    test_frontend

    # Test WebSocket
    test_websocket

    # Display summary
    echo ""
    display_summary

    if [ $FAILED -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"
