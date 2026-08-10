// Chat test bench: pick an agent, send a message, read the draft reply.
"use client";

import { useEffect, useRef, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Agent = { key: string; name: string };
type Message = { role: "user" | "assistant"; content: string };

export default function Home() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [agent, setAgent] = useState<string>("customer-service");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const chatRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`${API}/api/agents`)
      .then((r) => r.json())
      .then(setAgents)
      .catch(() => setError("Backend unreachable — is FastAPI running on :8000?"));
  }, []);

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight });
  }, [messages]);

  async function send(e: React.FormEvent) {
    e.preventDefault();
    const content = input.trim();
    if (!content || busy) return;
    const next: Message[] = [...messages, { role: "user", content }];
    setMessages(next);
    setInput("");
    setBusy(true);
    setError(null);
    try {
      const res = await fetch(`${API}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agent, messages: next }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setMessages([...next, data.message]);
    } catch (err) {
      setError(`Request failed: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setBusy(false);
    }
  }

  function pickAgent(key: string) {
    setAgent(key);
    setMessages([]);
    setError(null);
  }

  return (
    <main>
      <header>
        <h1>NNPC AI Agents</h1>
        <p>Internal test bench — every reply is a draft for human review.</p>
      </header>

      <div className="agent-picker">
        {agents.map((a) => (
          <button
            key={a.key}
            className={a.key === agent ? "active" : ""}
            onClick={() => pickAgent(a.key)}
          >
            {a.name}
          </button>
        ))}
      </div>

      <div className="chat" ref={chatRef}>
        {messages.length === 0 && (
          <div className="bubble assistant muted">
            Start a conversation with the {agents.find((a) => a.key === agent)?.name ?? "agent"}.
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.role}`}>
            {m.content}
          </div>
        ))}
        {busy && <div className="bubble assistant muted">Thinking…</div>}
        {error && <div className="bubble assistant muted">{error}</div>}
      </div>

      <form className="composer" onSubmit={send}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message (Thai or English)…"
          disabled={busy}
        />
        <button type="submit" disabled={busy || !input.trim()}>
          Send
        </button>
      </form>
    </main>
  );
}
