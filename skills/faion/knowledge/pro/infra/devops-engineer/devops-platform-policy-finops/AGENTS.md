---
slug: devops-platform-policy-finops
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Platform governance covers two complementary concerns: policy enforcement (preventing non-compliant workloads from being deployed via OPA/Gatekeeper admission control) and FinOps (providing cost visibility per team/service, pre-deployment cost estimation, and budget controls).
content_id: "e86a88630251e85d"
tags: [policy-as-code, opa, gatekeeper, finops, governance]
---
# Platform Governance: Policy as Code and FinOps Integration

## Summary

**One-sentence:** Platform governance covers two complementary concerns: policy enforcement (preventing non-compliant workloads from being deployed via OPA/Gatekeeper admission control) and FinOps (providing cost visibility per team/service, pre-deployment cost estimation, and budget controls).

**One-paragraph:** Platform governance covers two complementary concerns: policy enforcement (preventing non-compliant workloads from being deployed via OPA/Gatekeeper admission control) and FinOps (providing cost visibility per team/service, pre-deployment cost estimation, and budget controls). Both must be embedded into the platform's golden paths — not bolted on as separate review gates.

## Applies If (ALL must hold)

- Kubernetes clusters serving multiple teams where resource misuse or security misconfiguration is a recurring incident source.
- Orgs with compliance requirements (SOC2, HIPAA, PCI) that mandate container resource limits, non-root execution, and read-only filesystems.
- Teams where cloud costs are growing faster than usage — a signal that provisioning is undisciplined.
- Orgs where finance teams are chasing engineering teams for cost attribution after the fact.

## Skip If (ANY kills it)

- Single-team orgs where informal agreement provides equivalent governance with near-zero overhead.
- Non-Kubernetes environments — OPA/Gatekeeper is Kubernetes-specific; use Sentinel (Terraform Cloud) or AWS Service Control Policies for non-K8s enforcement.
- Early platform adoption phases — policy enforcement before golden paths are established drives developers to shadow infrastructure. Establish golden paths first (Phase 2), enforce policy second (Phase 4).

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
