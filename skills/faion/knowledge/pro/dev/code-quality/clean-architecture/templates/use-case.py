"""Clean Architecture use case skeleton with Input/Output dataclasses and dependency injection."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class UseCase(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    async def execute(self, input_data: InputT) -> OutputT:
        pass


# --- Example: CreateUser use case ---

@dataclass
class CreateUserInput:
    name: str
    email: str


@dataclass
class CreateUserOutput:
    user_id: str
    name: str
    email: str


class CreateUserUseCase(UseCase[CreateUserInput, CreateUserOutput]):
    def __init__(self, user_repository, unit_of_work, event_publisher):
        self._user_repository = user_repository
        self._unit_of_work = unit_of_work
        self._event_publisher = event_publisher

    async def execute(self, input_data: CreateUserInput) -> CreateUserOutput:
        # 1. Check preconditions via repository
        # 2. Create domain entity
        # 3. Persist via unit_of_work
        # 4. Publish domain events
        # 5. Return output DTO
        raise NotImplementedError
