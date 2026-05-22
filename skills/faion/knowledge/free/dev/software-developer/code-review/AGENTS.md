---
slug: code-review
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: PRs less than 400 lines; CI green before review; style delegated to formatters.
content_id: "0a8fa2a38e33f9c5"
tags: [code-review, pr-process, quality-assurance, team-practices, automation]
---
# Code Review

## Summary

**One-sentence:** PRs less than 400 lines; CI green before review; style delegated to formatters.

**One-paragraph:** PRs less than 400 lines; CI green before review; style delegated to formatters. Reviewers focus on correctness, design, tests, security, observability. LLM-authored PRs need second review.

## Applies If (ALL must hold)

- All PRs in a multi-engineer team — cheapest defect-detection layer.
- Before merging LLM-authored PRs — agent code requires a second pass.
- Security-sensitive paths (auth, payment, IAM, crypto) — mandatory dual review.
- Libraries and SDKs where API surface is sticky and backward compatibility must be enforced.
- Onboarding ramps where junior code benefits from senior review plus automated reviewer.

## Skip If (ANY kills it)

- Trunk-based solo prototypes pre-MVP — review overhead outpaces signal.
- Mechanical refactors from a codemod with green CI and full test coverage on touched code — skim, do not deep-review.
- Vendored or generated code (proto stubs, OpenAPI clients) — review the generator config, not the output.
- Documentation typos — accept fast, do not gate.

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

- parent skill: `free/dev/software-developer/`
