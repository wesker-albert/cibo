#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

npm install
mv /home/vscode/cibo/node_modules /home/vscode/
export PATH=/home/vscode/node_modules/.bin:$PATH

poetry config virtualenvs.create false
poetry install