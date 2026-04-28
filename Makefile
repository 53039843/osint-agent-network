.PHONY: help install dev test lint format run worker docker-up docker-down db-upgrade

help:
	@echo "OSINT Agent Network Makefile Commands:"
	@echo "  install      Install production dependencies"
	@echo "  dev          Install development dependencies"
	@echo "  test         Run test suite with pytest"
	@echo "  lint         Run flake8 and mypy"
	@echo "  format       Format code with black"
	@echo "  run          Start FastAPI development server"
	@echo "  worker       Start Celery worker"
	@echo "  docker-up    Start all services via docker-compose"
	@echo "  docker-down  Stop all docker services"
	@echo "  db-upgrade   Run Alembic database migrations"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=core --cov=agents

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy core/ agents/

format:
	black .

run:
	uvicorn app:app --host 0.0.0.0 --port 8000 --reload

worker:
	celery -A worker.tasks worker --loglevel=info

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

db-upgrade:
	alembic upgrade head
