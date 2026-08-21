# HANDOFF — CS Agent (n8n RAG prototype)

**Read this fully before touching anything. This is the employer's repo.**

> **Status:** the three items under "TASK" below are **done** — they are what
> put this file, the workflow JSONs and the corrected README into the repo.
> Read them as a record of what changed, not as work to do. The live to-do list
> is **"OPEN / NOT DONE"** near the bottom.

---

## RULES FOR CLAUDE CODE — READ FIRST

1. **Do not push. Do not commit. Do not open a PR.** Make changes in the working
   tree only and stop. The human reviews and pushes.
2. **Do not refactor.** Do not rename files, reorganise folders, reformat code,
   or "improve" anything you were not explicitly asked to change.
3. **Do not touch** `backend/`, `frontend/`, `docker-compose.yml`, or any file
   outside the specific edits listed in "TASK" below.
4. **No new dependencies.** No new packages, no new services, no version bumps.
5. **Minimal diffs.** Change the fewest lines possible. If a fix needs more than
   ~10 lines in a file you were not asked about, stop and ask.
6. **Never commit secrets.** VPN credentials, SSH passwords, IPs, and API keys
   must not enter this repo, not even in comments or examples. If you see one in
   a file, flag it — do not silently keep it.
7. **When unsure, ask.** Do not guess at config values. This project has already
   lost time to stale/guessed values (see "Stale docs" below).

---

## TASK

Only these three things:

### 1. Fix stale values in `README.md`

The README currently states values that are wrong. Verified against the running
server on 2026-08-21:

| README says | Reality |
|---|---|
| Embeddings: `bge-m3` | `qwen3-embedding:latest` |
| vLLM chat port `8001` | vLLM is on `8010` |
| vLLM embeddings port `8002` | does not exist |
| Vector DB: "Skipped for MVP" | Qdrant is running and in use |
| LLM default: Qwen3-8B | `scb10x/llama3.1-typhoon2-8b-instruct:latest` via Ollama |

Update the Stack table and Ports table to match. Do not rewrite the rest of the
README.

### 2. Add the n8n workflow JSONs

Place these in `n8n/` (the folder already exists for exported workflow JSON):

- `nnpc-cs-v5.json` — customer service agent
- `nnpc-ingestion-v2.json` — document ingestion

Do not modify their contents.

### 3. Add a short note in `n8n/README.md`

If that file exists, append. If not, create it. Keep it under 30 lines. Cover
only: what the two workflows do, which credentials must be created by hand, and
that Postgres/Gmail nodes ship disabled.

**Nothing else.**

---

## CONTEXT (background only — not tasks)

### What was built

A working RAG customer-service pipeline in n8n, replacing the keyword-based FAQ
matching in `~/ruumak/agents/cs/faq_store.py` on the client server. RuuMak
planned vector retrieval but never built it; this is that missing piece.

Flow: Chat Trigger / Webhook -> Normalize Input -> AI Agent (with Qdrant tool)
-> IF (escalation check) -> response.

### Current state

- 23 FAQ entries (20 original from `faq_nnpc.yaml` + 3 added, see below)
- 18 chunks in Qdrant collection `nnpc_docs`, all tagged `tenant: nnpc`
- Answers correctly in Thai, escalates when data is missing
- Approval gate (Gmail) and audit log (Postgres) exist as nodes but are DISABLED
- Runs on the developer's laptop only; no real channel connected

### Models (all on the client server, reached over VPN)

| Purpose | Model | Endpoint |
|---|---|---|
| Chat | `scb10x/llama3.1-typhoon2-8b-instruct:latest` | Ollama `:11434` |
| Embeddings | `qwen3-embedding:latest` | Ollama `:11434` |
| Vector store | Qdrant `nnpc_docs` | local to dev machine `:6333` |

Server IP and credentials are held separately and must NOT be committed.

Never use any `:cloud` model (`glm-5.2:cloud`, `kimi-k2.7-code:cloud`) — those
route inference off-server and break the on-prem guarantee.

---

## THREE THINGS THE NEXT PERSON SHOULD KNOW

### 1. Stale docs cost real time

The repo documented `bge-m3` and ports 8001/8002. Both were wrong. Always verify
against the running server (`curl /api/tags`, `docker ps`) before building.
That is why task #1 exists.

### 2. Small models paraphrase refusals

The system prompt instructs the model to output the literal string `NEED_HUMAN`
when it has no data. Typhoon-8B frequently paraphrases instead
("ไม่พบในฐานข้อมูล..."), so the IF node misses it and the answer goes out as
approved. Worse, with weak retrieval results in context, it sometimes invents
facts outright (it produced two different sets of business hours on separate
runs, at temperature 0).

Three mitigations were tried:
- Tighter prompt wording — partially effective
- Widening the IF node to match ~9 refusal phrasings — partially effective
- **Adding an explicit FAQ entry so the "no data" path is never reached — this
  worked**

The third is the same approach the original RuuMak author used (see their
comments on the `greeting` and `capabilities` entries). It is model-independent.
Three such entries were added: `business_hours`, `pricing_not_available`,
`company_details_not_available`.

Expect every future agent to hit this. Budget for it.

### 3. The GPU is saturated by vLLM

`nvidia-smi` on the server (RTX 5090, 32GB):

```
32044MiB / 32607MiB used
VLLM::EngineCore          27030MiB
ollama llama-server        3118MiB
```

vLLM pre-allocates ~90% of VRAM by default. It is holding 27GB to serve an 8B
model that needs about 5GB. Anything else falls back to CPU — a 27B model took
roughly 2.5 minutes per answer for this reason, not because of its size.

Fix is one flag: restart vLLM with `--gpu-memory-utilization 0.2`, freeing about
20GB. Or drop the vLLM container entirely, since the same Typhoon model is
already served by Ollama.

This is a server-owner action, not a repo change.

---

## OPEN / NOT DONE

- Gmail approval gate — node present, disabled, needs a named approver address
- Postgres audit log — node present, disabled, no Postgres instance yet
- Eval set at `~/ruumak/evals/questions.json` — never pulled; needed for a real
  accuracy baseline and for comparing models objectively
- Chin Chun tenant — `faq_chinchun.yaml` is internal staff HR policy, not
  customer FAQ. Scope decision still open.
- No real channel (LINE/email). LINE needs a public HTTPS endpoint, which means
  deploying to the server rather than a laptop.
- Marketing / Sales / Finance agents — no data supplied yet
- Finance will need database queries, not RAG. Numbers retrieve badly from
  embeddings.

---

## SECURITY FLAG

Access currently uses a shared VPN account and a shared SSH login with weak
credentials. Should become per-person logins before more people are added.
Do not record any of those values in this repo.
