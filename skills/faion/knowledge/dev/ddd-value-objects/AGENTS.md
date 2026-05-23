# DDD Value Objects: Immutable Self-Validating Domain Types

## Summary

**One-sentence:** DDD Value Object pattern — immutable, identity-free domain types that self-validate in constructor, support value equality, and replace primitive obsession.

**One-paragraph:** A Value Object is defined entirely by its attributes, not by identity. Two Value Objects with the same attributes are equal. They are immutable: operations return new instances rather than mutating. They self-validate in the constructor — an invalid Value Object cannot be constructed. Use them to replace primitive obsession (raw strings, ints, Decimals) with meaningful types (`Money`, `Email`, `Address`, `PhoneNumber`). This methodology pins five rules: immutability, constructor validation, value equality, operations return new instances, no identity field. Output: a value-object class conforming to `02-output-contract.xml`.

**Ефективно для:**

- Replacing raw `Decimal` + `str` currency pairs with `Money`.
- Email / phone / address normalization at construction time.
- Composite identifiers carrying validation rules (`Sku`, `OrderNumber`).
- Read-only DTOs in some languages (Python `dataclass(frozen=True)`).
- Type-safe units of measure (kg vs lbs, USD vs EUR).

## Applies If (ALL must hold)

- The concept has no separate identity — equality is by attributes.
- Validation rules apply at construction time, not later.
- The team's language supports immutability via the type system.
- Existing primitives in the domain carry implicit invariants.

## Skip If (ANY kills it)

- The concept genuinely has identity (`Order`, `Customer`) — use an Entity.
- Performance-critical hot loops where allocation cost dominates.
- Language without immutable record support (legacy Python 2, old Java) — adapt with caution.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain glossary | Markdown | domain owner |
| Existing primitives + their invariants | Markdown / source | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | Value objects compose into aggregates as attributes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: immutability, constructor-validation, value-equality, ops-return-new, no-identity | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for value-object spec | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: mutable-vo, post-construction-validation, hidden-identity | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on identity-need → rule | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-vo-candidate` | sonnet | Primitive obsession scan. |
| `write-value-object-class` | haiku | Mechanical scaffolding. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ValueObject.py` | Python `@dataclass(frozen=True)` skeleton |
| `templates/ValueObject.cs` | C# `record` / `readonly record struct` skeleton |
| `templates/ValueObject.java` | Java `record` skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-value-objects.py` | Validate value-object spec | Pre-commit on spec artefact |

## Related

- [[ddd-aggregates]]
- [[ddd-repositories]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (identity-need, mutation-need) to a rule from `01-core-rules.xml`. Use it whenever about to add a new domain concept and unsure whether it's a Value Object or an Entity.
