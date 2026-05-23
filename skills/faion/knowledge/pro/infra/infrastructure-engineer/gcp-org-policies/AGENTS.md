---
slug: gcp-org-policies
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Implement GCP organization policies to enforce security constraints: restrict resource locations, disable SA key creation, enforce OS Login, require labels, and set up Security Command Center.
content_id: "5567eb868ffae65b"
complexity: medium
produces: config
est_tokens: 4100
tags: [gcp, org-policy, security-baseline, governance, compliance]
---
# Gcp Org Policies

## Summary

**One-sentence:** Implement GCP organization policies to enforce security constraints: restrict resource locations, disable SA key creation, enforce OS Login, require labels, and set up Security Command Center.

**One-paragraph:** Organization policies are mandatory guardrails applied at the org or folder level that override project-level settings. They prevent the most common GCP security misconfigurations: VM external IPs, service account key creation, unapproved resource regions, and missing labels. A security baseline should be applied to every new organization before any teams create resources.

**Ефективно для:**

- Constraint policies на rівні organization (disable SA-keys, restrict regions).
- List/boolean constraints для service-enablement (allowed APIs).
- Resource location restrictions (gcp.resourceLocations) під data residency.
- Inheritance + exceptions через project-level overrides.

## Applies If (ALL must hold)

- Setting up a new GCP organization — apply the security baseline before any teams create resources.
- Hardening an existing organization where teams have been creating resources without constraints.
- Meeting compliance requirements (GDPR, HIPAA, SOC2) that require data residency or access controls.
- Enforcing consistent label usage across all projects for cost allocation.

## Skip If (ANY kills it)

- Project-only deployments without org/folder context.
- User-level IAM bindings — use `gcp-iam-design`.
- Quota management — use Service Quotas API.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Compliance constraints | list of constraint ids | security |
| Scope | org / folder / project | org admin |
| Exception list | projects allowed to override | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-resource-hierarchy]] | Sibling methodology that supplies context required here. |
| [[gcp-iam-design]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-config` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-org-policies.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-org-policies.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-org-policies.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-resource-hierarchy]]
- [[gcp-iam-design]]
- [[gcp-security-iam]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-org-policies vs an adjacent sibling).
