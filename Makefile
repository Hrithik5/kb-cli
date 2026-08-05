.PHONY: install dev-install test lint format clean help

help:
	@echo "Usage:"
	@echo "  make install      Install kb package locally"
	@echo "  make dev-install  Install kb package in editable mode with dev dependencies"
	@echo "  make test         Run test suite with pytest"
	@echo "  make lint         Run ruff linter"
	@echo "  make format       Run ruff code formatter"
	@echo "  make clean        Remove build artifacts and caches"

install:
	python3 -m pip install .

dev-install:
	python3 -m pip install -e ".[dev]"

test:
	pytest -v --cov=kb tests/

lint:
	ruff check .

format:
	ruff format .

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
