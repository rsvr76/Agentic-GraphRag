"""Global configuration management using Pydantic Settings."""

import os
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # TigerGraph Credentials
    tigergraph_host: str = "https://your-instance.i.tgcloud.io"
    tigergraph_username: str = "tigergraph"
    tigergraph_password: str = "tigergraph"
    tigergraph_graph: str = "OlympicsCorpus"
    tigergraph_secret: str = ""
    tigergraph_token: str = ""

    # LLM Providers
    gemini_api_key: str = ""
    xai_api_key: str = ""
    xai_base_url: str = "https://api.x.ai/v1"

    # Default Models
    primary_llm_provider: Literal["gemini", "grok"] = "gemini"
    gemini_model: str = "gemini-2.5-flash"
    grok_model: str = "grok-beta"
    embedding_model: str = "text-embedding-004"

    # Execution Parameters
    max_agent_steps: int = 8
    top_k_retrieval: int = 5


settings = Settings()
