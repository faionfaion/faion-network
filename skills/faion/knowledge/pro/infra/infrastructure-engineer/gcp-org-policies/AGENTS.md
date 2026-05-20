---
slug: gcp-org-policies
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Organization policies are mandatory guardrails applied at the org or folder level that override project-level settings.
content_id: "f5564f780e46d80a"
tags: [gcp, org-policy, security-baseline, governance, compliance]
---
# GCP Organization Policies and Security Baseline

## Summary

**One-sentence:** Organization policies are mandatory guardrails applied at the org or folder level that override project-level settings.

**One-paragraph:** Organization policies are mandatory guardrails applied at the org or folder level that override project-level settings. They prevent the most common GCP security misconfigurations: VM external IPs, service account key creation, unapproved resource regions, and missing labels. A security baseline should be applied to every new organization before any teams create resources.

## Applies If (ALL must hold)

- Setting up a new GCP organization — apply the security baseline before any teams create resources.
- Hardening an existing organization where teams have been creating resources without constraints.
- Meeting compliance requirements (GDPR, HIPAA, SOC2) that require data residency or access controls.
- Enforcing consistent label usage across all projects for cost allocation.

## Skip If (ANY kills it)

- Per-project configuration that does not need to be enforced org-wide — use project-level IAM or Terraform modules instead.
- Fine-grained network rules — org policies are coarse; use VPC firewall rules and VPC Service Controls for network-layer enforcement.

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
