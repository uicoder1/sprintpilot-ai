.PHONY: install playground run test lint

install:
	uv sync

playground:
	uv run adk web . --host 127.0.0.1 --port 18081 --no-reload

run:
	uv run uvicorn app.fast_api_app:app --host 127.0.0.1 --port 8000

test:
	uv run pytest tests/unit tests/integration

lint:
	uv run ruff check .
