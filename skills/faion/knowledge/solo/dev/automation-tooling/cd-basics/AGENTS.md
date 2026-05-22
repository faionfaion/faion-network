---
slug: cd-basics
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Continuous Delivery (CD) is the practice of keeping every commit in a deployable state so that production releases require only a manual trigger — not a manual testing campaign.
content_id: "1194c7724ddade5a"
tags: [continuous-delivery, ci-cd, deployment, feature-flags, releasable-commits]
---
# Continuous Delivery Basics

## Summary

**One-sentence:** Continuous Delivery (CD) is the practice of keeping every commit in a deployable state so that production releases require only a manual trigger — not a manual testing campaign.

**One-paragraph:** Continuous Delivery (CD) is the practice of keeping every commit in a deployable state so that production releases require only a manual trigger — not a manual testing campaign. Prerequisites: CI in place, comprehensive automated tests, feature flags, backward-compatible migrations, and IaC. Every change ships through an automated pipeline; the only human gate is the final production deploy button.

## Applies If (ALL must hold)

- Team currently does manual deployments and wants a phased CD roadmap.
- Auditing an existing pipeline against the CI / CD (Delivery) / CD (Deployment) matrix.
- Designing backward-compatible schema migrations (expand-contract pattern) to decouple deploy from data changes.
- Introducing feature flags as the bridge between "code shipped" and "feature released."
- Diagnosing CD blockers: large batches, slow tests, manual gates, non-backward-compatible migrations.

## Skip If (ANY kills it)

- Pipeline YAML and deployment strategy mechanics — read `cd-pipelines/` instead.
- Full GitOps (Argo/Flux) — `pro/infra/cicd-engineer` territory.
- Mobile app store releases — review/policy gates dominate; CD principles apply but tooling diverges.
- Environments with mandatory regulatory release boards — CD is achievable but heavier; this methodology does not cover evidence-capture automation.
- When CI is not yet in place — fix prerequisites first.

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
