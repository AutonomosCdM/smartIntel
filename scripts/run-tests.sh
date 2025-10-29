#!/usr/bin/env bash

# ProcureGenius Test Runner
# Usage: ./scripts/run-tests.sh [unit|integration|all] [--watch]

set -euo pipefail

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

# Parse arguments
TEST_TYPE="${1:-all}"
WATCH_MODE="${2:-}"

echo -e "${BLUE}ProcureGenius Test Runner${NC}"
echo ""

# Function to run tests
run_tests() {
    local test_path=$1
    local markers=$2

    echo -e "${YELLOW}→ Running ${TEST_TYPE} tests...${NC}"

    PYTEST_ARGS=(
        "$test_path"
        "-v"
        "--cov=src"
        "--cov-report=term-missing"
        "--cov-report=html"
        "--cov-report=xml"
    )

    if [ -n "$markers" ]; then
        PYTEST_ARGS+=("-m" "$markers")
    fi

    if pytest "${PYTEST_ARGS[@]}"; then
        echo ""
        echo -e "${GREEN}✓ Tests passed${NC}"
        echo -e "${BLUE}Coverage report: htmlcov/index.html${NC}"
        return 0
    else
        echo ""
        echo -e "${RED}✗ Tests failed${NC}"
        return 1
    fi
}

# Run tests based on type
case "$TEST_TYPE" in
    unit)
        run_tests "tests/unit/" "unit"
        ;;
    integration)
        run_tests "tests/integration/" "integration"
        ;;
    all)
        run_tests "tests/" ""
        ;;
    *)
        echo -e "${RED}Invalid test type: $TEST_TYPE${NC}"
        echo "Usage: $0 [unit|integration|all] [--watch]"
        exit 1
        ;;
esac

# Watch mode (if requested)
if [ "$WATCH_MODE" == "--watch" ]; then
    echo ""
    echo -e "${YELLOW}→ Entering watch mode (Ctrl+C to exit)...${NC}"
    pytest-watch -- "${PYTEST_ARGS[@]}"
fi
