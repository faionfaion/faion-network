---
slug: cloud-architecture
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Best practices for designing cloud-native applications using the Well-Architected Framework (six pillars: operational excellence, security, reliability, performance efficiency, cost optimisation, sustainability).
content_id: "9bff58b3fdab07b6"
tags: [cloud, well-architected, finops, disaster-recovery, vpc, landing-zone, zero-trust]
---
# Cloud Architecture

## Summary

**One-sentence:** Best practices for designing cloud-native applications using the Well-Architected Framework (six pillars: operational excellence, security, reliability, performance efficiency, cost optimisation, sustainability).

**One-paragraph:** Best practices for designing cloud-native applications using the Well-Architected Framework (six pillars: operational excellence, security, reliability, performance efficiency, cost optimisation, sustainability). Covers AWS/Azure/GCP selection, multi-cloud patterns, landing zone components, VPC network design, zero-trust security layers, FinOps cost strategies, and DR strategies (Backup/Restore - Pilot Light - Warm Standby - Active-Active). The agent uses this document to produce a defensible architecture decision record (ADR) plus IaC scaffolding before any cloud resource is created.

## Applies If (ALL must hold)

- Designing a new cloud-native application or migrating workloads to cloud (greenfield or lift-and-shift)
- Choosing between AWS, Azure, and GCP based on technical and organisational constraints
- Setting up a landing zone for a new cloud environment (accounts, VPC, IAM, logging)
- Optimising cloud costs using FinOps (right-sizing, reserved instances, spot)
- Designing a DR strategy with explicit RTO/RPO targets
- Reviewing an existing architecture against the six Well-Architected pillars before a major release
- Producing or refreshing an Architecture Decision Record (ADR) referenced in the SDD design.md

## Skip If (ANY kills it)

- On-premise-only environments where cloud primitives do not apply
- Single-function serverless refactoring - use serverless-architecture methodology instead
- Application-level performance tuning - this covers infrastructure/architecture, not code
- When the team has no cloud budget or access - design without deployment context is premature
- Edge / IoT-only deployments where the workload never touches a hyperscaler region

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

- parent skill: `pro/dev/software-architect/`
