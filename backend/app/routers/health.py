"""Liveness endpoint — reports the configured models, checks nothing external."""

from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "llm_model": settings.llm_model,
        "embed_model": settings.embed_model,
        "langfuse": settings.langfuse_enabled,
    }
