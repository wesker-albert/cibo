ARG VARIANT=3.11-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG NODE_VER=16
RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VER} 2>&1"

RUN pip3 install pipx

ARG POETRY_VER=1.4.2
RUN su vscode -c "pipx install poetry==${POETRY_VER}"
