# Trunk-Based Branch by Abstraction

## Summary

**One-sentence:** Produces a Branch-by-Abstraction plan that follows the five steps (Protocol → wrap old → implement new → flag-gated swap → remove old + collapse abstraction), with a step-5 cleanup ticket filed at step-1 merge time.

**One-paragraph:** Branch by Abstraction (BbA) is how teams refactor on trunk without long-lived branches. The methodology produces a five-step plan: (1) introduce an interface/Protocol; (2) wrap the old implementation behind it; (3) implement the new code behind the same interface; (4) flag-gate the swap and validate in production; (5) remove the old implementation and collapse the abstraction back to a direct call. Step 5 is the most-skipped step; this methodology files the step-5 cleanup ticket at step-1 merge time so the obligation outlives the implementation work.

**Ефективно для:**

- Large refactor that cannot fit in a single PR < 200 lines.
- Migrating a payment / auth / storage layer to a new implementation.
- Breaking a long-lived feature branch into a series of trunk-merged increments.
- Replacing a legacy library while keeping production stable.

## Applies If (ALL must hold)

- Project uses feature flags (any provider).
- Codebase compiles + tests green on trunk continuously.
- Refactor target has an interface boundary OR one can be introduced cheaply.
- Team agrees to the step-5 cleanup obligation up front.

## Skip If (ANY kills it)

- Tiny refactors that fit in a single < 200-line PR.
- Trivial renames/internal cleanups without behaviour change.
- Projects without feature-flag infrastructure (apply feature-flags first).
- Cases where the abstraction itself is desirable long-term (then step 5 changes; document explicitly).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Refactor goal + affected modules | design doc | task brief |
| Feature-flag provider + naming convention | string | config |
| Cleanup ticket tracker (e.g., Linear, Jira, .aidocs) | URL or path | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trunk-based-dev-patterns]] | feature-flag mechanics live there; BbA composes with it |
| [[trunk-based-ci-gates]] | trunk stays green during the migration |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-abstraction` | sonnet | design Protocol/interface based on existing call sites |
| `emit-step-plan` | sonnet | write the five-step playbook with cleanup ticket |
| `track-cleanup` | haiku | register cleanup ticket and link to flag |

## Templates

| File | Purpose |
|------|---------|
| `templates/plan.md.j2` | Branch-by-Abstraction five-step playbook skeleton |
| `templates/plan.md` | Branch-by-Abstraction five-step playbook skeleton Generated from `templates/plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/abstraction.py` | Python Protocol skeleton for BbA |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trunk-based-branch-by-abstraction.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trunk-based-dev-patterns]]
- [[trunk-based-ci-gates]]
- [[trunk-based-challenges]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/abstraction.py`

```python
from typing import Protocol
from decimal import Decimal


class PaymentProcessor(Protocol):
    def process(self, amount: Decimal) -> dict: ...


class LegacyProcessor:
    def process(self, amount: Decimal) -> dict:
        return self.old_gateway.charge(amount)


class StripeV2Processor:
    def process(self, amount: Decimal) -> dict:
        return self.stripe.create_charge(amount)


def get_processor(flags) -> PaymentProcessor:
    if flags.is_enabled('billing.use_stripe_v2'):
        return StripeV2Processor()
    return LegacyProcessor()
```

### `templates/artefact.json`

```json
{
  "plan_id": "billing-stripe-v2",
  "flag_name": "billing.use_stripe_v2",
  "cleanup_ticket_id": "OPS-148",
  "steps_in_order": true,
  "current_step": 4,
  "dark_launch_planned": true,
  "one_step_per_pr": true
}
```
