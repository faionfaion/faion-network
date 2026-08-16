# Python Basics

## Summary

**One-sentence:** Foundational Python 3.12+ patterns: built-in generics, EAFP, dataclasses, pathlib, uv + ruff + mypy.

**One-paragraph:** Foundational Python patterns for 3.12+ projects: data structures, control flow, functions, OOP, error handling, file I/O, and tooling (uv, ruff, mypy). Use built-in generic syntax (list[int], dict[str, int], X | None); prefer uv for environment and dependency management; use ruff for both lint and format.

**Ефективно для:** розробника, який починає новий 3.12+ проєкт або проводить ревʼю фундаменту — закриває петлю між сучасним синтаксисом і інструментарієм uv/ruff/mypy.

## Applies If (ALL must hold)

- Bootstrapping a fresh Python 3.12+ project (pyproject.toml, uv, ruff, mypy, pytest).
- Code review where the issue is fundamentals: mutable defaults, EAFP misuse, legacy typing imports.
- Onboarding developers from older Python or other languages.
- Migrating 3.9/3.10 syntax to 3.12+ built-in generics and X | None.

## Skip If (ANY kills it)

- Production async services — load python-async instead.
- Framework-specific work — load python-fastapi or django-* methodologies.
- Type-system deep dives — load python-type-hints.
- Tooling/quality setup — load python-code-quality.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python 3.12+ interpreter | binary | uv install |
| Empty repo or pyproject.toml | TOML | repo root |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `none` | Self-contained foundational methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: built-in generics, X | None union, EAFP over LBYL, no mutable defaults, pathlib over os.path, dataclasses for data containers. | ~900 |
| `content/02-output-contract.xml` | essential | Shape: 3.12+ syntax only, no typing.List/Optional/Union, no f-string {var=} debug in prod, dataclasses with frozen=True for immutable, with/context-managers for resources. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: mutable default args, LBYL on hasattr, broad except Exception, legacy typing imports, dict instead of dataclass. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: container = list of plain items? → list. Mixed types? → dataclass. Hashable lookup? → dict. Need set ops? → set. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-project` | haiku | Boilerplate from template. |
| `upgrade-syntax` | sonnet | 3.9/3.10 → 3.12+ rewrite with judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dataclass.py` | Frozen + slotted dataclass skeleton with __post_init__ validation. |
| `templates/pyproject.toml.fragment` | Minimal pyproject for 3.12+: build-system, requires-python, ruff target-version, mypy python_version. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-basics.py` | Lint a module for: typing.List/Optional/Union imports, mutable default args, bare except. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[python-modern-2026]]
- [[python-type-hints]]
- [[python-code-quality]]

## Decision tree

The tree at content/06-decision-tree.xml picks the right primitive (list / dict / set / dataclass / NamedTuple) and the right error pattern (EAFP vs LBYL) for the case at hand. Walk it any time you reach for typing.* imports or hasattr.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/dataclass.py`

```python
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Money:
    amount_cents: int
    currency: str = "EUR"

    def __post_init__(self) -> None:
        if self.amount_cents < 0:
            raise ValueError("Money cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("ISO 4217 currency code expected")
```

### `templates/pyproject.toml.fragment`

```toml
[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "T20", "S", "ASYNC"]

[tool.mypy]
python_version = "3.13"
strict = true

[tool.pytest.ini_options]
addopts = "--strict-markers --cov --cov-fail-under=80 -n auto"
testpaths = ["tests"]
markers = ["integration: requires external services"]
```
