---
slug: gcp-iam-design
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GCP IAM controls who can do what on which resource.
content_id: "3b461dee9a2669fe"
tags: [gcp, iam, service-accounts, workload-identity, least-privilege]
---
# GCP IAM Design and Service Account Strategy

## Summary

**One-sentence:** GCP IAM controls who can do what on which resource.

**One-paragraph:** GCP IAM controls who can do what on which resource. Every identity (user, group, service account) should receive the minimum role required. Basic roles (Owner/Editor/Viewer) must never be used in production — use predefined or custom roles. Service accounts must never use key files in GKE workloads; use Workload Identity Federation instead.

## Applies If (ALL must hold)

- Designing IAM role assignments for a new project, folder, or organization.
- Setting up service accounts for GKE workloads that need GCP API access.
- Auditing existing IAM bindings for over-permissive roles or unused service accounts.
- Implementing a break-glass access procedure for emergency org admin access.

## Skip If (ANY kills it)

- Quick personal projects without production data — overhead of custom roles exceeds value for throwaway work.
- Network-layer access control (firewall rules, VPC Service Controls) — those have separate methodologies.

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

- parent skill: `pro/infra/infrastructure-engineer/`
