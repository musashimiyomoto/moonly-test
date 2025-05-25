# Minimal Stateless Chatbot with LangGraph & Ollama

This is a minimal stateless chatbot using [LangGraph](https://github.com/langchain-ai/langgraph) and a free local model via [Ollama](https://ollama.com/). It supports a single tool: `get_current_time`.

## Quickstart

1. **Install Ollama** ([instructions](https://ollama.com/download))
2. **Pull the smallest free model** (qwen3:0.6b):
   ```bash
   ollama pull qwen3:0.6b
   ```
3. **Clone and set up the repo:**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   langgraph dev
   ```

## One-liner for setup (Linux):
```bash
curl -fsSL https://ollama.com/install.sh | sh && ollama pull phi3 && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && langgraph dev
```
