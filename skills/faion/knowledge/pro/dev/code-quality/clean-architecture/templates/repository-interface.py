"""
purpose: Repository interface owned by the domain layer.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (clean-architecture)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from abc import ABC, abstractmethod
from typing import Optional


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[object]: ...

    @abstractmethod
    async def save(self, user: object) -> None: ...
