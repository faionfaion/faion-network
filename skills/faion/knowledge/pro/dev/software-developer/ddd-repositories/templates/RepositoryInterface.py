# purpose: domain-layer Repository interface; no ORM imports
# consumes: aggregate type only
# produces: abstract port for persistence
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~100 tokens when loaded as reference

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

# import only domain types; the line below is a domain import, not an ORM one
from .order import Order


class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]: ...

    @abstractmethod
    def find_by_external_key(self, key: str) -> Optional[Order]: ...

    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def delete(self, order: Order) -> None: ...
