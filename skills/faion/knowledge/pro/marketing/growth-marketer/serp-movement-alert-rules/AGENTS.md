---
slug: serp-movement-alert-rules
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Alerting rule set for SEO operators: Search Console + rank-tracker thresholds (impressions drop, position delta, AI Overview appearance, CTR collapse) catching SERP moves within 48 hours.
content_id: "ac0b0033233d718b"
complexity: medium
produces: config
est_tokens: 4200
tags: [seo, serp, alerting, search-console, ai-overviews, rank-tracking]
---
# SERP Movement Alert Rules

## Summary

**One-sentence:** Alerting rule set for SEO operators: Search Console + rank-tracker thresholds (impressions drop, position delta, AI Overview appearance, CTR collapse) catching SERP moves within 48 hours.

**One-paragraph:** Alerting rule set for SEO operators: Search Console + rank-tracker thresholds (impressions drop, position delta, AI Overview appearance, CTR collapse) catching SERP moves within 48 hours. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- SEO operators / growth marketers що управляють > 50 ranking keywords.
- Сайт > 10k organic visits/mo — варто алертити.
- Після Google algorithm update / AI Overview rollout — встановити detection.
- Перед content refresh sprint — щоб знати які keywords прямо зараз dropping.

## Applies If (ALL must hold)

- Google Search Console connected + >= 90 days data.
- Rank tracker (Ahrefs / Semrush / Sistrix / SE Ranking) tracking >= 50 keywords.
- Alert infrastructure (Slack / PagerDuty / email) configured.

## Skip If (ANY kills it)

- New site < 90 days — baseline too noisy for thresholds.
- < 10 tracked keywords — manual review faster than alerts.
- 0 organic strategy — paid-only сайт; SEO alerts irrelevant.

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
| `templates/config-skeleton.md` | SERP Movement Alert Rules skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in SERP Movement Alert Rules. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-serp-movement-alert-rules.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[content-refresh-sop]]
- [[ai-overview-presence-tracker]]
- [[internal-link-audit]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
