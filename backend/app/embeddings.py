"""Embedding client — bge-m3 served by vLLM with --task embed."""

from openai import AsyncOpenAI

from app.config import settings

client = AsyncOpenAI(base_url=settings.embed_base_url, api_key=settings.llm_api_key)


async def embed(texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(model=settings.embed_model, input=texts)
    return [item.embedding for item in response.data]
