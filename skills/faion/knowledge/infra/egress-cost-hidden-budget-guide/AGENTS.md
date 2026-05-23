# Egress Cost Hidden Budget Guide

## Summary

**One-sentence:** Pre-launch + scale-event capacity exercise focused on the hidden cost trio: egress to internet, cross-AZ data, NAT-gateway processing, with per-feature attribution and per-region cap.

**One-paragraph:** Egress + NAT-gateway + cross-AZ are the #1 surprise on cloud bills, often 30-50% of total infra spend. They're hidden because they don't show in the architecture diagram. This methodology forces a pre-launch + per-quarter capacity exercise: identify each egress source (S3 -> internet, RDS -> cross-AZ, NAT-GW -> internet), attribute to features, model worst-case under traffic spike, set per-region caps, and add alerts. Output: egress-budget.yaml with sources + budgets + alert thresholds. Pairs with edge-and-cdn-strategy (CDN cuts egress) and headroom-cost-model (capacity overall).

**Ефективно для:**

- Уникнути 30-50% bill surprise від egress / NAT / cross-AZ.
- Per-feature attribution: яка фіча витрачає X TB/місяць.
- Per-region budget cap: alert до того, як bill пройшов ceiling.
- Pre-launch exercise: модель egress до того, як traffic ramp.

## Applies If (ALL must hold)

- Cloud-hosted workload with global users (egress to internet > GB/day)
- Multi-AZ deployment (cross-AZ traffic non-trivial)
- NAT-gateway in use (NAT processing + per-GB pricing)
- Pre-launch or scale-event (traffic ramp expected)

## Skip If (ANY kills it)

- Single-region single-AZ workload with negligible internet egress — egress < 1% of bill
- Self-hosted hardware (no egress pricing)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Last 90 days of cloud cost data with usage type breakdown | billing export | finance |
| Architecture diagram with data-flow arrows | platform diagram | architect |
| Forecasted traffic ramp (next quarter) | product roadmap | product owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[headroom-cost-model]] | Overall capacity context |
| [[edge-and-cdn-strategy]] | CDN reduces internet egress |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cost_aggregation` | haiku | Arithmetic on cost-explorer rows |
| `attribution_trace` | sonnet | Map source to feature via arch diagram |
| `worst_case_modelling` | opus | Cross-feature projection synthesis |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-egress-cost-hidden-budget-guide.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[edge-and-cdn-strategy]]
- [[headroom-cost-model]]
- [[greenfield-infra-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
