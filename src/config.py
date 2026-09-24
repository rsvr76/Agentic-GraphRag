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
    tigergraph_username: str = ""
    tigergraph_password: str = ""
    tigergraph_graph: str = "Olympics"
    tigergraph_secret: str = ""
    tigergraph_token: str = ""

    # Groq Provider
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "qwen/qwen3.8-27b"

    # NVIDIA NIM Provider (OpenAI-compatible)
    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_model: str = "nvidia/nemotron-3-super-120b-a12b"

    # Google Gemini Provider (Single or Comma-separated pool)
    gemini_api_key: str = ""
    gemini_api_keys: str = ""
    gemini_model: str = "gemini-3.5-flash"

    # Active Primary Provider (Hierarchy: 1. Gemini, 2. NVIDIA NIM, 3. Groq)
    primary_llm_provider: Literal["gemini", "nvidia", "groq"] = "gemini"

    # Local Offline Embeddings (FastEmbed ONNX Runtime - <300MB RAM)
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_batch_size: int = 32

    # Benchmark & Agent Harness Parameters
    max_agent_steps: int = 6
    top_k_retrieval: int = 10

    def get_gemini_keys(self) -> list:
        keys = []
        if self.gemini_api_keys:
            keys.extend([k.strip() for k in self.gemini_api_keys.split(",") if k.strip()])
        if self.gemini_api_key and self.gemini_api_key.strip() not in keys:
            keys.append(self.gemini_api_key.strip())
        return [k for k in keys if not k.startswith("your_")]


settings = Settings()
