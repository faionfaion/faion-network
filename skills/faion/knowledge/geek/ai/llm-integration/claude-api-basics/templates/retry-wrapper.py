# Tenacity-based retry wrapper for Anthropic API calls
# Usage: decorate any function that calls client.messages.create

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from anthropic import RateLimitError, APIStatusError


def anthropic_retry(max_attempts: int = 5, min_wait: float = 1.0, max_wait: float = 60.0):
    """Decorator factory: retry on rate limit (429) and server errors (5xx).

    Usage:
        @anthropic_retry()
        def call_claude(client, messages):
            return client.messages.create(...)
    """
    return retry(
        retry=retry_if_exception_type((RateLimitError, APIStatusError)),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        stop=stop_after_attempt(max_attempts),
    )


# Pre-built default decorator for convenience
default_retry = anthropic_retry()
