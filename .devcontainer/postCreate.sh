#!/bin/bash

# install useful zsh plugins
git clone https://github.com/marlonrichert/zsh-autocomplete.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autocomplete
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/jirutka/zsh-shift-select.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-shift-select
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
sed -i "s/plugins=(git)/plugins=(git zsh-autocomplete zsh-autosuggestions zsh-shift-select zsh-syntax-highlighting)/g" ~/.zshrc
exec zsh

# disable the creation of __pycache__ dirs
echo -e "export PYTHONDONTWRITEBYTECODE=1" >> ~/.zshrc

# install node dependencies
npm install
# move the node_modules dir up one level
mv /home/vscode/cibo/node_modules /home/vscode/
# add modules to PATH
echo -e "export PATH=/home/vscode/node_modules/.bin:$PATH" >> ~/.zshrc

# disable poetry venv creation
poetry config virtualenvs.create false
# install python dependencies
poetry install