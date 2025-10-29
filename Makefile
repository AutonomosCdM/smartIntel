.PHONY: help setup install install-dev clean test test-unit test-integration lint format type-check pre-commit run-dev deploy-staging deploy-production

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)ProcureGenius - IBM Hackathon$(NC)"
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

setup: ## Initial project setup (create venv, install dependencies, pre-commit)
	@echo "$(BLUE)Setting up ProcureGenius development environment...$(NC)"
	python3.11 -m venv .venv
	.venv/bin/pip install --upgrade pip setuptools wheel
	$(MAKE) install-dev
	.venv/bin/pre-commit install
	cp -n config/.env.example .env 2>/dev/null || true
	@echo "$(GREEN)✓ Setup complete! Activate with: source .venv/bin/activate$(NC)"

install: ## Install production dependencies
	@echo "$(BLUE)Installing production dependencies...$(NC)"
	pip install -e .
	@echo "$(GREEN)✓ Production dependencies installed$(NC)"

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	pip install -e ".[dev]"
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

clean: ## Clean build artifacts, cache, and temporary files
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ .coverage htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

test: ## Run all tests
	@echo "$(BLUE)Running test suite...$(NC)"
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Tests complete. Coverage report: htmlcov/index.html$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest tests/unit/ -v -m unit
	@echo "$(GREEN)✓ Unit tests complete$(NC)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest tests/integration/ -v -m integration
	@echo "$(GREEN)✓ Integration tests complete$(NC)"

lint: ## Run ruff linter
	@echo "$(BLUE)Running ruff linter...$(NC)"
	ruff check src/ tests/
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff format src/ tests/
	ruff check --fix src/ tests/
	@echo "$(GREEN)✓ Code formatted$(NC)"

type-check: ## Run mypy type checker
	@echo "$(BLUE)Running type checks...$(NC)"
	mypy src/
	@echo "$(GREEN)✓ Type checking complete$(NC)"

pre-commit: ## Run all pre-commit hooks
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit checks complete$(NC)"

verify: lint type-check test ## Run all verification checks (lint + type-check + test)
	@echo "$(GREEN)✓ All verification checks passed$(NC)"

run-dev: ## Run development server (placeholder for future)
	@echo "$(BLUE)Starting development environment...$(NC)"
	@echo "$(YELLOW)⚠ Not implemented yet - add your dev server command here$(NC)"

deploy-staging: ## Deploy to staging environment
	@echo "$(BLUE)Deploying to staging...$(NC)"
	./scripts/deploy-staging.py
	@echo "$(GREEN)✓ Staging deployment complete$(NC)"

deploy-production: ## Deploy to production (manual gate)
	@echo "$(RED)⚠ Production deployment requires manual approval$(NC)"
	@echo "$(YELLOW)Use GitHub Actions workflow: production-gate.yml$(NC)"

watch-tests: ## Watch tests and re-run on file changes
	@echo "$(BLUE)Watching for file changes...$(NC)"
	pytest-watch -- tests/ -v

jupyter: ## Start Jupyter notebook server
	@echo "$(BLUE)Starting Jupyter notebook server...$(NC)"
	jupyter notebook notebooks/

docs: ## Generate documentation (placeholder)
	@echo "$(BLUE)Generating documentation...$(NC)"
	@echo "$(YELLOW)⚠ Not implemented yet - add sphinx/mkdocs command here$(NC)"

requirements: ## Generate requirements.txt from pyproject.toml
	@echo "$(BLUE)Generating requirements.txt...$(NC)"
	pip freeze > requirements.txt
	@echo "$(GREEN)✓ requirements.txt generated$(NC)"

security-check: ## Run security vulnerability scan
	@echo "$(BLUE)Running security checks...$(NC)"
	pip-audit
	@echo "$(GREEN)✓ Security scan complete$(NC)"

.DEFAULT_GOAL := help
