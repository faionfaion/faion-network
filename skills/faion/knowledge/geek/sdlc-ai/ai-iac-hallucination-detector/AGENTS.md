---
slug: ai-iac-hallucination-detector
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "f1162c57f5f7e461"
summary: Pre-merge detector that validates AI-generated Terraform / Helm against the official provider schema, catching invented fields and resource names before they break a plan.
tags: [iac, hallucination, terraform, helm, schema-validation, geek]
---
# AI IaC Hallucination Detector

## Summary

**One-sentence:** A pre-merge detector that validates AI-generated Terraform / Helm / Pulumi against the official provider schema, catching invented resource fields, fabricated resource types, and version-incompatible arguments before they break a plan or surface in production.

**One-paragraph:** AI assistants frequently emit IaC that references resource attributes that do not exist in the current provider version — `aws_s3_bucket.acl` after v4 deprecation, `kubernetes_deployment.spec.strategy.rolling` instead of `rolling_update`, helm-chart values whose keys do not exist in `values.schema.json`. This methodology defines a deterministic detector that loads the provider schema (from Terraform Registry, Pulumi schema, or chart `values.schema.json`), parses every resource in the diff with an AST parser (hcl, helm-go-template), and asserts that every attribute and resource type exists in the schema. Output: a `hallucination-report.json` with each finding tagged by severity and a recommended fix; CI refuses merge until the diff is schema-clean or every finding is waived through CODEOWNERS.

## Applies If (ALL must hold)

- IaC diff was authored or substantially edited by an AI assistant.
- An official provider schema or values schema is available (Terraform Registry, Pulumi registry, chart values.schema.json).
- CI can fetch the schema for the version pinned in the repo.
- The diff is destined for a non-sandbox environment.

## Skip If (ANY kills it)

- Diff is from Renovate / Dependabot — deterministic dependency bumps need different validation.
- IaC uses a provider with no public schema available (rare; document the exception inline).
- The `ai-generated-iac-review-gate` already runs schema validation as part of its drift check — coordinate to avoid double-validation.
- Provider version is unpinned — fix RF-03 first via `ai-generated-iac-review-redflags`.

## Prerequisites

- Provider version pinned in `required_providers` (Terraform) or `version` (Helm).
- A local schema cache or live access to the provider registry.
- Tree-sitter (hcl) or alternative parser available in CI.
- `redflag-scan.py` from the sibling methodology may be reused; this methodology focuses on the schema-validation branch.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/ai-generated-iac-review-redflags` | Sibling: this detector is the AST-validation half of the red-flag catalogue. |
| `geek/sdlc-ai/ai-generated-iac-review-gate` (under `geek/infra/server-craft/`) | Sibling: this detector feeds the gate's drift check. |
| `geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan` | Version pin discipline; required for accurate schema lookup. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: schema-as-source, version-pin requirement, AST parsing required, deprecation warning, no LLM-suggested fixes without re-validation | ~1100 |
| `content/02-output-contract.xml` | essential | Hallucination-report shape, finding kinds, deprecation handling | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: schema stale, partial AST coverage, fix loop divergence | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse-iac-ast` | haiku | Mechanical: tree-sitter parse |
| `schema-validate` | haiku | Mechanical: schema lookup per node |
| `fix-suggest` | sonnet | Bounded judgement: find the correct schema-valid replacement |
| `pr-comment-compose` | sonnet | Structured comment composition |

## Templates

| File | Purpose |
|------|---------|
| `templates/hallucination-report.json` | JSON schema for the hallucination report |
| `templates/pr-comment.md` | Reviewer-facing comment template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/detect.py` | Parse IaC diff; validate against provider schema; emit report | CI on IaC diff |
| `scripts/schema-fetch.sh` | Fetch provider schema for pinned version | Daily / on version change |

## Related

- parent skill: `geek/sdlc-ai/`
- peer methodologies: `ai-generated-iac-review-redflags`, `ai-generated-iac-review-gate`, `ai-base-image-cve-triage`
- external: [Terraform Provider Schemas](https://developer.hashicorp.com/terraform/cli/commands/providers/schema) · [Helm values.schema.json](https://helm.sh/docs/topics/charts/#schema-files) · [Pulumi Schema](https://www.pulumi.com/docs/iac/concepts/resources/properties/)
