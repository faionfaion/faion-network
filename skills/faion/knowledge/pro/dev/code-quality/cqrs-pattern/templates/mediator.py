"""Mediator: routes commands to CommandHandlers and queries to QueryHandlers."""
from typing import Dict, Type, TypeVar

T = TypeVar("T")


class Mediator:
    def __init__(self):
        self._command_handlers: Dict[Type, object] = {}
        self._query_handlers: Dict[Type, object] = {}

    def register_command_handler(self, command_type: Type, handler) -> None:
        self._command_handlers[command_type] = handler

    def register_query_handler(self, query_type: Type, handler) -> None:
        self._query_handlers[query_type] = handler

    async def send(self, command) -> None:
        """Dispatch command — returns None."""
        handler = self._command_handlers.get(type(command))
        if not handler:
            raise LookupError(f"No handler registered for {type(command).__name__}")
        await handler.handle(command)

    async def query(self, query):
        """Dispatch query — returns read model."""
        handler = self._query_handlers.get(type(query))
        if not handler:
            raise LookupError(f"No handler registered for {type(query).__name__}")
        return await handler.handle(query)
