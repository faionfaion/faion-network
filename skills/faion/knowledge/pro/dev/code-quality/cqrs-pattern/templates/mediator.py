"""
purpose: Type-based Mediator dispatching to the right handler.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (cqrs-pattern)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from typing import Any


class Mediator:
    def __init__(self) -> None:
        self._handlers: dict[type, Any] = {}

    def register(self, message_type: type, handler: Any) -> None:
        self._handlers[message_type] = handler

    async def send(self, message: Any) -> Any:
        handler = self._handlers.get(type(message))
        if handler is None:
            raise KeyError(f"no handler for {type(message).__name__}")
        return await handler.handle(message)
