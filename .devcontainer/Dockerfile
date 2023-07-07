ARG VARIANT=3.11-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG NODE_VER=16
RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VER} 2>&1"

ARG NPM_VER=9.7.2
RUN su vscode -c "npm install -g npm@${NPM_VER}"

ARG PIPX_VER=1.2.0
RUN pip3 install pipx==${PIPX_VER}

ARG POETRY_VER=1.5.1
RUN su vscode -c "pipx install poetry==${POETRY_VER}"
