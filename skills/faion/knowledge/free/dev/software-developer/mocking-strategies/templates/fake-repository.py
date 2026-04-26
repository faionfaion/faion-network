"""
Fake in-memory repository implementing a UserRepository ABC.
Use in unit tests instead of a database.
Reset state between tests via fake_repo.clear() or a fresh fixture.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from uuid import uuid4


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: "User") -> "User": ...

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional["User"]: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional["User"]: ...


class FakeUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: Dict[str, "User"] = {}
        self.email_index: Dict[str, str] = {}

    def save(self, user: "User") -> "User":
        if not getattr(user, "id", None):
            user.id = str(uuid4())
        self.users[user.id] = user
        self.email_index[user.email] = user.id
        return user

    def find_by_id(self, user_id: str) -> Optional["User"]:
        return self.users.get(user_id)

    def find_by_email(self, email: str) -> Optional["User"]:
        uid = self.email_index.get(email)
        return self.users.get(uid) if uid else None

    def clear(self) -> None:
        self.users.clear()
        self.email_index.clear()
