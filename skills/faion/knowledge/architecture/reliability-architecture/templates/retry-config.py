"""
Retry with decorrelated jitter — recommended strategy for high-contention
scenarios (AWS/Netflix pattern). Breaks thundering herd by randomising each
client's wait independently rather than synchronising all retries.

Formula: next_sleep = min(cap, random(base, prev_sleep * 3))

Usage:
    result = retry_with_jitter(my_api_call, args=(payload,))

Only retry transient errors. Never retry 4xx client errors (bad request, auth
failure) — retrying them is wasteful and can trigger rate limiting.
"""

import random
import time
import logging
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Transient HTTP status codes safe to retry
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

# Error types that indicate transient infrastructure failures
RETRYABLE_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
)


def retry_with_jitter(
    fn: Callable[..., T],
    args: tuple = (),
    kwargs: dict | None = None,
    max_attempts: int = 4,
    base: float = 0.5,  # seconds
    cap: float = 30.0,  # seconds max sleep
) -> T:
    """
    Execute fn with decorrelated jitter retry on transient failures.

    Raises the last exception if all attempts are exhausted.
    """
    if kwargs is None:
        kwargs = {}

    prev_sleep = base
    last_exc: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            result = fn(*args, **kwargs)
            if attempt > 1:
                logger.info("retry_success", extra={"attempt": attempt})
            return result

        except RETRYABLE_EXCEPTIONS as exc:
            last_exc = exc
            logger.warning(
                "retry_transient_error",
                extra={"attempt": attempt, "max": max_attempts, "error": str(exc)},
            )

        if attempt == max_attempts:
            break

        # Decorrelated jitter: randomise between base and prev_sleep * 3
        sleep_time = min(cap, random.uniform(base, prev_sleep * 3))
        prev_sleep = sleep_time
        logger.debug("retry_sleep", extra={"seconds": round(sleep_time, 2)})
        time.sleep(sleep_time)

    raise last_exc  # type: ignore[misc]


# --- Example: requests wrapper with status-code-based retry ---

import requests  # noqa: E402 (import after stdlib)


def post_with_retry(url: str, payload: dict, timeout: float = 5.0) -> dict:
    """POST with decorrelated jitter retry on transient HTTP errors."""

    def _call():
        resp = requests.post(url, json=payload, timeout=timeout)
        if resp.status_code in RETRYABLE_STATUS_CODES:
            resp.raise_for_status()  # raises HTTPError → caught below
        resp.raise_for_status()  # raise on any 4xx/5xx not already handled
        return resp.json()

    # Wrap HTTPError in a retryable exception only for transient codes
    def _safe_call():
        try:
            return _call()
        except requests.HTTPError as exc:
            if exc.response.status_code in RETRYABLE_STATUS_CODES:
                raise ConnectionError(str(exc)) from exc
            raise  # non-retryable 4xx — propagate immediately

    return retry_with_jitter(_safe_call, max_attempts=4, base=0.5, cap=30.0)
