#!/bin/bash

set -e

if ! command -v ollama &> /dev/null; then
  echo "Ollama not found. Installing..."
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "Ollama already installed."
fi

MODEL_NAME=${MODEL_NAME:-${1:-qwen3:0.6b}}

export MODEL_NAME

ollama pull "$MODEL_NAME"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Starting langgraph dev..."
langgraph dev

exec $cmd
