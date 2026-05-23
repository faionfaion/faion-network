---
slug: ops-churn-basics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Computes a baseline churn-measurement report with customer churn rate, MRR churn rate, NRR, and segment breakdowns — gate for any retention intervention.
content_id: "2cb88b8c282360b4"
complexity: medium
produces: report
est_tokens: 4200
tags: [churn, retention, saas-metrics, measurement, health-score]
---
# Churn Basics

## Summary

**One-sentence:** Computes a baseline churn-measurement report with customer churn rate, MRR churn rate, NRR, and segment breakdowns — gate for any retention intervention.

**One-paragraph:** Computes a baseline churn-measurement report with customer churn rate, MRR churn rate, NRR, and segment breakdowns — gate for any retention intervention. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- SaaS / subscription бізнеси що шукають baseline churn rate перед prevention work.
- Quarterly board prep що вимагає customer churn + MRR churn + NRR + segment breakdown.
- Діагностика чи pain — acquisition mix, нові-cohort onboarding, чи aging cohort decay.
- Перед запуском cohort-basics, ops-churn-prevention або health-score алертів.

## Applies If (ALL must hold)

- Subscription / usage-based бізнес що потребує baseline churn rate.
- Mature data: ≥ 3 повні місячні cohorts з ≥ 30 customers each.
- Ownership: визначений власник звіту з доступом до billing + product DB.

## Skip If (ANY kills it)

- Pre-revenue або < 3 повних місяців даних — sample too small.
- Один-time transactional бізнес без subscription — використовуй repeat-purchase rate.
- Annual-only contracts з < 2 renewal cycles.

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
| `content/05-examples.xml` | medium | One worked end-to-end example | 700 |
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
| `templates/report-skeleton.md` | Churn Basics skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Churn Basics. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-churn-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[ops-churn-prevention]]
- [[cohort-basics]]
- [[retention-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
