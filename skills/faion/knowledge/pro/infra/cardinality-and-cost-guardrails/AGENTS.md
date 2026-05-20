---
slug: cardinality-and-cost-guardrails
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Cardinality and Cost Guardrails: codified platform / SRE practice that turns the recurring 'role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend' decision into a repeatable, auditable artefact.
content_id: "285c29ac108ea353"
tags: [cardinality-and-cost-guardrails, infra, pro]
---
# Cardinality and Cost Guardrails

## Summary

**One-sentence:** Cardinality and Cost Guardrails: codified platform / SRE practice that turns the recurring 'role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend' decision into a repeatable, auditable artefact.

**One-paragraph:** Cardinality and Cost Guardrails addresses the gap identified by the role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend playbook: FinOps content covers compute/storage well but completely misses the dominant 2026 obs-cost driver: metric/log cardinality explosion. Concrete recipes (label dropping, recording rules, log volume budgets). Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/cardinality-and-cost-guardrails.json` | JSON schema for the Cardinality and Cost Guardrails output contract |
| `templates/cardinality-and-cost-guardrails.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cardinality-and-cost-guardrails.py` | Enforce Cardinality and Cost Guardrails output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- upstream playbook: `role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend`
