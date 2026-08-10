# Local development

What each intern needs on their machine. Inference itself runs on the on-prem
GPU server — you point your local backend at it.

## Prerequisites

- **Python 3.11+** and [uv](https://docs.astral.sh/uv/) — backend
- **Node 20+** — frontend
- **Docker Desktop** — local n8n (and Langfuse if you run it locally)
- Network access to the on-prem AI server (vLLM ports 8001/8002)

## Backend

```bash
cp .env.example .env    # set LLM_BASE_URL / EMBED_BASE_URL to the GPU server
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Smoke test: `curl http://localhost:8000/api/health` and
`curl http://localhost:8000/api/agents`.

## Frontend

```bash
cd frontend
npm install
npm run dev    # http://localhost:3000
```

## Local n8n

The server-hosted n8n exists, but development happens on your own local
instance so you can break things safely.

```bash
docker compose up n8n    # http://localhost:5678
```

What you need for local n8n work:

1. **First run:** create your local owner account (local instance, local data —
   it is not connected to the server one).
2. **Credentials** are stored per-instance. Add your own dev credentials for
   LINE OA / Notion / SMTP locally; never commit them. Real credentials live
   only on the server instance.
3. **Incoming webhooks (LINE OA)** can't reach your laptop directly — use a
   tunnel while testing: `ngrok http 5678` or `cloudflared tunnel --url
   http://localhost:5678`, and point the LINE webhook at the tunnel URL.
4. **Reaching your local backend from the n8n container:** use
   `http://host.docker.internal:8000`, not `localhost`.
5. **Sync via the repo:** export finished workflows as JSON into
   `n8n/workflows/` and commit; import that JSON into the server-hosted n8n
   when promoting. See [../n8n/README.md](../n8n/README.md).

## Langfuse

Self-host via the official compose (we map its UI to port 3001):

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse && docker compose up
```

Create an org + project in the UI, copy the public/secret keys into `.env`
(`LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_HOST`). If the keys
are empty, the backend simply skips tracing — nothing breaks.

## Running vLLM yourself (optional)

Only relevant on a machine with an NVIDIA GPU (not a Mac):

```bash
docker compose --profile serving up
```

Models are set via `LLM_MODEL` / `EMBED_MODEL` in `.env`.
