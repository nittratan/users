.PHONY: install install-dev run test lint format docker-build docker-up docker-down

install:
	python3 -m pip install -r requirements.txt

install-dev:
	python3 -m pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

docker-build:
	docker build -t user-api:local .

docker-up:
	docker compose up --build

docker-down:
	docker compose down

