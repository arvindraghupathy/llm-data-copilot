run:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest -q

lint:
	poetry run ruff check .

typecheck:
	poetry run mypy app
