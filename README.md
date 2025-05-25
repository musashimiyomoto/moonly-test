# Minimal Stateless Chatbot with LangGraph & Ollama

This is a minimal stateless chatbot using [LangGraph](https://github.com/langchain-ai/langgraph) and a free local model via [Ollama](https://ollama.com/). It supports a single tool: `get_current_time`.

## Requirements
- Linux or WSL2
- Python 3.8+
- [Ollama](https://ollama.com/) (will be installed automatically if missing)

## Quickstart

Just run:
```bash
bash run.sh
```

The script will:
- Install Ollama if needed
- Pull the required model (`qwen3:0.6b`)
- Set up a Python virtual environment
- Install dependencies
- Start the LangGraph dev server

After the server starts, open: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

---

For manual setup or troubleshooting, see the contents of `run.sh`.
