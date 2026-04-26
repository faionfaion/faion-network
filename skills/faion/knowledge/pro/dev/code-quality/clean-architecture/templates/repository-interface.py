"""Abstract repository interface template — lives in domain/, implemented in infrastructure/."""
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

EntityT = TypeVar("EntityT")


class Repository(ABC, Generic[EntityT]):
    """Generic repository interface. Subclass per aggregate root."""

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> Optional[EntityT]:
        pass

    @abstractmethod
    async def save(self, entity: EntityT) -> None:
        pass

    @abstractmethod
    async def delete(self, entity: EntityT) -> None:
        pass


# --- Example: UserRepository ---

class UserRepository(Repository):
    """Repository for the User aggregate root."""

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[object]:
        pass

    # Infrastructure implementation in infrastructure/persistence/repositories/user_repository_impl.py
    # Never import the implementation from domain/ or application/
