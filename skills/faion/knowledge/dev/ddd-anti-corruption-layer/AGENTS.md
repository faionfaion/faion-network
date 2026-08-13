# DDD Anti-Corruption Layer: Translation Adapters for External Systems

## Summary

**One-sentence:** Anti-Corruption Layer (ACL) adapter pattern — translate between legacy/external API and your domain model, keeping foreign terminology and exceptions out of the domain.

**One-paragraph:** When integrating with a legacy API, third-party SaaS, or another Bounded Context, importing their client SDK directly into the domain leaks their model into yours: field names, error shapes, eventual data drift. The ACL is an adapter in the infrastructure layer that implements a domain-defined interface (`InventoryChecker`, `PaymentGateway`) speaking the Ubiquitous Language and translates to/from the external system at the boundary. This methodology pins five rules: domain owns the interface, ACL is the only importer of external SDK, errors are translated, fail-safe defaults documented, and integration tests at the ACL boundary. Output: an ACL adapter + interface conforming to `02-output-contract.xml`.

**Ефективно для:**

- Integration with legacy systems whose model conflicts with the new domain.
- Third-party SaaS (Stripe, Twilio) where the SDK changes faster than your domain.
- Cross-bounded-context calls — each context owns its translation.
- Microservice splits where one team should not absorb another's vocabulary.
- AI-generated integrations where the model defaults to inlining SDK calls in services.

## Applies If (ALL must hold)

- An external system or another Bounded Context must be consumed.
- That system's model materially differs from this domain's model.
- The team controls the calling code (not a thin proxy / API gateway only).
- Domain interface can be added without breaking existing code.

## Skip If (ANY kills it)

- Simple HTTP client with no semantic gap — direct call is fine.
- Throwaway integration (one-off migration script) — overhead exceeds benefit.
- External system is owned by the same team and identical model — no corruption to prevent.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| External API docs | OpenAPI / SDK doc | vendor |
| Domain interface sketch | Markdown / source | team |
| Fail-safe policy | spec | spec / SLA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | Domain that the ACL serves. |
| [[ddd-repositories]] | Sibling pattern — repository is an ACL over the database. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: domain-owns-interface, acl-only-sdk-importer, error-translation, fail-safe-documented, contract-tests | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ACL spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: leaked-sdk-types, raw-exceptions, no-failsafe, no-contract-test | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on integration shape → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-domain-interface` | sonnet | Vocabulary judgment. |
| `write-acl-adapter` | sonnet | Translation scaffolding. |
| `write-contract-test` | haiku | Mechanical wire-format pinning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/DomainInterface.py` | Domain-layer interface skeleton |
| `templates/AclAdapter.py` | Infrastructure-layer ACL skeleton |
| `templates/contract-test.md` | Outline of contract test cases |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-anti-corruption-layer.py` | Validate ACL spec against schema | Pre-commit on spec artefact |

## Related

- [[ddd-aggregates]]
- [[ddd-repositories]]
- [[ddd-value-objects]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (semantic gap, integration durability, ownership) to a rule from `01-core-rules.xml`. Use it whenever adding a new external integration to decide whether to build a full ACL or accept a direct SDK call.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/DomainInterface.py`

```python
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
```

### `templates/AclAdapter.py`

```python
from __future__ import annotations

import logging
from typing import Any

# This is the ONLY file in the codebase that imports the vendor SDK.
import requests

from ..domain.inventory import (
    InventoryChecker,
    InventoryQuote,
    InventoryUnavailableError,
    ItemNotFoundError,
)

log = logging.getLogger(__name__)


class ShopifyInventoryAdapter(InventoryChecker):
    """Anti-Corruption Layer for the Shopify Inventory API.

    Fail-safe: on network failure, raise InventoryUnavailableError and let the
    caller decide whether to assume-available or block the order. The default
    consumer of this adapter logs + assumes available, with a 60s retry.
    """

    def __init__(self, base_url: str, token: str, timeout: float = 5.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout = timeout

    def quote(self, sku: str) -> InventoryQuote:
        try:
            resp = requests.get(
                f"{self._base_url}/products/{sku}",
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=self._timeout,
            )
        except requests.RequestException as exc:  # translate to domain error
            log.warning("inventory network failure: %s", exc)
            raise InventoryUnavailableError(str(exc)) from exc

        if resp.status_code == 404:
            raise ItemNotFoundError(sku)
        if resp.status_code >= 500 or resp.status_code == 429:
            raise InventoryUnavailableError(f"upstream {resp.status_code}")
        if resp.status_code != 200:
            raise InventoryUnavailableError(f"unexpected status {resp.status_code}")

        body: dict[str, Any] = resp.json()
        return InventoryQuote(
            sku=sku,
            available=bool(body.get("available", False)),
            quantity=int(body.get("quantity", 0)),
        )
```
