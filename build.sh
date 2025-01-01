#!/bin/bash
set -e

# Install pygame-wasm
pip install pygame-wasm

# Compile the game to WebAssembly
python -m pygame_wasm.pack src/game.py -o public/game.js