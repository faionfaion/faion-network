---
slug: mr-graph-vs-diff-reviewer
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Two architectures of AI code reviewers co-exist and behave differently.
content_id: "0efd899c8b9df9c7"
tags: [code-review, pull-request, graph-indexed, diff-only, ai-reviewer]
---
# Graph-Indexed vs Diff-Only AI Reviewers

## Summary

**One-sentence:** Two architectures of AI code reviewers co-exist and behave differently.

**One-paragraph:** Two architectures of AI code reviewers co-exist and behave differently. Diff-only reviewers (Sourcery, GitHub Copilot Code Review, Codeball) read the patch plus its nearest neighbours — fast, cheap, blind to cross-file impact. Graph-indexed reviewers (Greptile, CodeRabbit Pro, Qodo Merge 2.0 multi-agent) build a repo-wide knowledge graph and trace ripple effects — slower, expensive, catch cross-module breakage that the diff-only class misses entirely. Pick diff-only for monorepos with strong module isolation and <100k LOC; pick graph-indexed for legacy/polyglot codebases >500k LOC where one rename quietly breaks five callers.

## Applies If (ALL must hold)

- Selecting an AI reviewer for a new repo or migrating from a basic comment bot.
- Re-evaluating after a repo crosses a size or polyglot threshold (e.g. acquisition, framework migration).
- Auditing an existing reviewer that "feels noisy" or "missed an obvious break" — usually wrong architecture.
- Cost-control reviews where the reviewer line item exceeds the budget for actual incident-prevention value.

## Skip If (ANY kills it)

- One-off open-source contribution flow where the maintainer reads every PR manually anyway.
- Repos with strict zero-third-party-app policy on source — pick a self-hosted PR-Agent variant or skip entirely.
- Tiny PR pipelines (<5 PRs/day) — the per-PR cost difference is negligible; pick on UX, not architecture.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
