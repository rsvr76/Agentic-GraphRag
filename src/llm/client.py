"""Unified LLM client supporting Groq, NVIDIA NIM, and Google Gemini with multi-key rotation and automatic failover."""

import os
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from src.config import settings

logger = logging.getLogger(__name__)


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
        self._groq_client = None
        self._nvidia_client = None
        self._gemini_clients: Dict[str, Any] = {}
        self._gemini_active_idx = 0

    def _get_groq_client(self):
        api_key = (settings.groq_api_key or os.getenv("GROQ_API_KEY", "")).strip()
        if not api_key or api_key.startswith("your_"):
            return None
        if self._groq_client is None:
            from openai import OpenAI
            self._groq_client = OpenAI(
                api_key=api_key,
                base_url=settings.groq_base_url.strip()
            )
        return self._groq_client

    def _get_nvidia_client(self):
        api_key = (settings.nvidia_api_key or os.getenv("NVIDIA_API_KEY", "")).strip()
        if not api_key or api_key.startswith("your_"):
            return None
        if self._nvidia_client is None:
            from openai import OpenAI
            self._nvidia_client = OpenAI(
                api_key=api_key,
                base_url=settings.nvidia_base_url.strip()
            )
        return self._nvidia_client

    def _get_gemini_client(self, api_key: str):
        key = api_key.strip()
        if not key or key.startswith("your_"):
            return None
        if key not in self._gemini_clients:
            try:
                from google import genai
                self._gemini_clients[key] = genai.Client(api_key=key)
            except Exception:
                try:
                    import google.generativeai as legacy_genai
                    legacy_genai.configure(api_key=key)
                    self._gemini_clients[key] = legacy_genai
                except Exception:
                    self._gemini_clients[key] = None
        return self._gemini_clients.get(key)

    def _generate_groq(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> Optional[LLMResponse]:
        client = self._get_groq_client()
        if not client:
            return None

        primary_model = (model or settings.groq_model).strip()
        candidate_models = [primary_model]
        for fallback in ["openai/gpt-oss-20b", "qwen/qwen3.8-27b"]:
            if fallback not in candidate_models:
                candidate_models.append(fallback)

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        for m in candidate_models:
            try:
                response = client.chat.completions.create(
                    model=m,
                    messages=messages,
                    temperature=temperature
                )
                usage = response.usage
                return LLMResponse(
                    content=response.choices[0].message.content or "",
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    total_tokens=usage.total_tokens if usage else 0,
                    model=m,
                    provider="groq"
                )
            except Exception as e:
                logger.warning(f"Groq API call failed with model {m} ({e}). Trying next model.")

        return None

    def _generate_nvidia(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> Optional[LLMResponse]:
        client = self._get_nvidia_client()
        if not client:
            return None

        primary_model = (model or settings.nvidia_model).strip()
        candidate_models = [primary_model]
        for fallback in [
            "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
            "nvidia/nemotron-3-super-120b-a12b",
            "meta/llama-3.2-11b-vision-instruct",
            "openai/gpt-oss-20b"
        ]:
            if fallback not in candidate_models:
                candidate_models.append(fallback)

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        for m in candidate_models:
            try:
                response = client.chat.completions.create(
                    model=m,
                    messages=messages,
                    temperature=temperature
                )
                usage = response.usage
                content = response.choices[0].message.content or ""
                # Also check reasoning_content if present in extra fields
                return LLMResponse(
                    content=content,
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    total_tokens=usage.total_tokens if usage else 0,
                    model=m,
                    provider="nvidia"
                )
            except Exception as e:
                logger.warning(f"NVIDIA NIM API call failed with model {m} ({e}). Trying next model.")

        return None

    def _generate_gemini(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> Optional[LLMResponse]:
        gemini_keys = settings.get_gemini_keys()
        if not gemini_keys:
            return None

        active_model = (model or settings.gemini_model).strip()
        candidate_models = [active_model]
        for m_fallback in ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"]:
            if m_fallback not in candidate_models:
                candidate_models.append(m_fallback)

        total_keys = len(gemini_keys)

        # Try prioritized model first across keys before falling back to lite models
        for target_model in candidate_models:
            for offset in range(total_keys):
                idx = (self._gemini_active_idx + offset) % total_keys
                key = gemini_keys[idx]
                client = self._get_gemini_client(key)
                if not client:
                    continue

                try:
                    if hasattr(client, "models"):
                        config = {"temperature": temperature}
                        if system_instruction:
                            config["system_instruction"] = system_instruction
                        response = client.models.generate_content(
                            model=target_model,
                            contents=prompt,
                            config=config
                        )
                        usage = getattr(response, "usage_metadata", None)
                        p_tok = getattr(usage, "prompt_token_count", 0) if usage else 0
                        c_tok = getattr(usage, "candidates_token_count", 0) if usage else 0
                        self._gemini_active_idx = idx
                        return LLMResponse(
                            content=response.text or "",
                            prompt_tokens=p_tok,
                            completion_tokens=c_tok,
                            total_tokens=p_tok + c_tok,
                            model=target_model,
                            provider=f"gemini_key_{idx+1}"
                        )
                    else:
                        gen_model = client.GenerativeModel(
                            model_name=target_model,
                            system_instruction=system_instruction
                        )
                        response = gen_model.generate_content(prompt)
                        usage = getattr(response, "usage_metadata", None)
                        p_tok = getattr(usage, "prompt_token_count", 0) if usage else 0
                        c_tok = getattr(usage, "candidates_token_count", 0) if usage else 0
                        self._gemini_active_idx = idx
                        return LLMResponse(
                            content=response.text or "",
                            prompt_tokens=p_tok,
                            completion_tokens=c_tok,
                            total_tokens=p_tok + c_tok,
                            model=target_model,
                            provider=f"gemini_key_{idx+1}"
                        )
                except Exception as e:
                    logger.debug(f"Gemini API key #{idx+1} with {target_model} failed ({e}). Trying next key/model.")

        return None

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> LLMResponse:
        active_provider = provider or self.provider

        # Enforce API providers hierarchy: 1. Gemini (all keys), 2. NVIDIA NIM, 3. Groq
        providers_order = ["gemini", "nvidia", "groq"]
        if active_provider == "nvidia":
            providers_order = ["nvidia", "gemini", "groq"]
        elif active_provider == "groq":
            providers_order = ["groq", "gemini", "nvidia"]

        for p in providers_order:
            if p == "groq":
                res = self._generate_groq(prompt, system_instruction, model, temperature)
                if res is not None:
                    return res
            elif p == "nvidia":
                res = self._generate_nvidia(prompt, system_instruction, model, temperature)
                if res is not None:
                    return res
            elif p == "gemini":
                res = self._generate_gemini(prompt, system_instruction, model, temperature)
                if res is not None:
                    return res

        # Simulation response if all configured providers are exhausted or unconfigured
        approx_tokens = len(prompt.split())
        return LLMResponse(
            content="[LLM execution simulated: Please configure valid API keys in .env]",
            prompt_tokens=approx_tokens,
            completion_tokens=15,
            total_tokens=approx_tokens + 15,
            model=model or settings.groq_model,
            provider="simulated"
        )


llm_client = UnifiedLLMClient()
