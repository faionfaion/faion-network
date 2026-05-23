---
slug: ai-iac-hallucination-detector
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Detector that catches AI-fabricated cloud resource types, attribute names, and module paths in Terraform/Pulumi before plan: validates every resource against provider schemas and registry index.
content_id: "ce4634905be15b62"
complexity: medium
produces: report
est_tokens: 4500
tags: [terraform, iac, hallucination, schema-validation, ai-review]
---
# AI IaC Hallucination Detector

## Summary

**One-sentence:** Detector that catches AI-fabricated cloud resource types, attribute names, and module paths in Terraform/Pulumi before plan: validates every resource against provider schemas and registry index.

**One-paragraph:** LLMs frequently fabricate IaC: non-existent resource types (`aws_dynamodb_globaltable` instead of `aws_dynamodb_global_table`), invented attributes (`encryption = true` on a resource that uses `server_side_encryption_configuration`), and bogus module sources (`hashicorp/awesome-stuff/aws`). The detector compares every block against the canonical provider schema (downloaded via `terraform providers schema -json`) and the public registry index, flags unknowns, and emits a structured report. Output gates `plan` — fabrications must be resolved before any apply.

**Ефективно для:**

- An AI agent generated Terraform / OpenTofu / Pulumi / CloudFormation that targets a real cloud account.
- The cloud provider exposes a machine-readable schema (Terraform providers do; CloudFormation has the CFN registry).
- The change has not yet reached `terraform plan` — we want to fail fast, before plan errors leak into shared CI.

## Applies If (ALL must hold)

- An AI agent generated Terraform / OpenTofu / Pulumi / CloudFormation that targets a real cloud account.
- The cloud provider exposes a machine-readable schema (Terraform providers do; CloudFormation has the CFN registry).
- The change has not yet reached `terraform plan` — we want to fail fast, before plan errors leak into shared CI.

## Skip If (ANY kills it)

- The IaC is a documentation example or a generated diagram — not intended to apply.
- The provider is in-house with no published schema; manual review remains the gate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IaC source files | tf/ts/yaml | PR diff |
| Provider schemas | json | `terraform providers schema -json` |
| Registry index snapshot | json | Terraform Registry public API + 24h cache |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace + final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-iac-hallucination-detector` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hallucination-report.json` | Report skeleton |
| `templates/worked-example.md` | End-to-end worked detection narrative |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-iac-hallucination-detector.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
