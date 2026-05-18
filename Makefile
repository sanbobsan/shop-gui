run:
	poetry run python -m app.main

run-web:
	poetry run flet run src/app/main.py --web --port 8000

check:
	poetry run mypy src
	poetry run ruff check src

format:
	poetry run ruff check --select I --fix
	poetry run ruff format src