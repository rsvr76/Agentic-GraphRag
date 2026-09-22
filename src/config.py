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

    # TigerGraph Savanna Credentials
    tigergraph_host: str = "https://your-instance.i.tgcloud.io"
    tigergraph_username: str = "tigergraph"
    tigergraph_password: str = "tigergraph"
    tigergraph_graph: str = "Olympics"
    tigergraph_secret: str = ""
    tigergraph_token: str = ""

    # LLM Providers (Groq primary, Gemini fallback)
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.3-70b-versatile"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # Default LLM Provider selection
    primary_llm_provider: Literal["groq", "gemini"] = "groq"

    # Local Offline Embeddings (FastEmbed ONNX Runtime - <300MB RAM)
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_batch_size: int = 32

    # Benchmark & Agent Harness Parameters
    max_agent_steps: int = 6
    top_k_retrieval: int = 10


settings = Settings()
