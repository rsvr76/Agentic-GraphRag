"""Unified LLM client supporting Groq (LPU at console.groq.com) and Google Gemini with automatic fallback and uniform token tracking."""

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
        self._gemini_client = None

    def _get_groq_client(self):
        api_key = settings.groq_api_key or os.getenv("GROQ_API_KEY")
        if not api_key or api_key.startswith("your_"):
            return None
        if self._groq_client is None:
            from openai import OpenAI
            self._groq_client = OpenAI(
                api_key=api_key,
                base_url=settings.groq_base_url
            )
        return self._groq_client

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

        active_model = model or settings.groq_model
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
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
                provider="groq"
            )
        except Exception as e:
            logger.warning(f"Groq API call failed ({e}). Falling back to secondary provider if available.")
            return None

    def _generate_gemini(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> Optional[LLMResponse]:
        client = self._get_gemini_client()
        if not client:
            return None

        active_model = model or settings.gemini_model
        try:
            if hasattr(client, "models"):
                config = {"temperature": temperature}
                if system_instruction:
                    config["system_instruction"] = system_instruction
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
            logger.warning(f"Gemini API call failed ({e}).")
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

        # Attempt primary provider first
        if active_provider == "groq":
            res = self._generate_groq(prompt, system_instruction, model, temperature)
            if res is not None:
                return res
            # Fallback to Gemini
            res = self._generate_gemini(prompt, system_instruction, model, temperature)
            if res is not None:
                return res
        else:
            res = self._generate_gemini(prompt, system_instruction, model, temperature)
            if res is not None:
                return res
            # Fallback to Groq
            res = self._generate_groq(prompt, system_instruction, model, temperature)
            if res is not None:
                return res

        # Simulation response if both keys are unconfigured (safe bootstrapping mode)
        approx_tokens = len(prompt.split())
        return LLMResponse(
            content="[LLM execution simulated: Please configure GROQ_API_KEY or GEMINI_API_KEY in .env]",
            prompt_tokens=approx_tokens,
            completion_tokens=15,
            total_tokens=approx_tokens + 15,
            model=model or settings.groq_model,
            provider="simulated"
        )


llm_client = UnifiedLLMClient()
