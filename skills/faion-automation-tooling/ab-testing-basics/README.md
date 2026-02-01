---
id: ab-testing-basics
name: "A/B Testing Basics"
domain: DEV
skill: faion-software-developer
category: "development"
---

# A/B Testing Basics

## Overview

A/B testing (split testing) compares two or more variants of a feature to determine which performs better based on defined metrics. It enables data-driven decisions about product changes while minimizing risk.

## When to Use

- Testing UI/UX changes (button colors, layouts, copy)
- Evaluating new features before full rollout
- Optimizing conversion funnels
- Pricing experiments
- Algorithm improvements (search, recommendations)

## Key Principles

- **Statistical significance**: Don't conclude until you have enough data
- **One variable at a time**: Isolate what you're testing
- **Clear hypothesis**: Define expected outcomes before testing
- **Minimize experiment interactions**: Avoid users in multiple conflicting tests
- **Document everything**: Results, learnings, decisions made

## Experiment Design

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Variant:
    name: str
    allocation: float  # 0.0 to 1.0
    description: str = ""


@dataclass
class Metric:
    name: str
    type: str  # "conversion", "continuous", "count"
    primary: bool = False
    direction: str = "increase"  # "increase" or "decrease"


@dataclass
class Experiment:
    id: str
    name: str
    hypothesis: str
    variants: list[Variant]
    metrics: list[Metric]
    status: ExperimentStatus = ExperimentStatus.DRAFT
    target_sample_size: int = 1000
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self) -> list[str]:
        """Validate experiment configuration."""
        errors = []

        # Check variant allocations sum to 1
        total_allocation = sum(v.allocation for v in self.variants)
        if abs(total_allocation - 1.0) > 0.001:
            errors.append(f"Variant allocations must sum to 1.0, got {total_allocation}")

        # Check at least 2 variants
        if len(self.variants) < 2:
            errors.append("Experiment must have at least 2 variants")

        # Check at least one metric
        if not self.metrics:
            errors.append("Experiment must have at least one metric")

        # Check exactly one primary metric
        primary_count = sum(1 for m in self.metrics if m.primary)
        if primary_count != 1:
            errors.append(f"Must have exactly one primary metric, got {primary_count}")

        return errors


# Example experiment definition
checkout_experiment = Experiment(
    id="exp-checkout-v2-2024",
    name="New Checkout Flow",
    hypothesis="The simplified checkout flow will increase conversion rate by 15%",
    variants=[
        Variant("control", 0.5, "Current checkout flow"),
        Variant("treatment", 0.5, "Simplified single-page checkout"),
    ],
    metrics=[
        Metric("checkout_conversion", "conversion", primary=True),
        Metric("cart_abandonment", "conversion", direction="decrease"),
        Metric("time_to_complete", "continuous", direction="decrease"),
        Metric("revenue_per_visitor", "continuous"),
    ],
    target_sample_size=10000,
    owner="checkout-team",
)
```

## Experiment Assignment

```python
import hashlib
from typing import Optional

class ExperimentAssigner:
    """Assigns users to experiment variants deterministically."""

    def __init__(self, experiments: dict[str, Experiment]):
        self.experiments = experiments

    def get_variant(
        self,
        experiment_id: str,
        user_id: str,
        override: Optional[str] = None
    ) -> Optional[str]:
        """Get assigned variant for a user in an experiment."""
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            return None

        if experiment.status != ExperimentStatus.RUNNING:
            return None

        # Allow overrides for testing
        if override and any(v.name == override for v in experiment.variants):
            return override

        # Deterministic assignment using hash
        hash_key = f"{experiment_id}:{user_id}"
        hash_value = int(hashlib.md5(hash_key.encode()).hexdigest(), 16)
        bucket = (hash_value % 10000) / 10000.0

        # Assign to variant based on allocation
        cumulative = 0.0
        for variant in experiment.variants:
            cumulative += variant.allocation
            if bucket < cumulative:
                return variant.name

        return experiment.variants[-1].name

    def get_all_assignments(self, user_id: str) -> dict[str, str]:
        """Get all experiment assignments for a user."""
        assignments = {}
        for exp_id, experiment in self.experiments.items():
            variant = self.get_variant(exp_id, user_id)
            if variant:
                assignments[exp_id] = variant
        return assignments


# Usage
assigner = ExperimentAssigner({"checkout-v2": checkout_experiment})

# Get user's variant
variant = assigner.get_variant("checkout-v2", user_id="user-123")

if variant == "treatment":
    render_new_checkout()
else:
    render_old_checkout()
```

## Anti-patterns

- **Peeking at results**: Checking significance before enough data
- **Multiple testing**: Running many tests without correction
- **Changing experiment mid-run**: Modifying allocation or variants
- **No hypothesis**: Testing without expected outcomes
- **Ignoring segments**: Missing important subgroup differences
- **Too small sample**: Underpowered experiments

## References

- [Trustworthy Online Controlled Experiments](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59)
- [Optimizely Stats Engine](https://www.optimizely.com/optimization-glossary/statistical-significance/)
- [Evan Miller A/B Testing Calculator](https://www.evanmiller.org/ab-testing/)
- [Google Analytics Experiments](https://support.google.com/analytics/answer/1745147)

## Related

- [ab-testing-implementation.md](ab-testing-implementation.md) - Event tracking, analysis, reporting
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate test cases from requirements | haiku | Pattern-based generation |
| Review test coverage gaps | sonnet | Requires code understanding |
| Design test architecture | opus | Complex coverage strategies |

