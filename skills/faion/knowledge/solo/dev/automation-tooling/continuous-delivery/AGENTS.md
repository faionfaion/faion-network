---
slug: continuous-delivery
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Router file for the CD knowledge cluster.
content_id: "358892d60eb7871d"
tags: [continuous-delivery, index, router, deployment, dora-metrics]
---
# Continuous Delivery (Index)

## Summary

**One-sentence:** Router file for the CD knowledge cluster.

**One-paragraph:** Router file for the CD knowledge cluster. Dispatches to cd-basics for principles, prerequisites, expand-contract migrations, and phased adoption roadmap; dispatches to cd-pipelines for YAML, deployment strategies (blue-green, canary, rolling), health checks, and monitoring. Reading this index alone is insufficient — always fan out to the correct child after running the triage checklist below.

## Applies If (ALL must hold)

- Trigger: a user prompt mentions "CD", "continuous delivery", "release pipeline", "deployment automation", "DORA metrics", or "blue-green / canary / rolling" without specifying basics vs. pipeline YAML.
- Trigger: an agent must produce an executive summary of CD using only the Quick Reference and CD vs CI matrix below.
- Trigger: cross-linking another knowledge base (trunk-based-dev, feature-flags, devops-engineer) into a single CD landing page.
- Trigger: auditing CD readiness across multiple services and needing a router to fan out per-service to cd-basics or cd-pipelines.
- Trigger: stakeholder asks "are we doing CD?" — answer requires the matrix here plus a prerequisite check from cd-basics.

## Skip If (ANY kills it)

- Implementation work — open cd-basics or cd-pipelines directly; do not paraphrase from this index.
- Continuous Deployment safety nets (canary analysis, SLO-based rollout gates, automated rollback) — covered in cd-pipelines, not here.
- Team-process change management — Accelerate and The DevOps Handbook are referenced but not unpacked; route to product-operations or pm domains.
- Branching strategy questions — route to trunk-based-dev-principles / trunk-based-dev-patterns.
- Feature-flag system design — route to feature-flags methodology.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/automation-tooling/`
