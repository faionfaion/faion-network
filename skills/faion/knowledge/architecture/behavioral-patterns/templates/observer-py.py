# purpose: Observer pattern template (Python).
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a behavioral-patterns artefact validating against scripts/validate-behavioral-patterns.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
"""
Observer / EventEmitter in Python.
- WeakSet prevents memory leaks when observer objects go out of scope.
- subscribe() returns an unsubscribe callable (no separate unsubscribe method needed).
- Errors in one observer are logged and do not block subsequent observers.

Use when: one-to-many notification; subject doesn't need to know subscribers.
Skip when: one-to-one relationship; use direct injection or a callback instead.
"""
from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any
from weakref import WeakSet

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Observer protocol
# ---------------------------------------------------------------------------
class EventEmitter:
    """Simple synchronous event emitter with WeakSet subscribers."""

    def __init__(self) -> None:
        # event_name → set of observers (weak references)
        # WeakSet: if the observer is garbage-collected, it is automatically removed.
        self._listeners: dict[str, WeakSet[Any]] = {}

    def subscribe(
        self,
        event: str,
        handler: Callable[[dict], None],
    ) -> Callable[[], None]:
        """
        Subscribe handler to event.
        Returns an unsubscribe callable:
            unsub = emitter.subscribe("user.created", my_handler)
            unsub()  # stop receiving events
        """
        if event not in self._listeners:
            self._listeners[event] = WeakSet()
        self._listeners[event].add(handler)

        def unsubscribe() -> None:
            if event in self._listeners:
                self._listeners[event].discard(handler)

        return unsubscribe

    def emit(self, event: str, data: dict | None = None) -> None:
        """Notify all subscribers for event. Errors are logged, not raised."""
        if event not in self._listeners:
            return
        payload = data or {}
        for handler in list(self._listeners[event]):  # copy to allow mutation
            try:
                handler(payload)
            except Exception:
                logger.exception("Error in observer for event %r", event)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    emitter = EventEmitter()

    def on_user_created(data: dict) -> None:
        print(f"[email] Welcome {data['email']}")

    def on_user_created_audit(data: dict) -> None:
        print(f"[audit] User created: {data['user_id']}")

    unsub_email = emitter.subscribe("user.created", on_user_created)
    unsub_audit = emitter.subscribe("user.created", on_user_created_audit)

    emitter.emit("user.created", {"user_id": "u-123", "email": "alice@example.com"})
    # Output:
    #   [email] Welcome alice@example.com
    #   [audit] User created: u-123

    unsub_email()  # stop email notifications

    emitter.emit("user.created", {"user_id": "u-456", "email": "bob@example.com"})
    # Output:
    #   [audit] User created: u-456
