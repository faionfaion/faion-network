# Gcp Iam Design

## Summary

**One-sentence:** Design GCP IAM strategy: least privilege, predefined roles, service account setup, Workload Identity Federation for GKE, and auditing overly permissive bindings.

**One-paragraph:** GCP IAM controls who can do what on which resource. Every identity (user, group, service account) should receive the minimum role required. Basic roles (Owner/Editor/Viewer) must never be used in production — use predefined or custom roles. Service accounts must never use key files in GKE workloads; use Workload Identity Federation instead.

**Ефективно для:**

- Folder/project hierarchy із політиками IAM на folder-level.
- Service accounts з least-privilege + impersonation замість keys.
- Workload Identity Federation для CI/CD без service-account keys.
- Conditional bindings (resource.name, time, IP) для sensitive ролей.

## Applies If (ALL must hold)

- Designing IAM role assignments for a new project, folder, or organization.
- Setting up service accounts for GKE workloads that need GCP API access.
- Auditing existing IAM bindings for over-permissive roles or unused service accounts.
- Implementing a break-glass access procedure for emergency org admin access.

## Skip If (ANY kills it)

- Single-user personal project without delegated access.
- Network-level controls — use `gcp-networking-vpc` firewall.
- External SaaS auth (OIDC for end users) — use Identity Platform.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource scope | org / folder / project / resource | IAM owner |
| Principal inventory | users / groups / service accounts | directory |
| Sensitive resources | list of resources needing conditions | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-resource-hierarchy]] | Sibling methodology that supplies context required here. |
| [[gcp-security-iam]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-iam-design.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-iam-design.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-iam-design.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-resource-hierarchy]]
- [[gcp-security-iam]]
- [[gcp-org-policies]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-iam-design vs an adjacent sibling).
