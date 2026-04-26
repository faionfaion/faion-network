"""CQRS command-side skeleton: Command base, CommandHandler base, example PlaceOrderCommand."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar
from uuid import UUID

T = TypeVar("T")


@dataclass
class Command(ABC):
    """Base for all commands. Commands change state; never return read models."""


class CommandHandler(ABC, Generic[T]):
    """Base for command handlers. handle() returns None or an ID."""

    @abstractmethod
    async def handle(self, command: T) -> None:
        pass


# --- Example usage ---

@dataclass
class PlaceOrderCommand(Command):
    order_id: UUID
    customer_id: UUID
    items: List[dict]
    shipping_address: dict


class PlaceOrderHandler(CommandHandler[PlaceOrderCommand]):
    def __init__(self, order_repository, event_bus):
        self._order_repository = order_repository
        self._event_bus = event_bus

    async def handle(self, command: PlaceOrderCommand) -> None:
        # 1. Reconstruct / create aggregate
        # 2. Apply domain logic
        # 3. Persist
        # 4. Publish events post-save
        pass
