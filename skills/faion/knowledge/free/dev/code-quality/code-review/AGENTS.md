---
slug: code-review
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A systematic examination of source code before merging, using five comment types — BLOCKING (bugs, security, standard violations), SUGGESTION (improvements), NITPICK (style), QUESTION (unclear intent), PRAISE (good code) — and six review categories: correctness, design, maintainability, testing, performance, security.
content_id: "0a8fa2a38e33f9c5"
tags: [code-review, pr-review, quality-gates, collaboration, agent-workflow]
---
# Code Review

## Summary

**One-sentence:** A systematic examination of source code before merging, using five comment types — BLOCKING (bugs, security, standard violations), SUGGESTION (improvements), NITPICK (style), QUESTION (unclear intent), PRAISE (good code) — and six review categories: correctness, design, maintainability, testing, performance, security.

**One-paragraph:** A systematic examination of source code before merging, using five comment types — BLOCKING (bugs, security, standard violations), SUGGESTION (improvements), NITPICK (style), QUESTION (unclear intent), PRAISE (good code) — and six review categories: correctness, design, maintainability, testing, performance, security. Keep PRs under 400 lines; agent review quality drops sharply above that threshold.

## Applies If (ALL must hold)

- All code changes before merging, with at least one human approval required.
- Security-sensitive change classes: auth, data access, file uploads, deserialization — run a dedicated security pass.
- Architectural changes requiring broader review.
- Large refactors where reviewers lack bandwidth for line-by-line scan; agent flags hotspots for human attention.
- Consistency enforcement: PR style, naming, test coverage thresholds.

## Skip If (ANY kills it)

- Non-code reviews (design docs, RFCs, copy edits) — use a doc-review workflow instead.
- Hotfixes during active incidents where speed outweighs review depth.
- Closed-source third-party SDK code where source cannot be loaded.
- One-line dependency bumps — Renovate/Dependabot plus automated tests is sufficient.
- Subjective architecture debates without team context — agent will pick a side arbitrarily.

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

- parent skill: `free/dev/code-quality/`
