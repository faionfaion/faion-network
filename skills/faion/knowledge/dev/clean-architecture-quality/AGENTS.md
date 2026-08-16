# Clean Architecture

## Summary

**One-sentence:** Produces a Clean-Architecture module skeleton (entities, use-cases, interface adapters, infrastructure) with inward-only imports enforced by an import-linter contract.

**One-paragraph:** Clean Architecture: four concentric layers with inward-only dependencies. Domain layer has no framework imports; use cases orchestrate entities via repository interfaces; controllers translate transport DTOs to use-case input; infrastructure implements interfaces defined inward. The methodology produces a working module skeleton plus an import-linter contract that machine-enforces the dependency rule.

**Ефективно для:**

- Складна business logic, що має пережити фреймворк/DB.
- Multiple delivery mechanisms (REST + CLI + event handler) — single use-case layer.
- DDD проєкт — Clean Architecture layers мапляться 1:1.
- Import-linter (Python) / ArchUnit (JVM) — enforced layer rule.

## Applies If (ALL must hold)

- Complex business logic that must survive infrastructure changes.
- Long-lived enterprise system where testability + onboarding justifies layer overhead.
- Application served via multiple delivery mechanisms (REST/CLI/event handler).
- Team will enforce layer boundaries via architecture tests.

## Skip If (ANY kills it)

- CRUD app with trivial logic — 4 layers for GET /users is over-engineering.
- Rapid prototype where feature exploration trumps stability.
- Teams unwilling to enforce dependency rule via tests.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bounded context / domain definition | Markdown | domain expert |
| Repository / project layout (clean slate or refactor target) | tree | team |
| Architecture-test tool (import-linter / ArchUnit) | tool | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[domain-driven-design]] | DDD bounded contexts define the entities + use-case names this methodology operationalises |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-layers` | sonnet | Generate domain/application/presentation/infrastructure folders + stubs. |
| `author-import-linter-contract` | sonnet | Write the contract that fails CI on inward-only violations. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/use-case.py` | Clean Architecture use case skeleton with Input/Output dataclasses + dependency injection. |
| `templates/repository-interface.py` | Repository interface owned by the domain layer. |
| `templates/import-linter.ini` | Import-linter contract that enforces inward-only layer dependencies. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[domain-driven-design]]
- [[cqrs-pattern]]
- [[microservices-design]]

## Decision tree

See `content/06-decision-tree.xml`. Tree picks Clean Architecture only when complexity and longevity justify the layer overhead AND the team will enforce the rule with architecture tests.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/use-case.py`

```python
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class UseCase(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    async def execute(self, input_data: InputT) -> OutputT: ...


@dataclass
class CreateUserInput:
    name: str
    email: str


@dataclass
class CreateUserOutput:
    user_id: str
```

### `templates/repository-interface.py`

```python
"""
from abc import ABC, abstractmethod
from typing import Optional


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[object]: ...

    @abstractmethod
    async def save(self, user: object) -> None: ...
```

### `templates/import-linter.ini`

```ini
[importlinter]
root_packages = myapp

[importlinter:contract:layers]
name = Clean architecture layers must point inward
type = layers
layers =
    myapp.presentation
    myapp.application
    myapp.domain
containers =
    myapp.infrastructure
ignore_imports =
```
