"""Settings loaded from the environment / repo-root .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    llm_base_url: str = "http://localhost:11434/v1"
    llm_model: str = "scb10x/llama3.1-typhoon2-8b-instruct:latest"
    llm_api_key: str = "dummy"

    embed_base_url: str = "http://localhost:11434/v1"
    embed_model: str = "qwen3-embedding:latest"

    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "http://localhost:3001"

    cors_origins: list[str] = ["http://localhost:3000"]

    @property
    def langfuse_enabled(self) -> bool:
        return bool(self.langfuse_public_key and self.langfuse_secret_key)


settings = Settings()
