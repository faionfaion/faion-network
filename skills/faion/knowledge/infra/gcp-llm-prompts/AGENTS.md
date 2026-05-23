# Gcp Llm Prompts

## Summary

**One-sentence:** Parameterized LLM prompts for GCP: Terraform generation (VPC, Cloud Run, GKE), security audits, IAM review, connectivity troubleshooting, cost optimization, migration, compliance, and runbooks.

**One-paragraph:** Parameterized LLM prompt templates for GCP infrastructure work: generating Terraform HCL for VPC, firewall, service accounts, Cloud Run, and GKE; security audits and IAM policy reviews; connectivity and Cloud Run troubleshooting; cost optimization and committed-use analysis; architecture documentation, runbooks, and compliance checks.

**Ефективно для:**

- Шаблони prompt-ів для архітектурних оглядів GCP проєктів.
- Стандартизовані prompt-и для cost-review, IAM-audit, network-review.
- Curated промпт-бібліотека для повторюваних аналітичних задач.
- Структуровані output-контракти (JSON Schema) для downstream automation.

## Applies If (ALL must hold)

- Generating Terraform HCL for a new GCP resource (VPC, Cloud Run, GKE, Cloud SQL).
- Auditing an existing GCP configuration for security issues.
- Troubleshooting connectivity (firewall, NAT, VPC-SC) or IAM permission denied errors.
- Planning cost optimization or committed-use discount purchases.
- Generating architecture documentation, runbooks, or change requests.
- Planning a workload or database migration to GCP.

## Skip If (ANY kills it)

- Single-shot ad-hoc prompt — no template reuse needed.
- Non-GCP-architecture LLM tasks.
- Prompts requiring proprietary product data the curated library doesn't cover.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task type | cost-review / iam-audit / network-review / arch-review | user |
| Inputs | project context / configs / billing data | user |
| Output shape contract | JSON Schema | consumer agent |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-overview-cli]] | Sibling methodology that supplies context required here. |
| [[gcp-security-iam]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-spec` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-llm-prompts.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-llm-prompts.md` | Skeleton for the spec artefact this methodology produces. |
| `templates/_smoke-test.md` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-llm-prompts.py` | Validate the spec artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-overview-cli]]
- [[gcp-security-iam]]
- [[gcp-terraform-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-llm-prompts vs an adjacent sibling).
