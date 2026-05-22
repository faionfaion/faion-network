---
slug: iac-pr-review-checklist
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Consolidated reviewer-side checklist for IaC / Helm / GHA pull requests covering blast radius, IAM, state safety, secrets, and rollback.
content_id: "dbba442d4a5c664c"
tags: [iac, terraform, helm, github-actions, pr-review, blast-radius, iam, secrets]
---
# IaC PR Review Checklist

## Summary

**One-sentence:** Consolidated reviewer-side checklist for IaC / Helm / GHA pull requests covering blast radius, IAM, state safety, secrets, and rollback.

**One-paragraph:** Terraform, Helm, and GitHub Actions methodologies exist as build guides ("here's how to write a module"), but no consolidated reviewer-side checklist exists — so reviewers ad-hoc inspect and miss the five dimensions that actually cause outages. This methodology defines the five must-check axes (blast_radius, iam_changes, state_safety, secrets_handling, rollback_plan), the per-axis approve/block criteria, the artifacts the PR must produce (plan output, drift report, IAM diff), and the reviewer voice ("I will not approve unless…"). Mechanism: a 24-item checklist scoped per IaC tool, integrated with PR-template automation. Primary output: a PR comment containing the per-axis verdict and a list of blockers.

## Applies If (ALL must hold)

- PR touches Terraform / OpenTofu / Pulumi / CloudFormation / Helm / GHA workflow files
- target environment is staging, pre-prod, or production (not personal sandbox)
- repository has branch protection requiring ≥ 1 reviewer
- IaC tool runs in CI with plan / dry-run output available to reviewer
- reviewer has read access to IAM / state backend / secrets manager

## Skip If (ANY kills it)

- pure docs / README change with no .tf / .yaml / .yml diff
- experimental sandbox account with no production blast radius
- read-only data-source addition with no resource creation (use lighter review)
- automated infra-bot PR with idempotent renames only (e.g., tag normalization)
- pre-prod ephemeral environment torn down nightly

## Prerequisites (must be true before starting)

- PR contains automatically-attached plan / dry-run output
- repo has documented "blast radius tiers" (e.g., S0/S1/S2/S3) mapped to environments
- IAM-change diff visible in the PR or linked artifact
- secrets-scanning bot has run and passed
- rollback procedure documented in repository (RUNBOOK.md or per-module section)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/terraform-state-best-practices` | State-safety axis criteria |
| `pro/infra/devops-engineer/aws-iam-practical-patterns` | IAM-diff interpretation guidance |
| `pro/infra/devops-engineer/image-digest-pinning-policy` | One sub-axis of secrets / supply-chain hardening |
| `pro/infra/cicd-engineer/github-actions-security` | GHA-specific reviewer rules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 axes: blast radius, IAM, state safety, secrets, rollback — each with block criteria | ~1000 |
| `content/02-output-contract.xml` | essential | Reviewer PR-comment schema, verdict format, blocker list | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (rubber-stamp, ignored plan, hidden IAM escalation, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan_output_diff_classifier` | sonnet | Tag each plan-output line by axis + risk |
| `iam_diff_summarizer` | sonnet | Convert raw IAM policy diff to human summary |
| `blast_radius_estimator` | sonnet | Map resources to tier (S0-S3) using ownership map |
| `pr_comment_draft` | sonnet | Compose final reviewer comment with verdict per axis |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-review-comment.md` | Per-axis verdict skeleton for the final reviewer comment |
| `templates/blast-radius-tiers.md` | Tier definitions (S0 = global outage, S3 = sandbox-only) |
| `templates/iam-diff-rubric.md` | What to look for in an IAM policy diff |
| `templates/rollback-plan-template.md` | Required rollback fields per resource type |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/tf-plan-summarizer.py` | Parse plan output, classify per axis | Reviewer pre-review |
| `scripts/iam-diff-extractor.py` | Extract IAM-policy delta between base + head | Reviewer pre-review |
| `scripts/secrets-trip-check.sh` | Scan diff for likely secrets and exposure patterns | Reviewer pre-review |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `image-digest-pinning-policy`, `terraform-state-best-practices`
- external: [HashiCorp PR Guide](https://developer.hashicorp.com/terraform/cloud-docs/run/ui) · [GHA security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
