<!-- __faion_header_v1__ -->
<!-- purpose: Vertical-slice layout reference (Django/FastAPI-style). -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec -->
<!-- depends-on: content/01-core-rules.xml#r1-monolith-first -->
<!-- token-budget-impact: ~150 tokens when loaded -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Vertical-slice layout reference (Django/FastAPI-style).","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-monolith-first","token_budget_impact":"~150 tokens when loaded"}} -->
# Monolith — Vertical Slice Layout

```
app/
  orders/
    create_order/
      handler.py
      command.py
      repository.py
      dto.py
    cancel_order/
      handler.py
      command.py
  inventory/
    reserve_stock/
      handler.py
  shared/
    auth/
    logging/
```

Rules
- Each feature owns all layers (presentation → application → domain → infrastructure).
- `shared/` reserved for cross-cutting concerns only.
- Forbid base classes spanning slices (no `BaseController`, `BaseService`).
