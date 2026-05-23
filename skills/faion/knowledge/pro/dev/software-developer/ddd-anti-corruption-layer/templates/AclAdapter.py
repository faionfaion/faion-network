# purpose: infrastructure-layer ACL adapter implementing the domain interface
# consumes: vendor SDK + HTTP transport
# produces: implementation of InventoryChecker
# depends-on: content/01-core-rules.xml, templates/DomainInterface.py
# token-budget-impact: ~250 tokens when loaded as reference

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
