---
slug: gha-matrix-builds
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use GHA matrix strategy to execute jobs across multiple OS and language-version combinations in parallel.
content_id: "b8e4b56ad9d17cea"
tags: [github-actions, matrix, ci, parallel-testing, multi-platform]
---
# GitHub Actions Matrix Builds

## Summary

**One-sentence:** Use GHA matrix strategy to execute jobs across multiple OS and language-version combinations in parallel.

**One-paragraph:** Use GHA matrix strategy to execute jobs across multiple OS and language-version combinations in parallel. Always set fail-fast: false on test matrices so failures on one axis do not mask results on others. Upload per-combination artifacts using the matrix variables in the artifact name.

## Applies If (ALL must hold)

- Libraries or tools that must support multiple language versions (e.g., Python 3.10/3.11/3.12, Node 18/20/22).
- Applications that ship to or run on multiple operating systems (Linux, Windows, macOS).
- Monorepos where different packages may have differing runtime requirements.
- Any project where a CI failure on one platform should not suppress results from others.

## Skip If (ANY kills it)

- Single-platform, single-version apps — matrix overhead adds noise without value.
- Deployment jobs — matrix is for testing; deploy jobs should run once with a specific artifact.
- Jobs that already take over 30 minutes each — a 3x3 matrix could occupy 9 runner-hours; confirm quota first.

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

- parent skill: `pro/infra/cicd-engineer/`
