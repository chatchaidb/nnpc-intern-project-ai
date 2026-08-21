# NNPC Intern Project — AI Agents Team

A self-operating AI agent team for **NNPC** (consulting) and **Chin Chun**
(manufacturing/trading), built in a three-month intern program. MVP: four agents
— Customer Service, Marketing, Sales, Finance — behind an orchestrator, with
human-review gates on everything outbound.

Full context: [docs/project-overview.md](docs/project-overview.md) ·
Architecture: [docs/architecture.md](docs/architecture.md) ·
Local setup: [docs/local-dev.md](docs/local-dev.md)

## Stack

| Layer | Choice |
|---|---|
| LLM serving | Ollama on the on-prem AI server — `scb10x/llama3.1-typhoon2-8b-instruct:latest`. vLLM also runs on the server (`:8010`) serving the same Typhoon model |
| Embeddings | `qwen3-embedding:latest` via Ollama |
| Vector DB | Qdrant — in use. Dev collection `nnpc_docs` (tenant-tagged); the server's `nnpc_kb` is empty and currently unused |
| Backend | FastAPI (`backend/`) |
| Frontend | Next.js (`frontend/`) |
| Workflows / integrations | n8n (`n8n/`) — LINE OA, email, Notion, human-approval flows |
| Observability | Langfuse (self-hosted, official compose) |

## Repository layout

```
backend/    FastAPI app — agents, LLM & embedding clients, Langfuse tracing
frontend/   Next.js internal chat UI with agent selector
n8n/        Exported n8n workflow JSON + local setup notes
docs/       Project overview, architecture, local dev guide
docker-compose.yml   vLLM serving (GPU server) + local n8n
```

## Quickstart

```bash
cp .env.example .env          # then fill in values

# Backend (Python 3.11+, uv)
cd backend && uv sync && uv run uvicorn app.main:app --reload   # :8000

# Frontend (Node 20+)
cd frontend && npm install && npm run dev                        # :3000

# Local n8n
docker compose up n8n                                            # :5678

# vLLM (on the GPU server only)
docker compose --profile serving up
```

## Ports

| Service | Port |
|---|---|
| FastAPI backend | 8000 |
| Ollama — chat + embeddings (server) | 11434 |
| vLLM — chat (server) | 8010 |
| Qdrant | 6333 |
| Next.js frontend | 3000 |
| Langfuse | 3001 |
| n8n | 5678 |

## Ground rules

- **Human-in-the-loop:** no outbound message, payment, or quotation leaves
  without human approval during MVP.
- **Data stays on-prem:** all inference runs on NNPC's own AI server.
- **Finance Agent never executes payments** — drafts and reminders only.
- Cross-repo knowledge (decisions, features, bugs, ops) lives in the
  `nnpc-obsidian` vault, not here.
