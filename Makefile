.PHONY: help venv install install-catalog install-orders test test-catalog test-orders lint lint-catalog lint-orders bandit bandit-catalog bandit-orders audit security run-catalog run-orders clean clean-venv

SYSTEM_PYTHON ?= python3
VENV ?= $(CURDIR)/.venv
PYTHON ?= $(VENV)/bin/python
PIP := $(PYTHON) -m pip

CATALOG_DIR := services/catalog-service
ORDERS_DIR := services/orders-service

help:
	@echo "SecureCommerce DevOps commands"
	@echo ""
	@echo "Setup:"
	@echo "  make venv             Create local Python virtual environment"
	@echo "  make install          Install runtime and dev dependencies"
	@echo ""
	@echo "Quality:"
	@echo "  make test             Run all unit tests"
	@echo "  make lint             Run Ruff lint checks"
	@echo "  make bandit           Run Bandit security scans"
	@echo "  make audit            Run pip-audit dependency scans"
	@echo "  make security         Run Bandit and pip-audit"
	@echo ""
	@echo "Local runtime:"
	@echo "  make run-catalog      Run catalog-service on port 8001"
	@echo "  make run-orders       Run orders-service on port 8002"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove Python cache/test cache files"
	@echo "  make clean-venv       Remove local virtual environment"

venv:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv install-catalog install-orders

install-catalog:
	$(PIP) install -r $(CATALOG_DIR)/requirements.txt
	$(PIP) install -r $(CATALOG_DIR)/requirements-dev.txt

install-orders:
	$(PIP) install -r $(ORDERS_DIR)/requirements.txt
	$(PIP) install -r $(ORDERS_DIR)/requirements-dev.txt

test: test-catalog test-orders

test-catalog:
	cd $(CATALOG_DIR) && $(PYTHON) -m pytest -v

test-orders:
	cd $(ORDERS_DIR) && $(PYTHON) -m pytest -v

lint: lint-catalog lint-orders

lint-catalog:
	cd $(CATALOG_DIR) && $(PYTHON) -m ruff check .

lint-orders:
	cd $(ORDERS_DIR) && $(PYTHON) -m ruff check .

bandit: bandit-catalog bandit-orders

bandit-catalog:
	cd $(CATALOG_DIR) && $(PYTHON) -m bandit -r app

bandit-orders:
	cd $(ORDERS_DIR) && $(PYTHON) -m bandit -r app

audit:
	$(PYTHON) -m pip_audit -r $(CATALOG_DIR)/requirements.txt
	$(PYTHON) -m pip_audit -r $(ORDERS_DIR)/requirements.txt

security: bandit audit

run-catalog:
	cd $(CATALOG_DIR) && $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

run-orders:
	cd $(ORDERS_DIR) && CATALOG_SERVICE_URL=http://localhost:8001 $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +

clean-venv:
	rm -rf $(VENV)
