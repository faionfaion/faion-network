"""
Chain of Responsibility in Python with fluent set_next chaining.

Models a request validation + processing pipeline (auth → rate-limit → handler).
set_next() returns the next handler, enabling builder-style chains:
    auth_handler.set_next(rate_limit_handler).set_next(business_handler)

Use when: multiple handlers may process a request; handler set is configurable.
Skip when: a simple list of functions achieves the same result with less ceremony.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Request:
    user_id: str
    api_key: str
    path: str
    payload: dict = field(default_factory=dict)


@dataclass
class Response:
    status: int
    body: str


# ---------------------------------------------------------------------------
# Abstract handler
# ---------------------------------------------------------------------------
class Handler(ABC):
    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        """Chain the next handler. Returns next for fluent builder syntax."""
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: Request) -> Response | None:
        """Return a Response to short-circuit, or pass_to_next() to continue."""

    def pass_to_next(self, request: Request) -> Response | None:
        if self._next is not None:
            return self._next.handle(request)
        return None


# ---------------------------------------------------------------------------
# Concrete handlers
# ---------------------------------------------------------------------------
VALID_API_KEYS = {"key-abc", "key-xyz"}


class AuthHandler(Handler):
    def handle(self, request: Request) -> Response | None:
        if request.api_key not in VALID_API_KEYS:
            return Response(status=401, body="Unauthorized: invalid API key")
        return self.pass_to_next(request)


class RateLimitHandler(Handler):
    """Trivial in-memory rate limiter (replace with Redis in production)."""

    def __init__(self, max_requests: int = 100) -> None:
        super().__init__()
        self._counts: dict[str, int] = {}
        self._max = max_requests

    def handle(self, request: Request) -> Response | None:
        count = self._counts.get(request.user_id, 0)
        if count >= self._max:
            return Response(status=429, body="Too Many Requests")
        self._counts[request.user_id] = count + 1
        return self.pass_to_next(request)


class RouteHandler(Handler):
    """Final handler: routes to the appropriate business logic by path."""

    def handle(self, request: Request) -> Response | None:
        if request.path == "/ping":
            return Response(status=200, body="pong")
        if request.path.startswith("/api/"):
            return Response(status=200, body=f"Handled {request.path}")
        return Response(status=404, body=f"Not found: {request.path}")


class DefaultHandler(Handler):
    """Fallback if no previous handler returned a Response."""

    def handle(self, request: Request) -> Response | None:
        return Response(status=500, body="No handler produced a response")


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Build chain
    auth = AuthHandler()
    rate_limit = RateLimitHandler(max_requests=3)
    router = RouteHandler()
    fallback = DefaultHandler()

    auth.set_next(rate_limit).set_next(router).set_next(fallback)

    # Valid request
    req = Request(user_id="u1", api_key="key-abc", path="/api/items")
    resp = auth.handle(req)
    print(resp)  # Response(status=200, body='Handled /api/items')

    # Invalid key
    req2 = Request(user_id="u2", api_key="bad-key", path="/api/items")
    resp2 = auth.handle(req2)
    print(resp2)  # Response(status=401, body='Unauthorized: invalid API key')

    # Rate limited (max 3 requests)
    for i in range(4):
        req3 = Request(user_id="u3", api_key="key-xyz", path="/ping")
        resp3 = auth.handle(req3)
        print(f"Request {i + 1}: {resp3}")
    # Requests 1–3: status=200; Request 4: status=429
