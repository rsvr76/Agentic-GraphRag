"""API Key Validation & Health Check Utility.

Tests all configured providers (Groq, NVIDIA NIM, and multiple Gemini keys)
and outputs a clear report showing status, latency, and active models.
"""

import os
import sys
import time
from typing import Dict, List
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(override=True)
from src.config import settings


def test_groq() -> List[Dict[str, str]]:
    api_key = (os.getenv("GROQ_API_KEY") or settings.groq_api_key).strip()
    if not api_key or api_key.startswith("your_"):
        return [{"provider": "Groq", "status": "Not Configured", "model": settings.groq_model, "latency": "0.00s", "note": "Set GROQ_API_KEY in .env"}]
    
    models = ["openai/gpt-oss-20b", "qwen/qwen3.8-27b"]
    results = []
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=settings.groq_base_url.strip())
    
    for m in models:
        try:
            t0 = time.time()
            resp = client.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": "Respond with: OK"}],
                max_tokens=10
            )
            latency = time.time() - t0
            content = resp.choices[0].message.content.strip()
            results.append({"provider": "Groq", "status": "Working", "model": m, "latency": f"{latency:.2f}s", "note": f"Response: {content}"})
        except Exception as e:
            results.append({"provider": "Groq", "status": "Failed", "model": m, "latency": "0.00s", "note": str(e)[:90]})
    return results


def test_nvidia() -> List[Dict[str, str]]:
    api_key = (os.getenv("NVIDIA_API_KEY") or settings.nvidia_api_key).strip()
    if not api_key or api_key.startswith("your_"):
        return [{"provider": "NVIDIA NIM", "status": "Not Configured", "model": settings.nvidia_model, "latency": "0.00s", "note": "Set NVIDIA_API_KEY in .env"}]
    
    candidate_models = [
        "nvidia/nemotron-3-super-120b-a12b",
        "meta/llama-3.2-11b-vision-instruct",
        "openai/gpt-oss-20b"
    ]
    
    results = []
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=settings.nvidia_base_url.strip())
    
    for m in candidate_models:
        try:
            t0 = time.time()
            resp = client.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": "Respond with: OK"}],
                max_tokens=10
            )
            latency = time.time() - t0
            content = resp.choices[0].message.content.strip()
            results.append({"provider": "NVIDIA NIM", "status": "Working", "model": m, "latency": f"{latency:.2f}s", "note": f"Response: {content}"})
        except Exception as e:
            results.append({"provider": "NVIDIA NIM", "status": "Failed", "model": m, "latency": "0.00s", "note": str(e)[:90]})
            
    return results


def test_gemini_keys() -> List[Dict[str, str]]:
    raw_keys_str = os.getenv("GEMINI_API_KEYS", "")
    single_key = os.getenv("GEMINI_API_KEY", "")
    
    keys = []
    if raw_keys_str:
        keys.extend([k.strip() for k in raw_keys_str.split(",") if k.strip()])
    if single_key and single_key.strip() not in keys:
        keys.append(single_key.strip())
        
    results = []
    if not keys:
        return [{"provider": "Gemini (all)", "status": "Not Configured", "model": settings.gemini_model, "latency": "0.00s", "note": "Set GEMINI_API_KEYS in .env"}]

    model_name = settings.gemini_model.strip()

    for idx, k in enumerate(keys):
        label = f"Gemini Key #{idx+1} ({k[:6]}...{k[-4:] if len(k) > 10 else ''})"
        if k.startswith("your_"):
            results.append({"provider": label, "status": "Placeholder", "model": model_name, "latency": "0.00s", "note": "Placeholder not updated"})
            continue
            
        try:
            from google import genai
            client = genai.Client(api_key=k)
            t0 = time.time()
            resp = client.models.generate_content(model=model_name, contents="Respond with: OK")
            latency = time.time() - t0
            content = (resp.text or "").strip()
            results.append({"provider": label, "status": "Working", "model": model_name, "latency": f"{latency:.2f}s", "note": f"Response: {content[:30]}"})
        except Exception as e1:
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=k)
                gen_model = legacy_genai.GenerativeModel(model_name=model_name)
                t0 = time.time()
                resp = gen_model.generate_content("Respond with: OK")
                latency = time.time() - t0
                content = (resp.text or "").strip()
                results.append({"provider": label, "status": "Working (legacy)", "model": model_name, "latency": f"{latency:.2f}s", "note": f"Response: {content[:30]}"})
            except Exception as e2:
                err_msg = str(e1) if "429" in str(e1) or "503" in str(e1) or "400" in str(e1) else str(e2)
                results.append({"provider": label, "status": "Failed", "model": model_name, "latency": "0.00s", "note": err_msg[:90]})
                
    return results


def check_all():
    print("=" * 80)
    print("LLM PROVIDER & API KEY HEALTH CHECK")
    print("=" * 80)
    
    checks = []
    checks.extend(test_groq())
    checks.extend(test_nvidia())
    checks.extend(test_gemini_keys())
    
    header = f"{'Provider / Key':<32} | {'Status':<16} | {'Model':<22} | {'Latency':<9} | {'Note'}"
    print(header)
    print("-" * 110)
    for c in checks:
        print(f"{c['provider']:<32} | {c['status']:<16} | {c['model']:<22} | {c['latency']:<9} | {c['note']}")
    print("=" * 80)


if __name__ == "__main__":
    check_all()
