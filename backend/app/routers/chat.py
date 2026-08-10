"""Agent endpoints: list agents, chat with one, embed texts."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents import AGENTS
from app.config import settings
from app.embeddings import embed
from app.llm import chat

router = APIRouter()


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    agent: str
    messages: list[Message] = Field(min_length=1)


class EmbedRequest(BaseModel):
    texts: list[str] = Field(min_length=1, max_length=64)


@router.get("/agents")
async def list_agents() -> list[dict]:
    return [{"key": key, "name": spec["name"]} for key, spec in AGENTS.items()]


@router.post("/chat")
async def agent_chat(request: ChatRequest) -> dict:
    spec = AGENTS.get(request.agent)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {request.agent}")
    reply = await chat(
        spec["system_prompt"], [m.model_dump() for m in request.messages]
    )
    return {
        "agent": request.agent,
        "model": settings.llm_model,
        "message": {"role": "assistant", "content": reply},
    }


@router.post("/embed")
async def embed_texts(request: EmbedRequest) -> dict:
    vectors = await embed(request.texts)
    return {
        "model": settings.embed_model,
        "dimensions": len(vectors[0]) if vectors else 0,
        "embeddings": vectors,
    }
