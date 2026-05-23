"""
purpose: Circuit breaker (CLOSED → OPEN → HALF_OPEN → CLOSED) for inter-service calls.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (microservices-design)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


class State(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_after_sec: int = 30) -> None:
        self.state = State.CLOSED
        self.failures = 0
        self.opened_at: datetime | None = None
        self.failure_threshold = failure_threshold
        self.reset_after = timedelta(seconds=reset_after_sec)

    async def call(self, fn: Callable[..., Awaitable[T]], *args, **kw) -> T:
        if self.state == State.OPEN:
            if self.opened_at and datetime.utcnow() - self.opened_at >= self.reset_after:
                self.state = State.HALF_OPEN
            else:
                raise RuntimeError("circuit open")
        try:
            result = await fn(*args, **kw)
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.state = State.OPEN
                self.opened_at = datetime.utcnow()
            raise
        else:
            self.failures = 0
            self.state = State.CLOSED
            return result
