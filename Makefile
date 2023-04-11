.PHONY: init init_node init_poetry

.DEFAULT_GOAL := init

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