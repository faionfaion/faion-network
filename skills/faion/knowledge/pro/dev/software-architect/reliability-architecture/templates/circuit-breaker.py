"""
Circuit Breaker skeleton using the pybreaker library.

Install: pip install pybreaker
Usage: wrap any external call with @breaker decorator or breaker.call(fn).

Configuration values below are starting points — tune based on:
- Expected p99 latency of the upstream
- Acceptable false-positive open rate (too sensitive → spurious opens)
- Acceptable cascade window (too long open → long degradation)
"""

import pybreaker
import logging
import requests
from functools import wraps

logger = logging.getLogger(__name__)


class CircuitBreakerListener(pybreaker.CircuitBreakerListener):
    """Log and alert on state transitions."""

    def state_change(self, cb, old_state, new_state):
        logger.warning(
            "circuit_breaker_state_change",
            extra={
                "name": cb.name,
                "old_state": old_state.name,
                "new_state": new_state.name,
            },
        )
        # Emit metric for alerting (Prometheus example)
        # circuit_breaker_state.labels(name=cb.name, state=new_state.name).set(1)

    def failure(self, cb, exc):
        logger.error(
            "circuit_breaker_failure",
            extra={"name": cb.name, "error": str(exc)},
        )


# --- Configuration ---
# fail_max: absolute failure count within the rolling window (use count, not
# percentage, for low-traffic services where 1 failure = 50% "rate").
# reset_timeout: seconds to stay open before moving to half-open.
# For the slow-call threshold: treat calls exceeding 2x expected p99 as failures
# by raising an exception in the caller when response time exceeds the threshold.

payment_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=30,
    name="payment-service",
    listeners=[CircuitBreakerListener()],
    # In half-open: accept 1 test request; require 3 successes to close
    # (pybreaker uses success_threshold in CircuitBreaker constructor)
)


def call_payment_service(payload: dict) -> dict:
    """Example external call protected by circuit breaker."""

    @payment_breaker
    def _do_call():
        response = requests.post(
            "https://payment-service/charge",
            json=payload,
            timeout=3.0,  # always set explicit timeout
        )
        response.raise_for_status()
        return response.json()

    try:
        return _do_call()
    except pybreaker.CircuitBreakerError:
        logger.error("circuit_open_fast_fail", extra={"service": "payment"})
        # Return degraded response or raise domain-specific exception
        raise ServiceUnavailableError("Payment service circuit is open")
    except requests.exceptions.Timeout:
        logger.error("payment_timeout")
        raise


class ServiceUnavailableError(Exception):
    pass
