1. Project Overview
This project builds a self-operating AI Agents team for two companies:
Chin Chun Co. (www.chinchun2002.com) — manufacturing / trading
NNPC Digital Transformation Consulting (www.nnpc.ai) — consulting services
Execution: a three-month intern program. Leader has an IT Marketing background; members are Computer Science students.
MVP principle: get four core agents live and producing measurable results first, then expand to all fourteen departments. Avoid building an all-encompassing system on day one.

2. MVP Scope
Phase
Departments
Notes
MVP (this phase)
Customer Service, Marketing, Sales, Finance
Working agents with tool integrations and KPIs
Phase 2
Management, HR, Procurement, Logistics
Reuse the architecture template validated in MVP
Phase 3
Production Planning, Production, QC, General Affairs, Compliance, R&D
Deeper system integration; onboard last

3. Architecture
Users / internal staff
      │
▌Orchestrator Agent▌── task routing, cross-agent coordination, human-review gates
      │
 ├─ Customer Service Agent
 ├─ Marketing Agent
 ├─ Sales Agent
 └─ Finance Agent
      │
▌Shared layer▌── knowledge base (docs / FAQ / product data), tool integrations (Email / LINE / CRM / accounting), logging & monitoring
​
Design principles:
One architecture, two companies: same agent templates with swapped knowledge bases and tool configs. Validate at NNPC first, then replicate to Chin Chun.
Human-in-the-loop: any outbound message, payment, or quotation requires human approval. No autonomous execution during MVP.
On-prem first (dogfooding): all LLM inference runs on the on-premises AI servers that NNPC itself sells, making this project a live proof case for NNPC's product line. Peripheral tooling stays on current SaaS (Notion, LINE OA, Google Workspace); no custom infrastructure.

4. Core Agent Specifications
4.1 Customer Service Agent
Duties: answer FAQs, look up order/service status, escalate complex cases to humans
Integrations: LINE OA / web forms / email; knowledge base on Notion
KPIs: auto-resolution rate ≥ 60%; first response < 1 min; correct escalation ≥ 90%
4.2 Marketing Agent
Duties: draft social & EDM copy, maintain content calendar, summarize competitor activity
Integrations: Notion content library, social scheduling tools, web analytics
KPIs: ≥ 5 usable drafts per week; human edit volume trending down week over week
4.3 Sales Agent
Duties: lead list organization and outreach drafts, pre-meeting briefs, follow-up drafts, CRM updates
Integrations: CRM (or Notion as a stand-in), email, calendar
KPIs: ≥ 20 leads processed per week; follow-up drafts within 24 hours
4.4 Finance Agent
Duties: document classification, AR reminder drafts, weekly cash-flow digest, month-end checklist
Integrations: accounting software exports, bank statements, spreadsheets
KPIs: classification accuracy ≥ 95%; weekly report on time 100% (note: drafts and reminders only — never executes payments)

5. Team Roles
Role
Responsibility
Leader (IT Marketing)
requirements interviews, prompt design, acceptance criteria, stakeholder communication
Member A (CS)
Orchestrator & Customer Service Agent, tool integrations
Member B (CS)
Marketing & Sales Agents, knowledge base build-out
Member C (CS)
Finance Agent, monitoring & testing, documentation

6. Three-Month Timeline
Month 1: Foundation + Customer Service Agent
W1: requirements interviews at both companies; inventory of tools and data
W2: build knowledge base (FAQ, product/service data); finalize tech stack
W3–W4: Customer Service Agent live (NNPC first); internal testing and iteration
Milestone M1: CS Agent answers ≥ 80% of FAQs correctly
Month 2: Marketing + Sales Agents
W5–W6: Marketing Agent (content pipeline); replicate CS Agent to Chin Chun
W7–W8: Sales Agent (lead/follow-up flows); first version of the Orchestrator
Milestone M2: three agents in real use at ≥ 1 company
Month 3: Finance Agent + Integration & Handover
W9–W10: Finance Agent; cross-agent collaboration testing
W11: full rollout at both companies; KPI measurement
W12: documentation, handover manual, Phase 2 proposal, final presentation
Milestone M3: four agents live at both companies with complete documentation

7. Recommended Tech Stack
LLM: on-prem open-weight models (Llama 3.3, Mistral, gpt-oss, etc.) served via vLLM / Ollama on NNPC's own on-prem AI Server product. The project doubles as a dogfooding showcase — deliverables convert directly into sales demos and customer case studies
Data sovereignty: all inference stays on-premises; company data never leaves the server room — a direct answer to customer privacy/compliance concerns
Agent framework: n8n (self-hostable on-prem) or a lightweight custom orchestrator calling the local model API — choose per intern skill level; validate with low-code first, then graduate
Knowledge base: Notion (already in use) + vector search if needed
Interfaces: LINE OA (customer service), email, Slack/LINE groups internally
Monitoring: daily conversation-log review board (Notion database)

8. Risks & Governance
Risk
Mitigation
Wrong agent answers cause external damage
all outbound messages human-reviewed before sending during MVP
Interns leave after 3 months; no maintainer
mandatory documentation & handover in W12; prefer low-code tooling
Confidential data leakage
tiered knowledge base; salaries / contracts / customer PII excluded from agent-accessible scope
Scope creep
every new request goes to the Phase 2 backlog; MVP scope is frozen

9. Success Criteria (end of month 3)
Four agents live and in real use at both companies
Each agent meets the KPIs in Section 4
Complete documentation: architecture diagram, prompt library, ops manual, handover guide
Phase 2 proposal covering the remaining ten departments with priorities and estimates