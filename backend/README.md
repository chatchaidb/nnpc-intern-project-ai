# Backend

FastAPI app that owns the agents: system prompts, LLM calls to vLLM
(OpenAI-compatible), bge-m3 embeddings, and Langfuse tracing.

```bash
uv sync
uv run uvicorn app.main:app --reload    # http://localhost:8000
uv run pytest                           # tests
```

Configuration comes from `.env` at the repo root (see `../.env.example`).

## Endpoints

| Route | Purpose |
|---|---|
| `GET /api/health` | Liveness + which model is configured |
| `GET /api/agents` | List available agents |
| `POST /api/chat` | `{agent, messages}` → agent's draft reply |
| `POST /api/embed` | `{texts}` → bge-m3 embeddings (for KB experiments) |

## Layout

```
app/config.py    Settings from environment
app/agents.py    Agent registry — names + system prompts
app/llm.py       Chat client (Langfuse-wrapped when keys are set)
app/embeddings.py  Embedding client
app/routers/     HTTP layer
```
