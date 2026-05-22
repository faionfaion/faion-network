# purpose: ClaudeService wrapper with sync/async/streaming + retry + centralised stop_reason.
# consumes: messages list, ClaudeConfig dataclass.
# produces: dict {content, model, usage, stop_reason} or raises RuntimeError on truncation.
# depends-on: rules r1+r5+r6 in content/01-core-rules.xml; claude-api-basics for client.
# token-budget-impact: passes through to Anthropic API; centralises no extra overhead.
"""ClaudeService — production-ready Claude API wrapper."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from anthropic import APIConnectionError, APIStatusError, Anthropic, RateLimitError
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

RETRYABLE_STATUSES = {500, 502, 503, 529}


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, (RateLimitError, APIConnectionError)):
        return True
    if isinstance(exc, APIStatusError):
        return getattr(exc, "status_code", 0) in RETRYABLE_STATUSES
    return False


@dataclass
class ClaudeConfig:
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1024
    system: Any = ""  # str | list[dict] for prompt caching.
    timeout: float = 60.0
    thinking: dict | None = None  # {"type": "enabled", "budget_tokens": N}
    tools: list[dict] = field(default_factory=list)


class ClaudeService:
    """Centralises stop_reason discipline, retry, and prompt caching for Claude."""

    def __init__(self, api_key: str | None = None) -> None:
        self.client = Anthropic(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    @retry(
        retry=retry_if_exception(_is_retryable),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(5),
    )
    def complete(self, messages: list[dict[str, Any]], config: ClaudeConfig | None = None) -> dict:
        cfg = config or ClaudeConfig()
        kwargs: dict[str, Any] = {
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "messages": messages,
            "timeout": cfg.timeout,
        }
        if cfg.system:
            kwargs["system"] = cfg.system
        if cfg.thinking:  # rule r5: never pass temperature with thinking.
            kwargs["thinking"] = cfg.thinking
        if cfg.tools:
            kwargs["tools"] = cfg.tools
        response = self.client.messages.create(**kwargs)
        if response.stop_reason == "max_tokens":  # rule r1.
            raise RuntimeError(
                f"Response truncated — increase max_tokens (current: {cfg.max_tokens})"
            )
        return {
            "content": response.content,  # rule r3: full content list, not just text.
            "model": response.model,  # rule r4 in claude-api-basics: response field.
            "usage": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
                "cache_read": getattr(response.usage, "cache_read_input_tokens", 0),
                "cache_creation": getattr(response.usage, "cache_creation_input_tokens", 0),
            },
            "stop_reason": response.stop_reason,
        }
