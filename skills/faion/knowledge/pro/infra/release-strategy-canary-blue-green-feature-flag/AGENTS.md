---
slug: release-strategy-canary-blue-green-feature-flag
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Picks between blue/green vs canary vs feature-flag vs ring deploys per service shape — the higher-level methodology k8s-canary-progressive misses.
content_id: "ab8a9a995f0c8999"
tags: [release-strategy-canary-blue-green-feature-flag, infra, pro]
---

# Release Strategy: Canary / Blue-Green / Feature-Flag

## Summary

**One-sentence:** Picks between blue/green vs canary vs feature-flag vs ring deploys per service shape — the higher-level methodology k8s-canary-progressive misses.

**One-paragraph:** k8s-canary-progressive is a single tactic. A higher-level methodology that picks between strategies per service shape is missing. Output: decision matrix + rollback policy + observation window.

## Applies If (ALL must hold)

- production service with ≥1 release/week
- team has authority to introduce or change release strategy
- observability sufficient to compare canary vs baseline

## Skip If (ANY kills it)

- single deploy per quarter (over-engineered)
- stateless static site (canary irrelevant)
- team without observability (build observability first)

## Prerequisites

- service map: stateless/stateful, traffic profile
- current deploy tooling (Argo Rollouts, Spinnaker, custom)
- feature-flag service if any

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `pro/infra/cicd-engineer` | peer methodology — produces inputs or consumes outputs |
| `geek/sdlc-ai/k8s-canary-progressive` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `pro/infra/cicd-engineer`
- peer methodology: `geek/sdlc-ai/k8s-canary-progressive`
- peer methodology: `pro/infra/incident-response-blameless-playbook`
- external: https://martinfowler.com/bliki/BlueGreenDeployment.html; https://martinfowler.com/articles/feature-toggles.html; https://argo-rollouts.readthedocs.io/
