---
slug: code-review-process
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Standardize PR descriptions, CI checks, and reviewer comment scaffolding so inconsistent review practices don't slow the cycle.
content_id: "b867a9ffee91642f"
tags: [code-review, pull-requests, ci-workflow, review-metrics, process]
---
# Code Review Process

## Summary

**One-sentence:** Standardize PR descriptions, CI checks, and reviewer comment scaffolding so inconsistent review practices don't slow the cycle.

**One-paragraph:** Standardize PR descriptions, CI checks, and reviewer comment scaffolding so inconsistent review practices don't slow the cycle. Use four canonical scenario templates (bug, design, security, performance) and track five health metrics (time to first review, cycle time, rework rate, comment ratio, defect escape rate) to measure process health.

## Applies If (ALL must hold)

- Standardizing PR-description quality: agent fills the template from commit messages, diff, and linked issue.
- Wiring CI checks so human and agent reviewer see the same signal before commenting.
- Generating reviewer comment scaffolding for the four canonical scenarios.
- Tracking weekly review health metrics and producing dashboard reports.

## Skip If (ANY kills it)

- Replacing the human review verdict — process scaffolding only, not approval authority.
- Greenfield repos without established conventions — process amplifies existing bad habits.
- Tiny teams (1-2 developers) where overhead exceeds value — use lightweight inline review.
- Spike or throwaway branches — process overhead does not pay back.

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
