.PHONY: check lint format format-check fix

check: lint format-check

lint:
	python -m ruff check .

format:
	python -m ruff format .

format-check:
	python -m ruff format --check .

fix:
	python -m ruff check --fix .
