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

## Using Other Ollama Models

You can use any model from the [Ollama library](https://ollama.com/library) by specifying its name when running the script:

```bash
bash run.sh <model_name>
```

For example, to use the `llama3:8b` model, run:

```bash
bash run.sh llama3:8b
```

If no model name is provided, the default is `qwen3:0.6b`.
