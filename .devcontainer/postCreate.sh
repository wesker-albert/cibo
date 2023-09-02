#!/bin/bash

# install useful zsh plugins
# git clone https://github.com/marlonrichert/zsh-autocomplete.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autocomplete
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/jirutka/zsh-shift-select.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-shift-select
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions zsh-shift-select zsh-syntax-highlighting)/g" ~/.zshrc

# redirect the creation of __pycache__ dirs to tmp
echo -e "export PYTHONPYCACHEPREFIX=/tmp" >> ~/.zshrc

# disable poetry venv creation
poetry config virtualenvs.create false
# install python dependencies
poetry install
