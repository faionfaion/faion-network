# purpose: domain-owned interface for an external dependency (no SDK imports)
# consumes: domain types only
# produces: abstract interface for ACL implementations
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~120 tokens when loaded as reference

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryQuote:
    sku: str
    available: bool
    quantity: int


class InventoryUnavailableError(Exception):
    """Domain error: cannot determine inventory state."""


class ItemNotFoundError(Exception):
    """Domain error: SKU is not known to the inventory system."""


class InventoryChecker(ABC):
    """Domain-owned port for inventory lookups. No vendor types appear here."""

    @abstractmethod
    def quote(self, sku: str) -> InventoryQuote:  # pragma: no cover - interface
        ...
