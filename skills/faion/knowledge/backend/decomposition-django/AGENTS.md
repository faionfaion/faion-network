# Decomposition: Django Monolith to Bounded Apps

## Summary

**One-sentence:** Splits a Django monolith into bounded apps by ownership boundaries, locks the dependency graph with import-linter, and migrates models with explicit boundary contracts.

**One-paragraph:** Splits a Django monolith into bounded apps by ownership boundaries, locks the dependency graph with import-linter, and migrates models with explicit boundary contracts. Boundaries follow ownership, not technical layers. import-linter contract enforces app dependency direction; cross-app reaches are confined to a contracts/ module per app. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Django repo > 25k LOC with > 6 apps that import each other freely.
- Tests run > 10 min because they cannot be partitioned by app boundary.
- Team plans to extract one app into its own service in the next 6 months.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Django repo > 25k LOC with > 6 apps that import each other freely.
- Tests run > 10 min because they cannot be partitioned by app boundary.
- Team plans to extract one app into its own service in the next 6 months.

## Skip If (ANY kills it)

- Repo < 5k LOC — premature decomposition costs more than it saves.
- Single-developer project with no horizontal team boundaries to enforce.
- Stack is moving off Django in the next quarter — decompose during the rewrite instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current app graph | import-linter report or pydeps | scripts/scan_imports.py |
| Owner map | YAML: app→team | ops/owners.yaml |
| Top-10 cross-app imports | list | git grep / pydeps top edges |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[django-services]] | Service layer pattern this builds boundaries on top of. |
| [[django-celery]] | Background-task isolation; cross-app calls often go via Celery. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-boundary-map` | opus | Cross-cutting synthesis: read owner map + app graph + business model. |
| `write-import-contract` | sonnet | Mechanical translation of boundary map to importlinter.ini. |
| `migrate-model` | sonnet | Per-model move with foreign-key rewrite. |

## Templates

| File | Purpose |
|------|---------|
| `templates/importlinter.ini` | INI configuration scaffolding the artefact. |
| `templates/contracts.py` | Python scaffold realising the artefact in code. |
| `templates/move_model_migration.py` | Python scaffold realising the artefact in code. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decomposition-django.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-services]]
- [[django-celery]]
- [[modular-monolith]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the Django repo above the decomposition threshold (>25k LOC, >6 apps, ownership leakage)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/importlinter.ini`

```ini
; faion_header_json: {"__faion_header__":{"purpose":"INI configuration scaffolding the artefact.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#ownership-defines-boundary","token_budget_impact":"~150 tokens when loaded"}}
[importlinter]
root_packages =
    apps

[importlinter:contract:layered]
name = Apps follow ownership layers
type = layers
layers =
    apps.notifications
    apps.orders
    apps.payments
    apps.users
```

### `templates/contracts.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Python scaffold realising the artefact in code.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#ownership-defines-boundary","token_budget_impact":"~150 tokens when loaded"}}
"""Decomposition: Django Monolith to Bounded Apps scaffold. See AGENTS.md for context and content/02-output-contract.xml for the contract."""
from __future__ import annotations

# Minimal scaffold for the decomposition-django methodology.
# Replace this stub with real implementation; keep the header intact.

def main() -> int:
    """Entrypoint; returns exit code."""
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### `templates/move_model_migration.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Python scaffold realising the artefact in code.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#ownership-defines-boundary","token_budget_impact":"~150 tokens when loaded"}}
"""Decomposition: Django Monolith to Bounded Apps scaffold. See AGENTS.md for context and content/02-output-contract.xml for the contract."""
from __future__ import annotations

# Minimal scaffold for the decomposition-django methodology.
# Replace this stub with real implementation; keep the header intact.

def main() -> int:
    """Entrypoint; returns exit code."""
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### `templates/_smoke-test.json`

```json
{
  "boundary_id": "decomp-2026-q2",
  "apps": [
    "payments",
    "orders",
    "users",
    "notifications",
    "contracts_shared"
  ],
  "dependency_edges": [
    "payments->users",
    "orders->payments",
    "orders->users",
    "notifications->orders",
    "notifications->payments"
  ],
  "forbidden_edges": [
    "users->payments",
    "users->orders",
    "payments->orders"
  ],
  "owner_map": {
    "payments": "core-platform",
    "orders": "commerce",
    "users": "identity",
    "notifications": "growth",
    "contracts_shared": "core-platform"
  },
  "migration_plan": [
    {
      "model": "Refund",
      "from": "orders",
      "to": "payments",
      "pr": "#812"
    }
  ]
}
```
