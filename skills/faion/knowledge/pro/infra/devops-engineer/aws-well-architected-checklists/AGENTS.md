---
slug: aws-well-architected-checklists
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Actionable checklists for all six AWS Well-Architected pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) plus new-account setup baseline and pre-production readiness gates.
content_id: "8ee9300e7d97c525"
tags: [aws, well-architected, checklist, security, cost-optimization]
---
# AWS Well-Architected Framework Checklists (2025-2026)

## Summary

**One-sentence:** Actionable checklists for all six AWS Well-Architected pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) plus new-account setup baseline and pre-production readiness gates.

**One-paragraph:** Actionable checklists for all six AWS Well-Architected pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) plus new-account setup baseline and pre-production readiness gates.

## Applies If (ALL must hold)

- Pre-launch review of a new AWS workload before production traffic.
- Quarterly well-architected review for an existing production environment.
- New AWS account baseline setup for security and cost management.
- Post-incident review to identify which checklist items were missing.
- Agent-driven environment audit where each item maps to a verifiable CLI check.

## Skip If (ANY kills it)

- Throwaway sandbox accounts where security overhead exceeds the value.
- Replacing a formal AWS Well-Architected Tool review for compliance documentation — use this as a working checklist alongside the official tool.

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

- parent skill: `pro/infra/devops-engineer/`
