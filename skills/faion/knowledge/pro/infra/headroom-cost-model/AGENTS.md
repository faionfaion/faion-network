---
slug: headroom-cost-model
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Headroom + cost model that captures capacity safety margin per resource, per-resource cost, peak-traffic projection, and triggers a re-evaluation when actual usage crosses 70% of provisioned capacity."
content_id: "d7cf0558c963720c"
complexity: medium
produces: report
est_tokens: 3900
tags: [infra, pro, methodology, capacity, cost-model, headroom]
---

# Headroom Cost Model

## Summary

**One-sentence:** Headroom + cost model that captures capacity safety margin per resource, per-resource cost, peak-traffic projection, and triggers a re-evaluation when actual usage crosses 70% of provisioned capacity.

**One-paragraph:** Capacity planning + cost planning are usually done by different people and meet only at the bill. A headroom-cost model unifies them: per critical resource (compute, db, network), capture provisioned capacity, current utilisation, cost per unit, headroom %. The model alerts when usage crosses 70% (re-provision soon) or 90% (re-provision now), and produces a quarterly capacity report with cost projection for the next quarter. Used together with egress-cost-hidden-budget-guide (egress side) and greenfield-infra-decision-matrix (initial sizing).

**Ефективно для:**

- Capacity safety margin: знаєш, коли треба re-provision.
- Cost projection: квартальний звіт замість bill-shock.
- Alert при 70% usage — не чекай 95% + downtime.
- Unified capacity + cost замість двох розрізнених таблиць.

## Applies If (ALL must hold)

- Production workload with multi-resource architecture (compute + db + network)
- Pre-launch or scale-event with traffic ramp expected
- Cloud spend > $5k/month (model overhead pays back)
- Quarterly review cadence committed by engineering leader

## Skip If (ANY kills it)

- Single small instance (1 EC2, 1 RDS) — overkill
- Pre-product workload — no traffic, no model value

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-resource utilisation metrics | Prometheus / CloudWatch | platform team |
| Cost data with usage breakdown | billing export | finance |
| Capacity targets per resource (e.g. RDS IOPS, EKS node count) | infra docs | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[egress-cost-hidden-budget-guide]] | Egress-side companion model |
| [[greenfield-infra-decision-matrix]] | Initial sizing context |

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
| `utilisation_compute` | haiku | Arithmetic on metrics |
| `projection_synthesis` | opus | Cross-resource forecast from roadmap |
| `anomaly_triage` | sonnet | Bounded judgment on deviation source |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-headroom-cost-model.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[egress-cost-hidden-budget-guide]]
- [[greenfield-infra-decision-matrix]]
- [[edge-and-cdn-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
