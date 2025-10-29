#!/usr/bin/env bash

# ProcureGenius Local Development Setup
# Usage: ./scripts/local-setup.sh

set -euo pipefail

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}ProcureGenius - Local Development Setup${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}→ Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if [[ ! "$PYTHON_VERSION" =~ ^3\.(11|12) ]]; then
    echo -e "${RED}✗ Python 3.11+ required (found: $PYTHON_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo -e "${YELLOW}→ Creating virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
    read -p "Remove and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        python3 -m venv .venv
    fi
else
    python3 -m venv .venv
fi
echo -e "${GREEN}✓ Virtual environment ready${NC}"

# Activate virtual environment
echo -e "${YELLOW}→ Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}→ Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel --quiet

# Install dependencies
echo -e "${YELLOW}→ Installing dependencies...${NC}"
pip install -e ".[dev]" --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Setup pre-commit hooks
echo -e "${YELLOW}→ Installing pre-commit hooks...${NC}"
pre-commit install
echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"

# Create .env file
echo -e "${YELLOW}→ Setting up environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cp config/.env.example .env
    echo -e "${GREEN}✓ Created .env file (edit with your credentials)${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists (skipped)${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}→ Creating data directories...${NC}"
mkdir -p data/{raw,processed,predictions}
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/predictions/.gitkeep
echo -e "${GREEN}✓ Data directories ready${NC}"

# Run initial tests
echo -e "${YELLOW}→ Running initial tests...${NC}"
if pytest tests/unit/ -q 2>/dev/null; then
    echo -e "${GREEN}✓ Tests passed${NC}"
else
    echo -e "${YELLOW}⚠ No tests found yet (expected for new project)${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Activate virtual environment:"
echo "     ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo "  2. Configure your credentials in .env:"
echo "     ${YELLOW}vim .env${NC}"
echo ""
echo "  3. Run tests:"
echo "     ${YELLOW}make test${NC}"
echo ""
echo "  4. Start development:"
echo "     ${YELLOW}make run-dev${NC}"
echo ""
echo -e "${BLUE}For help:${NC}"
echo "     ${YELLOW}make help${NC}"
echo ""
