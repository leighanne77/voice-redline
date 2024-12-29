.PHONY: translations backend frontend all

# Backend commands
translations-setup:
	python scripts/setup_translations.py

test-backend:
	pytest tests/

lint-python:
	flake8 .
	black .

# Frontend commands (calls npm scripts)
frontend-build:
	npm run build

frontend-test:
	npm run test:extension

# Combined commands
all-tests: test-backend frontend-test

install:
	pip install -r requirements.txt
	npm install 