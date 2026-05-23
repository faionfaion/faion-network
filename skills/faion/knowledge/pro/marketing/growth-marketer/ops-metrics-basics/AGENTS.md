---
slug: ops-metrics-basics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 5-10 actionable SaaS metrics with collection plan, target + alert thresholds, and a tiered review cadence (daily pulse / weekly review / monthly deep-dive).
content_id: "75d436d234aa7450"
complexity: medium
produces: config
est_tokens: 4200
tags: [metrics, operations, saas, analytics, kpi, dashboard]
---
# Ops Metrics Basics

## Summary

**One-sentence:** 5-10 actionable SaaS metrics with collection plan, target + alert thresholds, and a tiered review cadence (daily pulse / weekly review / monthly deep-dive).

**One-paragraph:** 5-10 actionable SaaS metrics with collection plan, target + alert thresholds, and a tiered review cadence (daily pulse / weekly review / monthly deep-dive). The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Solopreneur або small team що тільки запустив SaaS і потребує metric foundation.
- Team що тоне в дашбордах і хоче скоротити до 5-10 actionable metrics.
- Перед board / investor reporting setup, щоб уніфікувати definitions.
- Перед dashboard rebuild — спершу defined metric set, потім UI.

## Applies If (ALL must hold)

- Subscription business з MRR > $1k, або equivalent transaction volume.
- Доступ до billing data (Stripe / Paddle / equivalent) + product analytics.
- Команда здатна owned >= 1 metric review cadence (weekly mandatory).

## Skip If (ANY kills it)

- Pre-revenue / pre-launch — використовуй leading product metrics замість.
- Enterprise з 50+ KPI що вже інстальовані — це consolidation problem, не basics.
- Один-off transactional бізнес без recurring — використовуй repeat-purchase metrics.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-skeleton.md` | Ops Metrics Basics skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Ops Metrics Basics. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-metrics-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[ops-churn-basics]]
- [[north-star-metric]]
- [[retention-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
