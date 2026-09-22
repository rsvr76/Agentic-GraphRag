"""Unified LLM and Embeddings client supporting Google GenAI and Grok (xAI) with token tracking."""

import os
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel
from src.config import settings


class LLMResponse(BaseModel):
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    provider: str = ""


class UnifiedLLMClient:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.primary_llm_provider
        self._gemini_client = None
        self._grok_client = None

    def _get_gemini_client(self):
        api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key or api_key.startswith("your_"):
            return None
        if self._gemini_client is None:
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=api_key)
            except Exception:
                try:
                    import google.generativeai as legacy_genai
                    legacy_genai.configure(api_key=api_key)
                    self._gemini_client = legacy_genai
                except Exception:
                    self._gemini_client = None
        return self._gemini_client

    def _get_grok_client(self):
        api_key = settings.xai_api_key or os.getenv("XAI_API_KEY")
        if not api_key or api_key.startswith("your_"):
            return None
        if self._grok_client is None:
            from openai import OpenAI
            self._grok_client = OpenAI(
                api_key=api_key,
                base_url=settings.xai_base_url
            )
        return self._grok_client

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> LLMResponse:
        active_provider = provider or self.provider

        if active_provider == "grok":
            client = self._get_grok_client()
            if not client:
                return LLMResponse(
                    content=f"[Simulated Grok response (XAI_API_KEY required in .env)]",
                    prompt_tokens=len(prompt.split()),
                    completion_tokens=15,
                    total_tokens=len(prompt.split()) + 15,
                    model=settings.grok_model,
                    provider="grok-simulated"
                )
            active_model = model or settings.grok_model
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=active_model,
                messages=messages,
                temperature=temperature
            )
            usage = response.usage
            return LLMResponse(
                content=response.choices[0].message.content or "",
                prompt_tokens=usage.prompt_tokens if usage else 0,
                completion_tokens=usage.completion_tokens if usage else 0,
                total_tokens=usage.total_tokens if usage else 0,
                model=active_model,
                provider="grok"
            )
        else:
            # Default to Google GenAI / Gemini
            active_model = model or settings.gemini_model
            client = self._get_gemini_client()
            if not client:
                return LLMResponse(
                    content=f"[Simulated Gemini response (GEMINI_API_KEY required in .env)]",
                    prompt_tokens=len(prompt.split()),
                    completion_tokens=15,
                    total_tokens=len(prompt.split()) + 15,
                    model=active_model,
                    provider="gemini-simulated"
                )
            try:
                if hasattr(client, "models"):
                    # Modern google-genai SDK
                    config = {}
                    if system_instruction:
                        config["system_instruction"] = system_instruction
                    config["temperature"] = temperature
                    
                    response = client.models.generate_content(
                        model=active_model,
                        contents=prompt,
                        config=config
                    )
                    usage = getattr(response, "usage_metadata", None)
                    p_tok = getattr(usage, "prompt_token_count", 0) if usage else 0
                    c_tok = getattr(usage, "candidates_token_count", 0) if usage else 0
                    return LLMResponse(
                        content=response.text or "",
                        prompt_tokens=p_tok,
                        completion_tokens=c_tok,
                        total_tokens=p_tok + c_tok,
                        model=active_model,
                        provider="gemini"
                    )
                else:
                    # Legacy google.generativeai SDK fallback
                    gen_model = client.GenerativeModel(
                        model_name=active_model,
                        system_instruction=system_instruction
                    )
                    response = gen_model.generate_content(prompt)
                    usage = getattr(response, "usage_metadata", None)
                    p_tok = getattr(usage, "prompt_token_count", 0) if usage else 0
                    c_tok = getattr(usage, "candidates_token_count", 0) if usage else 0
                    return LLMResponse(
                        content=response.text or "",
                        prompt_tokens=p_tok,
                        completion_tokens=c_tok,
                        total_tokens=p_tok + c_tok,
                        model=active_model,
                        provider="gemini"
                    )
            except Exception as e:
                # Mock response if keys not configured yet during bootstrapping
                return LLMResponse(
                    content=f"[LLM generation simulated (API key needed)]: {e}",
                    prompt_tokens=len(prompt.split()),
                    completion_tokens=20,
                    total_tokens=len(prompt.split()) + 20,
                    model=active_model,
                    provider="gemini-mock"
                )

    def get_embedding(self, text: str) -> List[float]:
        """Generate vector embedding for text using Google GenAI or fallback."""
        try:
            from google import genai
            client = self._get_gemini_client()
            if hasattr(client, "models"):
                result = client.models.embed_content(
                    model=settings.embedding_model,
                    contents=text
                )
                return result.embeddings[0].values
        except Exception:
            pass
        # Return deterministic dummy vector if offline
        return [0.0] * 768


llm_client = UnifiedLLMClient()
