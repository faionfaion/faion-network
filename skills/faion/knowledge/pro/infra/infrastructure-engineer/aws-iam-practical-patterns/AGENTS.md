---
slug: aws-iam-practical-patterns
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Write least-privilege IAM policies scoped to specific resource ARNs with conditions.
content_id: "c7489e1927102dcc"
tags: [aws, iam, least-privilege, cross-account]
---
# IAM Practical Patterns: Policies, Instance Roles, Cross-Account, Permission Boundaries

## Summary

**One-sentence:** Write least-privilege IAM policies scoped to specific resource ARNs with conditions.

**One-paragraph:** Write least-privilege IAM policies scoped to specific resource ARNs with conditions. Create EC2 instance roles with SSM and CloudWatch access. Configure cross-account AssumeRole with MFA and ExternalId conditions. Apply permission boundaries to prevent privilege escalation in delegated admin scenarios.

## Applies If (ALL must hold)

- Writing IAM policies for application workloads that need access to S3, Secrets Manager, or DynamoDB.
- Creating EC2 instance roles to replace long-lived access keys on servers.
- Setting up cross-account access for a CI/CD pipeline or audit tool.
- Delegating IAM role creation to a team while preventing privilege escalation.

## Skip If (ANY kills it)

- EKS pod-level permissions — use IRSA (IAM Roles for Service Accounts) with OIDC; see the templates.md IRSA pattern.
- Human user management — use IAM Identity Center (SSO) with permission sets, not IAM users.
- Account-wide guardrails — use Service Control Policies (SCPs) at the Organizations level, not IAM policies.

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
