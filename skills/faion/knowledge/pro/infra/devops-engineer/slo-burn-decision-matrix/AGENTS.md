---
slug: slo-burn-decision-matrix
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Decision matrix mapping fast-burn vs slow-burn SLO error-budget patterns to specific operational actions (canary halt, ship freeze, focus shift, accept) so error-budget burn becomes deterministic."
content_id: "114215ac771d05c0"
complexity: medium
produces: decision-record
est_tokens: 3700
tags: [slo, error-budget, burn-rate, devops-engineer, decision-matrix, canary]
---

# SLO Burn Decision Matrix

## Summary

**One-sentence:** Decision matrix mapping fast-burn vs slow-burn SLO error-budget patterns to specific operational actions (canary halt, ship freeze, focus shift, accept) so error-budget burn becomes deterministic.

**One-paragraph:** SRE methodology defines fast-burn (14.4h to exhaust budget) and slow-burn (6h over 30d) as alert categories but stops short of the operational decision. Teams without the matrix debate 'what does this mean for us' every time, producing inconsistent responses. This methodology pins a matrix: each burn category × service-class (user-facing critical, async worker, batch, internal) maps to a named action (halt canary, freeze ship, focus shift, accept). Actions have explicit owner, SLA, and revert criteria. Mechanism: burn alert fires → matrix lookup → action triggered → audit log. Primary output: slo-burn-matrix.yaml per portfolio + per-event audit log.

**Ефективно для:**

- Burn alert → deterministic action замість дебатів про 'що це значить'.
- Audit trail: яку action тригерила яка burn category коли.
- Уникнення accept-by-default: matrix робить acceptance явним рішенням.
- Узгодження SRE-команди з product на freeze criteria.

## Applies If (ALL must hold)

- SLOs are defined with explicit objective + window (e.g. 99.9% over 30 days)
- Burn-rate alerting is in place (Prometheus multi-window multi-burn-rate, Datadog, Honeycomb)
- Service catalog includes service-class taxonomy (user-facing / async / batch / internal)
- Team commits to act on burn alerts (not observe-only)

## Skip If (ANY kills it)

- No SLOs defined — define them first (slo-definition-template-per-service-class)
- SLOs aspirational and never breached — calibrate SLOs first
- Single-service shop — overhead exceeds value; use a 3-row simplified table

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| SLO definitions per service | slo.yaml per service | service owners |
| Service-class taxonomy | catalog entries | platform team |
| Burn-rate alert thresholds | alert rules | SRE |
| On-call rotation | PagerDuty / Opsgenie schedule | engineering leader |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[slo-definition-template-per-service-class]] | Defines the SLOs this matrix consumes |
| [[fast-vs-slow-burn-rule]] | Defines fast vs slow burn detection |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `matrix_lookup` | haiku | Deterministic table lookup |
| `action_message_draft` | sonnet | Compose action notification with context |
| `quarterly_tuning_review` | opus | Cross-quarter pattern analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-slo-burn-decision-matrix.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[slo-definition-template-per-service-class]]
- [[fast-vs-slow-burn-rule]]
- [[error-budget-policy-and-freeze-rules]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
