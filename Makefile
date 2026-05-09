run:
	poetry run python -m app.main

check:
	poetry run mypy src
	poetry run ruff check src

format:
	poetry run ruff format src

ui: 
	poetry run pyside6-designer