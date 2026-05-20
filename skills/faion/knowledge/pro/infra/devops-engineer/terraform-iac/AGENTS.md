---
slug: terraform-iac
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Terraform manages cloud infrastructure declaratively using HCL, tracking state in a remote backend and applying changes via the plan-apply workflow.
content_id: "83d0382a2358167e"
tags: [terraform, infrastructure-as-code, iac, modules, state-management]
---
# Terraform IaC

## Summary

**One-sentence:** Terraform manages cloud infrastructure declaratively using HCL, tracking state in a remote backend and applying changes via the plan-apply workflow.

**One-paragraph:** Terraform manages cloud infrastructure declaratively using HCL, tracking state in a remote backend and applying changes via the plan-apply workflow. The module tree must stay flat (prefer composition over deep nesting), modules must be sized to one logical component (e.g., VPC with subnets/NAT/routing — not single security group rules, not entire application stacks). State must always use a remote backend with encryption, locking, and per-environment isolation.

## Applies If (ALL must hold)

- Multi-cloud or cloud-agnostic infrastructure provisioning
- Team environments where concurrent applies must be serialized (state locking)
- Infrastructure that needs policy-as-code gates (Sentinel, OPA)
- GitOps-style infra where plan output becomes a PR comment

## Skip If (ANY kills it)

- AWS-only shops already deep in CloudFormation — migration cost may not justify switch
- Teams preferring general-purpose languages — use Pulumi (TypeScript/Python/Go)
- Pure Kubernetes resource management — Crossplane or Helm is more native
- Single-developer local prototyping with throwaway infra — local state is acceptable

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
