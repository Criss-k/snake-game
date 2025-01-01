#!/bin/bash
set -e

# Install Python using pyenv if not already available
if ! command -v python3 &> /dev/null; then
  echo "Python not found. Installing Python..."
  curl https://pyenv.run | bash
  export PATH="$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH"
  pyenv install 3.9.7  # Use a specific Python version
  pyenv global 3.9.7
fi

# Install pip if missing
if ! command -v pip &> /dev/null; then
  echo "pip not found. Installing pip..."
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python3 get-pip.py
  rm get-pip.py
fi

# Install pygame-wasm
pip install pygame-wasm

# Build the game to WebAssembly
python3 -m pygame_wasm.pack src/game.py -o public/game.js
