# Makefile for development and testing

.PHONY: help install install-dev test test-watch test-coverage test-coverage-xml test-coverage-html lint lint-fix format format-check security type-check quality build upload upload-test dev-setup clean ci dev release-check

# Default target
help: ## Show this help message
	@echo "Project Development Makefile"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation targets
install: ## Install the package and all dependencies
	uv add financial-indicators

install-dev: ## Install development dependencies (Includes testing and quality tools)
	uv sync --extra dev

# Testing targets
test: ## Run full test suite. Requires all dependencies. Use `make test m=marker_name` to filter by markers.
	@if [ -n "$(m)" ]; then \
		echo "Running tests with marker: $(m)"; \
		uv run pytest -m "$(m)" -v --tb=short; \
	else \
		echo "Running all tests"; \
		uv run pytest -v --tb=short; \
	fi

test-watch: ## Run tests in watch mode
	uv run pytest-watch --onpass "echo 'Tests passed'" --onfail "echo 'Tests failed'" -- -v --tb=short 

test-coverage: ## Run tests with coverage
	uv run pytest --cov=src/financial_indicators --cov-branch --cov-report=term-missing --cov-fail-under=80
	@echo "Coverage report generated. Check the terminal output for details."

test-coverage-xml: ## Run tests with coverage and generate XML report
	uv run pytest --cov=src/financial_indicators --cov-branch --cov-report=xml:coverage.xml --cov-fail-under=80
	@echo "Coverage report generated at coverage.xml"

test-coverage-html: ## Run tests with coverage and generate HTML report
	uv run pytest --cov=src/financial_indicators --cov-branch --cov-report=html:coverage_html_report --cov-fail-under=80
	@echo "HTML coverage report generated at coverage_html_report/index.html"

# Code quality targets
lint: ## Run linting
	uv run ruff check src/ tests/

lint-fix: ## Run linting with auto-fix
	uv run ruff check src/ tests/ --fix

format: ## Format code
	uv run ruff format src/ tests/

format-check: ## Check code formatting
	uv run ruff format src/ tests/ --check

security: ## Run security analysis
	uv run bandit -r src/

type-check: ## Run type checking. mypy is optional, so it will not fail if mypy is not installed.
	@if uv run python -c "import mypy" 2>/dev/null; then \
		echo "Running mypy type check..."; \
		uv run mypy src/ --ignore-missing-imports || true; \
	else \
		echo "mypy not installed, skipping type check"; \
		echo "Install mypy for type checking: uv add --dev mypy"; \
	fi

quality: lint format-check security type-check ## Run all quality checks

# Build and distribution
build: ## Build the package
	uv build

upload: ## Upload to PyPI
	uv publish

upload-test: ## Upload to Test PyPI
	uv publish --index testpypi

# Development targets
dev-setup: install-dev ## Set up development environment
	@echo "Development environment set up!"
	@echo "Run 'make test-fast' to run quick tests"
	@echo "Run 'make test' to run full test suite"

clean: ## Clean up build artifacts and cache
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf coverage_html_report/
	rm -f .coverage
	rm -f coverage.xml
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# CI simulation
ci: quality test-coverage ## Run CI-like checks locally

# Quick development workflow
dev: install-dev lint test ## Quick development workflow: install, lint, test

# Release workflow
release-check: quality test build ## Pre-release checks
	@echo "✅ Release checks passed!"
	@echo "   Run 'make upload-test' to upload to Test PyPI"
	@echo "   Run 'make upload' to upload to PyPI"
