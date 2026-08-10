"""Chat client against vLLM's OpenAI-compatible API.

When Langfuse keys are configured, the drop-in wrapper traces every call;
otherwise this is a plain OpenAI client and tracing is silently skipped.
"""

from app.config import settings

if settings.langfuse_enabled:
    from langfuse.openai import AsyncOpenAI
else:
    from openai import AsyncOpenAI

client = AsyncOpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)


async def chat(system_prompt: str, messages: list[dict]) -> str:
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[{"role": "system", "content": system_prompt}, *messages],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
