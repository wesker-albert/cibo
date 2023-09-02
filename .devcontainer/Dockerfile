ARG VARIANT=3.11-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG PIPX_VER=1.2.0
RUN pip3 install pipx==${PIPX_VER}

ARG POETRY_VER=1.5.1
RUN su vscode -c "pipx install poetry==${POETRY_VER}"
