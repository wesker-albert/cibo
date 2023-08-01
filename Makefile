.PHONY: init init_node init_poetry python lint formatting test coverage safety_check \
	start

.DEFAULT_GOAL := init


# Container

init: init_node init_poetry

init_node: package-lock.json

init_poetry: ../.poetry_check

package-lock.json: package.json
	npm install
	@rm -rf /home/vscode/node_modules
	@mv /home/vscode/cibo/node_modules /home/vscode/
	@touch $@

poetry.lock: pyproject.toml
	poetry lock
	@touch $@

../.poetry_check: poetry.lock
	poetry install
	@touch $@


# Development

python:
	@poetry --quiet run python

test_verbose:
	@poetry run pytest --durations=5 -vv


# Quality Control

safety_check:
	@poetry export --without-hashes --with dev -o requirements.txt && cat requirements.txt \
		| poetry run safety check --stdin --full-report && poetry check -n

lint:
	@poetry run pylint ./cibo ./tests

type_check:
	@poetry run mypy

formatting:
	@poetry run black --diff --check ./cibo ./tests

test:
	@poetry run pytest --durations=5

coverage:
	@poetry run pytest --cov-report term --cov-report xml:coverage.xml --cov=cibo


# Server

start:
	@poetry --quiet run python ./cibo
