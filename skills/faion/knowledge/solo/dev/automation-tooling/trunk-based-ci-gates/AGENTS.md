---
slug: trunk-based-ci-gates
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Trunk-Based Development requires two quality gates: a fast local pre-commit hook that completes in under one second (lint + type-check on staged files only) and a CI pipeline under 10 minutes wall time that gates merge to main.
content_id: "ca2e1889ee897c68"
tags: [trunk-based-development, ci-cd, pre-commit, github-actions, branch-protection]
---
# CI Gates for Trunk-Based Development

## Summary

**One-sentence:** Trunk-Based Development requires two quality gates: a fast local pre-commit hook that completes in under one second (lint + type-check on staged files only) and a CI pipeline under 10 minutes wall time that gates merge to main.

**One-paragraph:** Trunk-Based Development requires two quality gates: a fast local pre-commit hook that completes in under one second (lint + type-check on staged files only) and a CI pipeline under 10 minutes wall time that gates merge to main. Branch protection must require both. A broken trunk is auto-reverted by bot, never by humans.

## Applies If (ALL must hold)

- Any repository practising trunk-based development that pushes to main at least once per day.
- Setting up a new Python + GitHub Actions project and need a working quality gate from day one.
- Existing CI that takes more than 10 minutes — this pattern shows where to cut.
- Codebases where developers routinely use --no-verify — replace the slow hook causing the habit.

## Skip If (ANY kills it)

- Mobile/desktop projects where the store review cycle makes daily deploys impossible — CI gating still applies but the deploy stage is different.
- Pure data science / notebook repos where pre-commit hook overhead is irrelevant and CI is a batch job, not a merge gate.
- Throwaway prototypes where the overhead of setting up hooks is not justified.

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

- parent skill: `solo/dev/automation-tooling/`
