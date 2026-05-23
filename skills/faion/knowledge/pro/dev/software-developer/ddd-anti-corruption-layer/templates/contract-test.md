<!-- purpose: outline of contract-test cases for the ACL -->
<!-- consumes: canonical vendor JSON responses -->
<!-- produces: test names + payload shapes to scaffold -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens when loaded as reference -->

# Contract tests for ShopifyInventoryAdapter

| # | Case | Mock response | Expected domain outcome |
|---|------|---------------|-------------------------|
| 1 | SKU exists, available | `{"available": true, "quantity": 7}` 200 | `InventoryQuote(sku, available=True, quantity=7)` |
| 2 | SKU exists, out of stock | `{"available": false, "quantity": 0}` 200 | `InventoryQuote(available=False, quantity=0)` |
| 3 | SKU missing | 404 | raises `ItemNotFoundError(sku)` |
| 4 | Rate limit | 429 | raises `InventoryUnavailableError` |
| 5 | Network failure | `requests.ConnectionError` | raises `InventoryUnavailableError` |

Use `responses` or `pytest-httpx` to pin the mock; record a `cassette.json` next to the test for re-recording when intentional contract changes are agreed with the upstream team.
