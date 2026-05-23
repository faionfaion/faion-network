"""
purpose: Clean Architecture use case skeleton with Input/Output dataclasses + dependency injection.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (clean-architecture)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class UseCase(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    async def execute(self, input_data: InputT) -> OutputT: ...


@dataclass
class CreateUserInput:
    name: str
    email: str


@dataclass
class CreateUserOutput:
    user_id: str
