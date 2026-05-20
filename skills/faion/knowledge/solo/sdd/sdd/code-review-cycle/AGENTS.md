---
slug: code-review-cycle
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured human-AI collaboration for code review running as a 3-step pipeline: (1) AI pre-screen flags style, anti-patterns, and missing tests; (2) parallel review agents (Claude + cross-model) produce structured BLOCK/WARN/NOTE finding lists; (3) a merge step deduplicates findings and produces a unified report.
content_id: "84ffc4248a451289"
tags: [code-review, quality-gates, ai-assistance, sdd, reflexion]
---
# Code Review Cycle

## Summary

**One-sentence:** A structured human-AI collaboration for code review running as a 3-step pipeline: (1) AI pre-screen flags style, anti-patterns, and missing tests; (2) parallel review agents (Claude + cross-model) produce structured BLOCK/WARN/NOTE finding lists; (3) a merge step deduplicates findings and produces a unified report.

**One-paragraph:** A structured human-AI collaboration for code review running as a 3-step pipeline: (1) AI pre-screen flags style, anti-patterns, and missing tests; (2) parallel review agents (Claude + cross-model) produce structured BLOCK/WARN/NOTE finding lists; (3) a merge step deduplicates findings and produces a unified report. Humans address BLOCK items; reflexion feeds review findings back into patterns.md and mistakes.md. AI assists but never replaces human judgment on business logic, architecture decisions, and security context.

## Applies If (ALL must hold)

- After any SDD task execution, before marking the task done — run AI pre-screen + human spot-check
- When PRs consistently exceed 300 lines — AI pre-review reduces noise before human review
- Setting up a multi-model review pipeline (write with Claude, review with a separate model)
- Integrating SDD reflexion: post-review findings feed into patterns.md and mistakes.md
- After detecting a spike in change failure rates — add AI review as a quality gate in CI/CD

## Skip If (ANY kills it)

- Single-file configuration changes — linter is sufficient
- Trivial one-line bug fixes — peer review + merge is faster
- First pass in a new codebase where patterns are not yet established — establish patterns first
- When the human reviewer has deep domain knowledge and AI review produces high false positives

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

- parent skill: `solo/sdd/sdd/`
