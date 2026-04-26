"""Circuit breaker for inter-service HTTP calls. States: CLOSED → OPEN → HALF_OPEN → CLOSED."""
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, TypeVar

T = TypeVar("T")


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_secs: int = 30,
        half_open_max_calls: int = 3,
    ):
        self.name = name
        self._failure_threshold = failure_threshold
        self._recovery_timeout = timedelta(seconds=recovery_timeout_secs)
        self._half_open_max = half_open_max_calls
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0
        self._last_failure_time: datetime | None = None

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        if self._is_open():
            raise CircuitOpenError(f"Circuit {self.name!r} is OPEN")
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _is_open(self) -> bool:
        if self._state == CircuitState.OPEN:
            if self._last_failure_time and (
                datetime.utcnow() - self._last_failure_time > self._recovery_timeout
            ):
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
                return False
            return True
        return False

    def _on_success(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
            if self._half_open_calls >= self._half_open_max:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
        else:
            self._failure_count = 0

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = datetime.utcnow()
        if self._state == CircuitState.HALF_OPEN or self._failure_count >= self._failure_threshold:
            self._state = CircuitState.OPEN
