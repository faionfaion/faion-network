---
slug: terraform
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Terraform spec: HCL modules, remote state (S3 + DynamoDB or Terraform Cloud), explicit provider version pinning, plan-review-apply gate, drift detection, secret-free state hygiene."
content_id: "a216424d374a52bc"
complexity: medium
produces: code
est_tokens: 4000
tags: [terraform, infrastructure-as-code, hcl, aws, state-management]
---

# Terraform

## Summary

**One-sentence:** Terraform spec: HCL modules, remote state (S3 + DynamoDB or Terraform Cloud), explicit provider version pinning, plan-review-apply gate, drift detection, secret-free state hygiene.

**One-paragraph:** Terraform codifies infrastructure changes in version-controlled HCL, enabling reproducible environments, drift detection, and auditable change history. The wins come from discipline: pinned provider versions, remote state with locking, plan-review-apply in CI (no terraform apply from a laptop), modules over copy-paste, and secret-free state. The losses come from skipping any of those: drifted state, secrets in plaintext state files, modules forked into N copies. This methodology pins the rules + the bootstrap pattern + the audit hooks.

**Ефективно для:**

- Reproducible infra: HCL → identical envs (dev / staging / prod).
- Drift detection через terraform plan в CI на щотижневому cron.
- Plan review в PR замість apply-from-laptop.
- Module reuse через terraform-aws-modules + private registry.

## Applies If (ALL must hold)

- Multi-cloud or single-cloud infra that needs to be reproducible across envs
- Team of >=2 engineers touching infra (state locking needed)
- Compliance requires change history + plan review
- Drift detection needed (manual console changes happen)

## Skip If (ANY kills it)

- Single dev laptop with one EC2 instance — overhead exceeds value
- All resources provisioned via cloud-provider-specific GUI tooling and no automation needed
- Pulumi / CDK already in place and team prefers programming-language IaC — pick one, don't run both

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cloud account + IAM role for Terraform | credentials | platform team |
| Remote state backend (S3 + DynamoDB / TF Cloud) | backend config | platform team |
| CI runner with terraform binary + creds via OIDC | GitHub Actions / GitLab | DevOps lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[secrets-management]] | Secrets injected via env / vault, not state file |
| [[security-as-code]] | Policy gates on plan output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `module_extraction` | sonnet | HCL refactor with judgement on interface |
| `plan_review` | opus | Cross-resource impact analysis |
| `backend_config_fill` | haiku | Template fill |

## Templates

| File | Purpose |
|------|---------|
| `templates/backend.tf` | Backend template |
| `templates/locals.tf` | Locals template |
| `templates/prompt-generate-module.txt` | Prompt generate module template |
| `templates/prompt-security-review.txt` | Prompt security review template |
| `templates/variables.tf` | Variables template |
| `templates/versions.tf` | Versions template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[terraform-iac]]
- [[drift-classification-taxonomy]]
- [[security-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
