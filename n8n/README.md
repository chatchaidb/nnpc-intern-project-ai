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
