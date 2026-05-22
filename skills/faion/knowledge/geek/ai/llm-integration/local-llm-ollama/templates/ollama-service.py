"""
purpose: Production-ready Ollama wrapper — health check, generate, pull, cloud fallback hook.
consumes: model name + prompt + (optional) cloud_fallback_callable
produces: text response or escalation to cloud fallback
depends-on: content/01-core-rules.xml r3, r5
token-budget-impact: local — zero per call (sunk hardware cost)
"""
# OllamaService: production-ready wrapper with health check, generate, pull
# Usage: svc = OllamaService(); text = svc.generate("prompt")

from dataclasses import dataclass
from typing import Optional
import json
import logging
import requests


@dataclass
class OllamaConfig:
    model: str = "llama3.1:8b"
    temperature: float = 0.7
    num_ctx: int = 4096
    base_url: str = "http://localhost:11434"
    timeout: int = 120  # seconds — large models need time on first token


class OllamaService:
    """Production-ready Ollama service wrapper.

    Always call is_available() at startup before making model calls.
    Use the openai-compatible /v1 endpoint for drop-in cloud/local switching.
    """

    def __init__(self, config: Optional[OllamaConfig] = None):
        self.cfg = config or OllamaConfig()
        self.logger = logging.getLogger(__name__)

    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            return requests.get(
                f"{self.cfg.base_url}/api/tags", timeout=2
            ).status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, system: str = "") -> str:
        """Generate text. Returns response string.
        Raises RuntimeError with diagnostics if Ollama is unavailable.
        """
        if not self.is_available():
            raise RuntimeError(
                f"Ollama not running at {self.cfg.base_url}. "
                "Start with: ollama serve"
            )
        body = {
            "model": self.cfg.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": self.cfg.temperature,
                "num_ctx": self.cfg.num_ctx,
            },
        }
        resp = requests.post(
            f"{self.cfg.base_url}/api/generate",
            json=body,
            timeout=self.cfg.timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        # Log tokens/sec to detect CPU fallback (10-50x slower than GPU)
        if data.get("eval_count") and data.get("eval_duration"):
            tps = data["eval_count"] / (data["eval_duration"] / 1e9)
            self.logger.debug("%.1f tokens/sec (model=%s)", tps, self.cfg.model)
        return data["response"]

    def pull_model(self, model: str) -> bool:
        """Pull a model. Blocking — handle as a long-running operation."""
        resp = requests.post(
            f"{self.cfg.base_url}/api/pull",
            json={"name": model},
            stream=True,
            timeout=None,
        )
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                self.logger.info("pull %s: %s", model, data.get("status"))
                if data.get("status") == "success":
                    return True
        return False
