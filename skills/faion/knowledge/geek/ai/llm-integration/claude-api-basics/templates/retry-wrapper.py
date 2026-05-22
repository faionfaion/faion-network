# purpose: Tenacity decorator factory covering 429 + 5xx + 529 + connection errors.
# consumes: a callable that issues client.messages.create or stream.
# produces: a decorated callable that retries up to N times with exp backoff + jitter.
# depends-on: rule r3 in content/01-core-rules.xml.
# token-budget-impact: zero per attempt; total cost scales with retry count.
"""Tenacity-based retry wrapper for Anthropic API calls."""
from __future__ import annotations

from anthropic import APIConnectionError, APIStatusError, RateLimitError
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


def anthropic_retry(max_attempts: int = 5, min_wait: float = 1.0, max_wait: float = 60.0):
    """Decorator factory: retry on 429 + 500/502/503/529 + connection errors."""
    return retry(
        retry=retry_if_exception(_is_retryable),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        stop=stop_after_attempt(max_attempts),
    )


default_retry = anthropic_retry()
