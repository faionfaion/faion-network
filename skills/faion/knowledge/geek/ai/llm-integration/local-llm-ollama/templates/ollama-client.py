"""
purpose: OpenAI-compatible local client with health-probe + cloud fallback.
consumes: ollama base_url + model + optional cloud client + prompt
produces: text response from local or cloud fallback
depends-on: content/01-core-rules.xml r2, r4
token-budget-impact: zero for local; falls through to cloud cost on failure
"""
from __future__ import annotations

import requests
from openai import OpenAI

OLLAMA_BASE = "http://localhost:11434"


def ollama_ready(base_url: str = OLLAMA_BASE) -> bool:
    try:
        return requests.get(f"{base_url}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False


def make_local_client(base_url: str = OLLAMA_BASE) -> OpenAI:
    """OpenAI SDK pointed at local /v1 endpoint."""
    return OpenAI(base_url=f"{base_url}/v1", api_key="ollama")


def generate(prompt: str, model: str = "llama3.1:8b", cloud_fallback: OpenAI | None = None,
             cloud_model: str = "claude-sonnet-4-6") -> str:
    if not ollama_ready():
        if cloud_fallback is None:
            raise RuntimeError("Ollama not running. Start with: systemctl start ollama")
        return _cloud(cloud_fallback, prompt, cloud_model)
    local = make_local_client()
    try:
        resp = local.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content or ""
    except Exception:
        if cloud_fallback is not None:
            return _cloud(cloud_fallback, prompt, cloud_model)
        raise


def _cloud(client: OpenAI, prompt: str, model: str) -> str:
    resp = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content or ""
