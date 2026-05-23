"""
purpose: Command + CommandHandler skeleton; returns None or ID only.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (cqrs-pattern)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4

T = TypeVar("T")


@dataclass
class Command:
    pass


class CommandHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, cmd: Command) -> T | None: ...


@dataclass
class PlaceOrderCommand(Command):
    user_id: UUID
    items: list[str]


class PlaceOrderHandler(CommandHandler[UUID]):
    async def handle(self, cmd: PlaceOrderCommand) -> UUID:
        # validate, write to event store, return new id
        return uuid4()
