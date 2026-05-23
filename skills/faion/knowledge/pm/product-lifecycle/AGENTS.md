# Product Lifecycle Management

## Summary

**One-sentence:** Four-stage diagnostic (Introduction -> Growth -> Maturity -> Decline) matching stage signals to investment strategy, with explicit transition checkpoints and end-of-life sunset plan.

**One-paragraph:** Quantitative stage classification (growth, churn, NPS, market share), stage-matched investment strategy, written transition memos, mandatory sunset plan on Decline tag, lifecycle-tag-before-roadmap discipline. Output: lifecycle-decision-record markdown + per-product stage memo.

**Ефективно для:**

- Quarterly portfolio review — investment level per shipped продукт.
- Metrics inflection: growth slows від 30% до 8%, churn jumps.
- Pre-roadmap step: tag every product зі stage перед sequencing року.
- End-of-life decision: product declining 3+ quarters, потрібен sunset plan.

## Applies If (ALL must hold)

- Quarterly portfolio review — decide investment level for each shipped product.
- A product hits a metrics inflection (growth slows from 30% to 8%, churn jumps).
- Pre-roadmap step: tag every product with its stage before sequencing the year.
- End-of-life decision: product declining for 3+ quarters.
- Investor or board update: defending why a Maturity product gets retention budget instead of new features.

## Skip If (ANY kills it)

- Single-product team with no portfolio.
- Pre-PMF product where lifecycle stages don't apply yet.
- Agency project (each engagement is finite).
- Stable lifecycle tag <=90 days old without trigger events.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product metrics | growth, churn, NPS, market share | product-analytics |
| Lifecycle tag history | list | previous reviews |
| Market context | competitive landscape | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[portfolio-strategy]] | Horizon framing maps onto the lifecycle stage. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: quantitative classification, stage-investment match, transition memo, mandatory sunset, pre-roadmap tagging | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for lifecycle-decision-record | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vibes-tagging, growth-budget-on-maturity, silent-transition, open-ended-decline | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: collect signals -> classify -> match strategy -> write memo -> sunset if needed | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on portfolio + recent tag | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal-extract` | sonnet | Read metrics + research to extract stage signals. |
| `stage-tag` | haiku | Mechanical match of signals to stage. |
| `transition-memo` | sonnet | Write the transition rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lifecycle-assessment.md` | Lifecycle assessment skeleton. |
| `templates/stage-strategy-guide.md` | Per-stage investment strategy guide. |
| `templates/stage-suggest.sh` | Shell wrapper that suggests stage from metrics input. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-lifecycle.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[portfolio-strategy]]
- [[solo-pivot-decision-framework]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
