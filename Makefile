.PHONY: init init_node init_poetry python start_server

.DEFAULT_GOAL := init


# Container

init: init_node init_poetry

init_node: package-lock.json

init_poetry: poetry.lock
	poetry install

package-lock.json: package.json
	npm install
	rm -rf /home/vscode/node_modules
	@mv /home/vscode/cibo/node_modules /home/vscode/
	@touch $@

poetry.lock: pyproject.toml
	poetry lock
	@touch $@


# Development

python:
	poetry run python


# Server

start:
	poetry run python ./cibo/server.py