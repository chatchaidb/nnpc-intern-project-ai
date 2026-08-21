# CLAUDE.md — Project Context & Working Agreement

> **Read this first.** The repo you see is a fresh skeleton. It does **not**
> reflect the system that is already running on the client's server. This file
> reconciles the two and states how we intend to build. When the repo and this
> file disagree, this file describes *reality*; the repo describes an *earlier plan*.
>
> Last verified against the running server: **2026-08-11.** Anything here may
> drift — re-verify before relying on it for a big decision.

---

## 1. What this project is

A four-agent AI system (Customer Service, Marketing, Sales, Finance) for two
clients — **NNPC** (consulting) and **Chin Chun** (manufacturing/trading) —
behind an orchestrator with human-review gates on everything outbound. Built by
a small intern team over ~3 months. MVP focus is the **Customer Service agent
first**, then replicate.

Full charter: `docs/project-overview.md`. That charter is still our north star
for *scope and principles*. It is **not** accurate about the current tech state —
see Section 3.

## 2. The big thing the repo doesn't tell you: "RuuMak" already exists

A previous developer (now departed) built a more complete system called
**RuuMak**, and it is **currently running** on the client's on-prem server. We
inherited it as a running black box with limited documentation. Its source lives
on that server under `~/ruumak/` (not yet in our version control).

RuuMak is **partial, not finished.** "Running" ≠ "done." Several features are
plumbed but switched off (`line=off`, `tracing=off`), and the knowledge base is
essentially empty (see Section 4).

**Our stance toward RuuMak = salvage, not blind-adopt and not ignore.** We mine
it for expensive-to-recreate assets and rebuild the code in a form *we own and
can maintain*, because our charter (Section 8) explicitly requires the system to
survive after the interns leave. Adopting an undocumented custom codebase whole
works against that.

Worth lifting from RuuMak:
- Its **FAQ content** (see Section 4).
- Its **multi-tenancy pattern**: same Docker image, one orchestrator instance
  per tenant, per-tenant data mount. This is a proven pattern — copy it.
- Its **approval-queue / human-in-the-loop** design.
- Its **prompts** and its **eval harness** (`~/ruumak/evals/`).
- Its **design philosophy** (Section 5) — genuinely good, keep it.

## 3. Actual infrastructure (verified 2026-08-11)

Everything runs on the client's on-prem AI server, reached over VPN. The models
are already served as **OpenAI-compatible HTTP endpoints** — we do **not** need
to install or host any model ourselves; we call what's already running.

**Model backends currently up:**

| Backend | Endpoint (on the server) | Purpose |
|---|---|---|
| vLLM | `:8010/v1` | Serving path. Runs `typhoon2-8b` (`scb10x/llama3.1-typhoon2-8b-instruct`, ctx 8192). Production-grade / high-throughput engine. |
| Ollama | `:11434/v1` | Dev + embeddings + misc models. Easier, lower-throughput engine. |
| Qdrant | `:6333` | Vector store. **Currently near-empty** (see Section 4). |

**Embedding model in use:** `qwen3-embedding` (via env `EMBED_MODEL`).
Note: the repo's stack table says `bge-m3` — that's stale. Reality is
`qwen3-embedding`.

**Chat models available on Ollama:** `typhoon2-8b`, `llama3.2`, `qwen2.5:32b`,
`qwen2.5-coder:32b`, plus larger/newer names (`qwen3.6:27b`, `ornith:35b`).
- `ornith:35b` is **not** a custom model — it's a stock Qwen3.5-MoE with a
  "coding assistant" system prompt. Not CS-relevant.
- **No fine-tuned models exist.** Customization was done via *system prompt +
  temperature*, never by training. (Typhoon on the server carries a custom
  system prompt and `temperature 0.4`.) Keep customizing this way — it's
  inspectable and reversible.

**⛔ Do NOT use `:cloud` models** (`kimi-k2.7-code:cloud`, `glm-5.2:cloud`, etc.)
in any agent path that touches client data. The `:cloud` suffix routes inference
to an external API — that **breaks the on-prem / data-sovereignty guarantee** we
sell to both clients (charter Section 3 & 8). They're acceptable only for our own
dev tooling, never in the product.

## 4. Data state — the real blocker

The agent can only answer from material we load into it. Right now that material
is thin:

- `~/ruumak/agents/cs/faq_chinchun.yaml` — **real** Chin Chun content, but it's
  **internal-staff HR/leave policy** (paraphrased from one scanned regulation
  sheet), not external customer-service FAQs. ~a dozen entries. Accurate; numbers
  preserved exactly from source.
- `~/ruumak/agents/cs/faq_nnpc.yaml` — **placeholder**, hand-written from the
  public nnpc.ai website. The author marked it v0, to be replaced.
- **Qdrant `nnpc_kb`**: `points_count: 30`, `indexed_vectors_count: 0` —
  effectively empty. The real document ingestion (repo's "Week 2" work) was
  **never done**. There is **no Chin Chun collection at all.**

**Takeaway: the previous dev hit the same data wall we're hitting.** He had one
scanned sheet and a public website — no hidden data source. The real unblock is
getting **substantial source documents** from the clients (product/service info,
customer FAQs, order references). That is a people/permission task, not a coding
task, and it's pending with the employer (Section 8).

Current FAQ matching (`~/ruumak/agents/cs/faq_store.py`) is **keyword-based in
code** (v0). Vector/RAG retrieval was planned but not built.

## 5. Design philosophy to preserve

From the previous dev's code comments, and worth keeping as our own rule:

> **Code owns every fact; the model only owns phrasing.** The model never
> decides *whether* a question is answerable — code selects the answer, the model
> only rephrases it. Anything not backed by a real source document is deliberately
> absent, so the agent **escalates rather than guesses.**

This is the right posture for a CS agent where a confidently-wrong answer (e.g.
an HR or pricing fact) is worse than an escalation. Build to this.

## 6. How we build (non-negotiables)

1. **Use the client's running models via their endpoints** — do not install
   models locally. Call them over HTTP.
2. **Keep the model call behind a swappable adapter** (backend URL + model name
   in env/config, never hardcoded). This is a core project requirement: an
   industrial partner will later provide their own model API, and swapping it
   must be a one-line config change. It's also how "use their models today,
   partner's model tomorrow" stays trivial.
3. **Build in this repo, on our machines. Deploy to the server.** Do **not**
   author code by typing into an SSH session on the live box. SSH is for
   inspection and deployment only. The live server may be serving real traffic;
   don't edit production by hand.
4. **On-prem only.** All inference stays on the client's server. No cloud model
   calls in the product path. Company data never leaves the server room.
5. **Human-in-the-loop.** No outbound message, quotation, or payment leaves
   without human approval during MVP. Finance agent **never executes payments** —
   drafts/reminders only.
6. **No secrets in the repo.** VPN/SSH/model credentials, LINE tokens, `.env`
   values live outside version control (`.env` is gitignored; use `.env.example`
   as the template). If you find a secret committed, flag it.
7. **Multi-tenancy from day one.** Hard data isolation between NNPC and Chin Chun
   is a client requirement, not a later retrofit. Follow RuuMak's per-tenant
   instance + per-tenant data-mount pattern.

## 7. Immediate priorities

While we wait on real source documents (Section 8), build the foundation so data
can be plugged in the moment it arrives:

1. **CS agent skeleton**: message in → FAQ match (code-side) → model rephrases →
   reply. Wire it to the **existing** vLLM/Ollama endpoint via the adapter.
2. **Reuse** `faq_chinchun.yaml` / `faq_nnpc.yaml` as starting content (pending
   the clearance in Section 8).
3. **Approval gate**: outbound answers pass through a human-review step.
4. **Get RuuMak's source into our version control** (a read-only copy) so months
   of prior work aren't one disk failure from gone, and so we can study it.
5. **Model choice = measure, don't guess.** Before switching the answer model,
   run the candidate (e.g. Qwen3-8B) against the dev's existing CS eval set
   (`~/ruumak/evals/questions.json`) head-to-head with Typhoon2-8B. Typhoon is
   Thai-tuned and may beat a newer generic model on Thai CS phrasing — decide on
   numbers. Check GPU headroom (`nvidia-smi`) before loading a second model.

## 8. Open questions (pending employer — do not assume answers)

- **Direction:** is the deliverable *RuuMak finished*, or *our own system* hitting
  the same goals? The team must not split between the two.
- **Data clearance:** are we cleared to reuse RuuMak's FAQ content? Is any of it
  out of scope (PII, contracts, salary/HR)?
- **Source documents:** who provides the real product/service/customer material
  so the knowledge base is more than a placeholder?
- **Server dependency:** may our agents depend on this server's models as the
  backend long-term, or is it shared/subject to change?
- **Accounts:** move off the shared login to per-person accounts before we take
  ownership of a live system.

---

### Glossary (plain language)

- **vLLM / Ollama** — two programs that "serve" an AI model behind a web address.
  Ollama = easy, for development. vLLM = fast, for production. Same interface, so
  our code can point at either by changing a URL.
- **Endpoint** — a web address our code sends a question to and gets an answer
  back. The models are already running as endpoints; we just call them.
- **Embedding model** — turns text into numbers so similar text can be searched.
  Used for RAG. Ours is `qwen3-embedding`.
- **Qdrant / vector store** — the search index that RAG looks things up in.
  Currently near-empty.
- **RAG** — answering by first *retrieving* relevant documents, then having the
  model phrase an answer from them. Needs real documents loaded (our blocker).
- **Adapter / swappable backend** — keeping the model's address in a config value
  so we can point at a different model later without rewriting code.
- **Multi-tenancy** — running the same system separately for each client so their
  data never mixes.
