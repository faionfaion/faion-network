# Gcp Resource Hierarchy

## Summary

**One-sentence:** Design and configure GCP resource hierarchy (org/folders/projects), naming conventions, required labels, and project setup to enforce governance at scale.

**One-paragraph:** GCP organizes all resources in a 4-level tree: Organization → Folder → Project → Resource. IAM policies and organization constraints flow downward; projects are the billing boundary and API-enablement boundary. Designing this hierarchy upfront prevents costly restructuring later.

**Ефективно для:**

- Organization → Folder (per BU/env) → Project (per workload).
- Policy inheritance + override моделювання.
- Naming conventions для project-id-ів (env-bu-service-purpose).
- Billing-account assignment на folder/project level.

## Applies If (ALL must hold)

- Setting up new GCP organizations or migrating standalone projects into an organization structure.
- Designing folder and project layouts for new teams, environments, or applications.
- Planning multi-environment deployments (dev/staging/prod) with clear separation boundaries.
- Establishing governance and security foundations before teams start creating resources.

## Skip If (ANY kills it)

- Single-project personal account.
- Per-project IAM-only changes — use `gcp-iam-design`.
- Org-policy details — use `gcp-org-policies`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Organisation node | GCP organization id | org admin |
| Folders inventory | BU / env split | leadership |
| Naming convention | project-id pattern | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-iam-design]] | Sibling methodology that supplies context required here. |
| [[gcp-billing-cost]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-spec` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-resource-hierarchy.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-resource-hierarchy.md` | Skeleton for the spec artefact this methodology produces. |
| `templates/_smoke-test.md` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-resource-hierarchy.py` | Validate the spec artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-iam-design]]
- [[gcp-billing-cost]]
- [[gcp-org-policies]]
- [[gcp-overview-cli]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-resource-hierarchy vs an adjacent sibling).
