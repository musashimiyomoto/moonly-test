# Minimal Stateless Chatbot with LangGraph & Ollama

This is a minimal stateless chatbot using [LangGraph](https://github.com/langchain-ai/langgraph) and a free local model via [Ollama](https://ollama.com/). It supports a single tool: `get_current_time`.

## Requirements
- Linux or WSL2
- Python 3.8+
- [Ollama](https://ollama.com/) (will be installed automatically if missing)

## Quickstart

Just run:
```bash
bash run.sh [<model_name>]
```

The script will:
- Install Ollama if needed
- Pull the specified model (default: `qwen3:0.6b`, or any other from the [Ollama library](https://ollama.com/library) if you provide its name)
- Set up a Python virtual environment
- Install dependencies
- Start the LangGraph dev server

After the server starts, open: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

**Examples:**
- Default model:
  ```bash
  bash run.sh
  ```
- Custom model:
  ```bash
  bash run.sh llama3:8b
  ```

---

For manual setup or troubleshooting, see the contents of `run.sh`.
