---
slug: retention-metrics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Locked-formula retention metric set: D1/D7/D30 cohort retention, DAU/MAU ratio, monthly churn, churn-risk score — each with single canonical SQL.
content_id: "26697c7992f1d07b"
complexity: medium
produces: config
est_tokens: 4200
tags: [retention, metrics, cohort, churn, engagement, dau-mau]
---
# Retention Metrics

## Summary

**One-sentence:** Locked-formula retention metric set: D1/D7/D30 cohort retention, DAU/MAU ratio, monthly churn, churn-risk score — each with single canonical SQL.

**One-paragraph:** Locked-formula retention metric set: D1/D7/D30 cohort retention, DAU/MAU ratio, monthly churn, churn-risk score — each with single canonical SQL. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Product teams що мають active product analytics (Amplitude, Mixpanel, PostHog, або equivalent).
- Перед запуском retention-strategies — спершу defined metric set.
- Якщо різні reports показують різні retention numbers — це consolidation cue.
- Перед board / investor narrative про product-market fit.

## Applies If (ALL must hold)

- Product з >= 30 daily active users + >= 90 days history (cohort stability).
- Доступ до event log (login, session, key-action events) + billing data.
- Team здатний на SQL / Looker / Mode-level metric definitions.

## Skip If (ANY kills it)

- Pre-launch або < 30 DAU — sample too small.
- Pure marketing site без login / session — використовуй traffic metrics.
- Transactional бізнес без recurring — use repeat-purchase metrics instead.

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
| `templates/config-skeleton.md` | Retention Metrics skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Retention Metrics. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retention-metrics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[ops-churn-basics]]
- [[ops-metrics-basics]]
- [[retention-strategies]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
