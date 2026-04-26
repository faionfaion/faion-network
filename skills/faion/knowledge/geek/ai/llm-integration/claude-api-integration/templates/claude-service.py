"""
ClaudeService — production-ready Claude API wrapper with config, retry, and token tracking.

Usage:
    svc = ClaudeService()
    result = svc.complete(
        messages=[{"role": "user", "content": "Hello"}],
        config=ClaudeConfig(system="You are a helpful assistant.")
    )
    print(result["content"], result["usage"])
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import logging
from anthropic import Anthropic, RateLimitError, APIConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


@dataclass
class ClaudeConfig:
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1024
    system: str = ""
    timeout: float = 60.0


class ClaudeService:
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    @retry(
        retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3),
    )
    def complete(
        self,
        messages: List[Dict[str, Any]],
        config: Optional[ClaudeConfig] = None,
    ) -> Dict:
        """Execute completion. Returns {content, model, usage, stop_reason}."""
        cfg = config or ClaudeConfig()
        response = self.client.messages.create(
            model=cfg.model,
            max_tokens=cfg.max_tokens,
            system=cfg.system,
            messages=messages,
            timeout=cfg.timeout,
        )
        if response.stop_reason == "max_tokens":
            raise RuntimeError(f"Response truncated — increase max_tokens (current: {cfg.max_tokens})")
        return {
            "content": response.content[0].text,
            "model": response.model,
            "usage": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
            },
            "stop_reason": response.stop_reason,
        }
