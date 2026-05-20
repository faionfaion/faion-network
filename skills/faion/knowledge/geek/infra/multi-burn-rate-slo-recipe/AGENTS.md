---
slug: multi-burn-rate-slo-recipe
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Multi Burn Rate Slo Recipe: codified infra practice that turns the recurring 'role-devops-engineer/Observability stack rollout: logs + metrics + traces + SLOs (8 weeks)' decision into a repeatable, auditable artefact.
content_id: "d4c1557351e12447"
tags: [multi-burn-rate-slo-recipe, infra, geek]
---
# Multi Burn Rate Slo Recipe

## Summary

**One-sentence:** Multi Burn Rate Slo Recipe: codified infra practice that turns the recurring 'role-devops-engineer/Observability stack rollout: logs + metrics + traces + SLOs (8 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Multi Burn Rate Slo Recipe addresses the gap identified by the role-devops-engineer/Observability stack rollout: logs + metrics + traces + SLOs (8 weeks) playbook: Google-style multi-window multi-burn-rate alerting is the modern alert pattern. Currently undocumented in faion despite being the natural endpoint for any SLO program. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-devops-engineer/Observability stack rollout: logs + metrics + traces + SLOs (8 weeks) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-devops-engineer/Observability stack rollout: logs + metrics + traces + SLOs (8 weeks) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/infra/devops-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
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
| `templates/multi-burn-rate-slo-recipe.json` | JSON schema for the Multi Burn Rate Slo Recipe output contract |
| `templates/multi-burn-rate-slo-recipe.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-burn-rate-slo-recipe.py` | Enforce Multi Burn Rate Slo Recipe output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/infra/devops-engineer/`
- upstream playbook: `role-devops-engineer/Observability stack rollout: logs + metrics + traces + SLOs (8 weeks)`
