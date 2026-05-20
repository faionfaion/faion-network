---
slug: ai-generated-iac-review-redflags
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e7fe56015dc3206d"
summary: Reviewer's pattern catalogue of AI-generated IaC red flags — hallucinated provider arguments, invented resource names, drifted version constraints — with a checklist the reviewer scans before approving.
tags: [iac, code-review, ai-codegen, red-flags, sdlc-ai]
---
# AI-Generated IaC Review Red Flags

## Summary

**One-sentence:** A reviewer's pattern catalogue of the eight common AI-generated IaC red flags — hallucinated provider arguments, invented resource names, drifted version constraints, copied secrets, "for_each" misuse, dangling outputs, count-of-list shape mismatches, missing tags — with a checklist the reviewer scans before approving the PR.

**One-paragraph:** AI coding assistants now author the majority of IaC diffs in many shops, but they hallucinate provider arguments (`aws_s3_bucket.acl` after it was deprecated, `kubernetes_deployment.spec.strategy.type = "rolling"` instead of `RollingUpdate`), invent resource names (`aws_route53_zone_record`), drift version constraints (`required_providers.aws` left unpinned), copy secrets verbatim from chat context, misuse `for_each` over indexed lists, leave dangling outputs, and skip tag-mandates. This methodology consolidates the eight catch patterns into a single checklist that the reviewer scans through on every IaC PR. The checklist is paired with regex / AST detectors in `scripts/redflag-scan.py` so the human reviewer focuses on judgement, not pattern matching.

## Applies If (ALL must hold)

- The IaC diff (Terraform, Pulumi, Helm) was authored or substantially edited by an AI assistant.
- The reviewer is human and is the merge gate for the PR.
- A provider schema is available for validation (Terraform Registry, Pulumi schema, Helm chart values schema).
- The PR is not blocked by an upstream gate already (otherwise integrate with `ai-generated-iac-review-gate`).

## Skip If (ANY kills it)

- Diff is a deterministic-tool change (Renovate dependency bump, automated drift-detection commit).
- IaC files only touch comments / formatting.
- Stricter gate already runs `ai-generated-iac-review-gate` end-to-end with the four checks — this catalogue's content is integrated there.
- Reviewer has &lt; 5 minutes and the diff is &gt; 200 lines — escalate; the catalogue assumes a real review.

## Prerequisites

- Provider schema or registry mirror reachable from the review environment.
- `scripts/redflag-scan.py` runs in CI and emits a structured comment on the PR.
- A tag-policy file (`tag-policy.yaml`) declaring required tags per resource type.
- Reviewer has Terraform / Pulumi / Helm syntax familiarity.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/ai-iac-hallucination-detector` | Sibling: covers the schema validation branch in depth. |
| `geek/sdlc-ai/ai-generated-iac-review-gate` (under `geek/infra/server-craft/`) | Sibling: this catalogue feeds the gate's security + drift checks. |
| `geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan` | Provider version constraints fold into supply-chain scan. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: catalogue immutability, provider-schema authoritative, regex-then-AST, secret scrub, tag-policy enforcement | ~1100 |
| `content/02-output-contract.xml` | essential | Red-flag report shape, severity scheme, PR-comment structure | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: schema stale, AI-suggested fix, false-positive flood | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `regex-pre-scan` | haiku | Mechanical: fast pattern match across diff |
| `provider-schema-validate` | haiku | Mechanical: schema lookup |
| `red-flag-classify` | sonnet | Bounded judgement: confirm a flag is real vs false positive |
| `pr-comment-compose` | sonnet | Structured comment composition |

## Templates

| File | Purpose |
|------|---------|
| `templates/redflag-catalogue.md` | The 8-pattern catalogue with examples and counter-examples |
| `templates/redflag-report.json` | JSON schema for the report |
| `templates/tag-policy.yaml` | Required-tags-by-resource-type policy file |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/redflag-scan.py` | Run regex + AST checks against the diff; emit redflag-report.json | CI on IaC diff |
| `scripts/provider-schema-fetch.sh` | Refresh provider schemas from Terraform Registry | Daily |

## Related

- parent skill: `geek/sdlc-ai/`
- peer methodologies: `ai-iac-hallucination-detector`, `ai-generated-iac-review-gate`, `ai-base-image-cve-triage`
- external: [Terraform Registry](https://registry.terraform.io/) · [Pulumi schema](https://www.pulumi.com/registry/) · [tag-policy reference: AWS Tag Editor](https://docs.aws.amazon.com/ARG/latest/userguide/tag-editor.html)
