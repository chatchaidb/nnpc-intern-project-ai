# n8n workflows

n8n handles channel & tool integrations (LINE OA, email, Notion) and the
human-approval workflows. It calls the FastAPI backend for anything that needs
the LLM — n8n itself never talks to vLLM directly.

## Instances

- **Server-hosted** — the real instance with real credentials. Promotion target.
- **Local (Docker)** — each developer's sandbox: `docker compose up n8n`
  (port 5678). Setup details in [../docs/local-dev.md](../docs/local-dev.md).

## Workflow sync

The repo is the source of truth for workflow definitions:

1. Build and test on your local instance.
2. Export the workflow as JSON (Workflow menu → Download) into `workflows/`,
   named `<area>-<purpose>.json` (e.g. `cs-line-inbound.json`).
3. Commit. To promote, import that JSON into the server-hosted instance and
   re-attach server credentials.

**Never export credentials.** n8n exports reference credentials by name only —
keep it that way, and recreate credentials by hand on each instance.

## Conventions

- Every outbound send (LINE push, email) must pass through an explicit approval
  step during MVP — no workflow may go webhook → LLM → send directly.
- Call the local backend from the n8n container via
  `http://host.docker.internal:8000`.

## Current workflows (RAG prototype)

Two exported workflows live in this folder. They are the working CS prototype
and they call Ollama and Qdrant **directly**, not through the FastAPI backend —
so they do not follow the "n8n never talks to the model directly" convention
above. Treat that convention as describing the intended end state, not today.

- **`nnpc-ingestion-v2.json`** — manual trigger. Reads `.txt` files from an
  inbox folder, chunks them (400/50), embeds with `qwen3-embedding:latest`, and
  inserts into the Qdrant collection `nnpc_docs` tagged `tenant: nnpc`.
- **`nnpc-cs-v5.json`** — chat/webhook in → normalize → AI agent (Typhoon2,
  temperature 0.2) with `nnpc_docs` as a retrieval tool → escalation check →
  reply. Tenant is read from the request and used as a Qdrant filter.

### Credentials to create by hand

n8n exports reference credentials by name only, so on each instance create:
Ollama (chat + embeddings), Qdrant, and — only if you enable the disabled nodes
below — Postgres and Gmail.

### Nodes that ship disabled

`Gmail Approval`, `Log Approval`, and `Log Escalation` are exported with
`disabled: true`. **With them disabled, drafts flow straight to the reply
marked `status: approved` without any human seeing them.** Enable the Gmail node
and set a real approver address before this touches a customer. The approver
address is a placeholder in the export — replace it locally, never commit one.
