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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ValueObject.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        if self.amount < 0:
            raise ValueError("Money amount must be >= 0")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Money currency must be ISO 4217 (3 chars)")
        object.__setattr__(self, "currency", self.currency.upper())

    def add(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"currency mismatch {self.currency} vs {other.currency}")
```

### `templates/ValueObject.cs`

```csharp
namespace Faion.Domain.Money;

public readonly record struct Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        if (amount < 0) throw new ArgumentOutOfRangeException(nameof(amount), "amount must be >= 0");
        if (string.IsNullOrEmpty(currency) || currency.Length != 3)
            throw new ArgumentException("currency must be ISO 4217 (3 chars)", nameof(currency));
        Amount = amount;
        Currency = currency.ToUpperInvariant();
    }

    public Money Add(Money other)
    {
        EnsureSameCurrency(other);
        return new Money(Amount + other.Amount, Currency);
    }

    public Money Subtract(Money other)
    {
        EnsureSameCurrency(other);
        return new Money(Amount - other.Amount, Currency);
    }

    private void EnsureSameCurrency(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException($"currency mismatch {Currency} vs {other.Currency}");
    }
}
```

### `templates/ValueObject.java`

```java
package faion.domain.money;

import java.math.BigDecimal;

public record Money(BigDecimal amount, String currency) {

    public Money {
        if (amount == null) throw new IllegalArgumentException("amount required");
        if (amount.signum() < 0) throw new IllegalArgumentException("amount must be >= 0");
        if (currency == null || currency.length() != 3)
            throw new IllegalArgumentException("currency must be ISO 4217 (3 chars)");
        currency = currency.toUpperCase();
    }

    public Money add(Money other) {
        ensureSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money subtract(Money other) {
        ensureSameCurrency(other);
        return new Money(amount.subtract(other.amount), currency);
    }

    private void ensureSameCurrency(Money other) {
        if (!currency.equals(other.currency))
            throw new IllegalStateException("currency mismatch " + currency + " vs " + other.currency);
    }
}
```
