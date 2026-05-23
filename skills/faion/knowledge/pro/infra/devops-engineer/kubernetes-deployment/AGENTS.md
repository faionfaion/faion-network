---
slug: kubernetes-deployment
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Decision record selecting Rolling Update, Blue-Green or Canary deployment strategy with rollback wiring and progressive-delivery gating."
content_id: "19536d42ddccf098"
complexity: medium
produces: decision-record
est_tokens: 4000
tags: [kubernetes, deployment-strategy, blue-green, canary, argo-rollouts]
---
# Kubernetes Deployment Strategies

## Summary

**One-sentence:** Decision record selecting Rolling Update, Blue-Green or Canary deployment strategy with rollback wiring and progressive-delivery gating.

**One-paragraph:** Decision record selecting Rolling Update, Blue-Green or Canary deployment strategy with rollback wiring and progressive-delivery gating. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `decision-record` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-kubernetes-deployment.py` before publication.

**Ефективно для:**

- Вибір deployment-стратегії для нового сервісу.
- Налаштування canary metric-analysis через Argo Rollouts.
- Перехід з Recreate на Rolling Update / Blue-Green.

## Applies If (ALL must hold)

- Input matches the methodology scope (kubernetes-deployment) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `decision-record` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service traffic profile | RPS + acceptable error budget per service | product owner |
| Rollback contract | max time-to-rollback target | release manager |
| Available analysis source | Prometheus / Datadog metric for canary analysis | observability team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kubernetes]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-decision-record-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | ADR-style skeleton with context / options / decision / consequences |
| `templates/_smoke-test.md` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kubernetes-deployment.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[kubernetes]]
- [[gitops]]
- [[helm-charts]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `strategy-matches-state` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
