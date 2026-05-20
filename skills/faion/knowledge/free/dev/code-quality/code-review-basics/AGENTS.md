---
slug: code-review-basics
tier: free
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured approach to examining code changes before merge: reviewer reads the diff plus touched files, categorizes findings using Conventional Comments labels (blocking/suggestion/nit/question/praise), and emits at most 20 comments prioritized correctness → security → maintainability → nits.
content_id: "d6c797b1e8e9847d"
tags: [code-review, pr-review, conventional-comments, review-checklist, beginner]
---
# Code Review Basics

## Summary

**One-sentence:** A structured approach to examining code changes before merge: reviewer reads the diff plus touched files, categorizes findings using Conventional Comments labels (blocking/suggestion/nit/question/praise), and emits at most 20 comments prioritized correctness → security → maintainability → nits.

**One-paragraph:** A structured approach to examining code changes before merge: reviewer reads the diff plus touched files, categorizes findings using Conventional Comments labels (blocking/suggestion/nit/question/praise), and emits at most 20 comments prioritized correctness → security → maintainability → nits. PR size cap: 400 changed lines. Agent is never the sole approver on a merge to main.

## Applies If (ALL must hold)

- Pre-review pass on every PR before a human reviewer is assigned.
- Self-review automation for agent-authored diffs before pushing.
- Mentoring junior contributors: agent leaves educational comments with explanations.
- Bulk review of mechanical PRs (dependabot, renovate) where breaking-change risk varies.

## Skip If (ANY kills it)

- Architecture/design PRs needing product context the agent does not have — humans only.
- Security-sensitive merges where regulatory sign-off (PCI, HIPAA) is required — agent advises but cannot approve.
- Trivial single-line fixes already covered by lint + CI — agent comment is noise.
- Repos where rubber-stamping is already the failure mode — adding another approval signal worsens it.

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
