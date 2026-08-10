# Architecture

One architecture, two companies: the same agent templates with swapped knowledge
bases and tool configs. Validate at NNPC first, then replicate to Chin Chun.

```
Users / internal staff
      │
▌Orchestrator Agent▌── task routing, cross-agent coordination, human-review gates
      │
 ├─ Customer Service Agent
 ├─ Marketing Agent
 ├─ Sales Agent
 └─ Finance Agent
      │
▌Shared layer▌── knowledge base (Notion docs / FAQ / product data),
                 tool integrations (Email / LINE OA / CRM / accounting) via n8n,
                 logging & monitoring via Langfuse
```

## Components

| Component | Where it runs | Port | Notes |
|---|---|---|---|
| vLLM — chat model | On-prem AI server (GPU) | 8001 | Typhoon2-8B or Qwen2.5, OpenAI-compatible API |
| vLLM — embeddings | On-prem AI server (GPU) | 8002 | `BAAI/bge-m3`, `--task embed` |
| FastAPI backend | server / local dev | 8000 | Agent definitions, LLM & embedding clients, Langfuse tracing |
| Next.js frontend | server / local dev | 3000 | Internal chat UI with agent selector |
| n8n | server (hosted) + local (dev) | 5678 | Channel & tool integrations, human-approval workflows; calls the backend API |
| Langfuse | self-hosted | 3001 | Traces every LLM call; official docker compose |

## Request flow (MVP)

1. A channel event arrives (LINE OA message, web form, email) → n8n webhook.
2. n8n calls the backend `POST /api/chat` with the agent key and conversation.
3. Backend builds the agent's system prompt, calls vLLM, traces to Langfuse.
4. The draft reply goes back to n8n → **human-approval step** → only then is it
   sent out through the channel.

No autonomous outbound execution during MVP. The Finance Agent never executes
payments.

## Deliberately deferred

- **Vector DB** — knowledge base is small enough for in-context retrieval; add
  vector search only when it stops fitting.
- **Orchestrator as code** — routing starts as n8n workflows; graduate to code
  if flows outgrow low-code.
