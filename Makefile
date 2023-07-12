.PHONY: init init_node init_poetry python start

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


# Server

start:
	@poetry --quiet run python ./cibo
