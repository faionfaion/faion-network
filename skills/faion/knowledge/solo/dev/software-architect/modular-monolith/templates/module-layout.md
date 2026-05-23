<!-- __faion_header_v1__ -->
<!-- purpose: Reference module layout (Python / Go / Java agnostic). -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#r1-one-context-per-module -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Reference module layout (Python / Go / Java agnostic).","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-one-context-per-module","token_budget_impact":"~150 tokens when loaded"}} -->
# Modular Monolith Layout

```
src/
  orders/
    __public__.py        # public API (only this import path is allowed across modules)
    application/         # use cases
    domain/              # entities, value objects
    infrastructure/      # repository implementations, DB models
  payments/
  inventory/
  users/
  shared/                # cross-cutting only: auth scaffolding, logging
```

Rules
- Cross-module calls go through `__public__.py` only.
- No module imports another module's `domain/`, `application/`, or `infrastructure/`.
- Shared DB instance, one schema per module.
