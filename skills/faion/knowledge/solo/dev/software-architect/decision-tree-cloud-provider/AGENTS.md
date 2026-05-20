---
slug: decision-tree-cloud-provider
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Walk this decision tree to choose between AWS, Azure, and GCP.
content_id: "8b6fdcc870da7a70"
tags: [decision-tree, cloud-provider, aws, azure, gcp]
---
# Cloud Provider Selection Decision Tree

## Summary

**One-sentence:** Walk this decision tree to choose between AWS, Azure, and GCP.

**One-paragraph:** Walk this decision tree to choose between AWS, Azure, and GCP. The tree routes first by existing technology investments (Microsoft, Google, or neutral), then by workload type and budget sensitivity. Output: recommended provider, runner-up, cost optimization tips.

## Applies If (ALL must hold)

- Greenfield project with no existing cloud footprint — use the full tree.
- Evaluating a secondary cloud provider for a specific workload (e.g., adding GCP for ML to an AWS-primary architecture).
- Compliance-gated decisions requiring a structured audit of certifications and data residency.
- Cost-sensitive startups comparing sustain-use discounts and free-tier depth.

## Skip If (ANY kills it)

- When a hard organizational or contractual constraint already mandates a provider — skip the tree.
- When evaluating cloud-agnostic deployments (Kubernetes on bare metal, Hetzner) — the tree assumes hyperscaler.
- For single-service evaluations (e.g., "which managed Postgres is cheapest") — that is a service comparison, not a provider decision.

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

- parent skill: `solo/dev/software-architect/`
