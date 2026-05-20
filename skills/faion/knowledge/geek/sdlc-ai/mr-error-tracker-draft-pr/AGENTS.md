---
slug: mr-error-tracker-draft-pr
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When a production exception crosses a tunable event-count and fixability threshold inside an error tracker (Sentry Seer/Autofix, Bugsink, Rollbar, Starsling), a coding agent ingests the structured signal {stack_trace, breadcrumbs, distributed_trace, linked_repo, recent_diffs}, proposes a code patch plus a regression test, and opens a draft pull request that is bidirectionally linked to the alert.
content_id: "40eadbb6d3d122b7"
tags: [error-tracker, pull-request, sentry, draft-pr, codeowners]
---
# Error-Tracker to Draft-PR Pipeline

## Summary

**One-sentence:** When a production exception crosses a tunable event-count and fixability threshold inside an error tracker (Sentry Seer/Autofix, Bugsink, Rollbar, Starsling), a coding agent ingests the structured signal {stack_trace, breadcrumbs, distributed_trace, linked_repo, recent_diffs}, proposes a code patch plus a regression test, and opens a draft pull request that is bidirectionally linked to the alert.

**One-paragraph:** When a production exception crosses a tunable event-count and fixability threshold inside an error tracker (Sentry Seer/Autofix, Bugsink, Rollbar, Starsling), a coding agent ingests the structured signal {stack_trace, breadcrumbs, distributed_trace, linked_repo, recent_diffs}, proposes a code patch plus a regression test, and opens a draft pull request that is bidirectionally linked to the alert. The PR is never auto-merged: the alert URL lives in the PR body, the alert page links back to the PR, and a human in CODEOWNERS clicks Merge after review. Sentry Seer is the canonical implementation, with min_events: 10 and min_fixability: 0.7 as the standard auto-run gate.

## Applies If (ALL must hold)

- Production runtime errors with a clean stack trace and source map (NullPointer, KeyError, IntegrityError, TypeError).
- Repeatable exceptions whose first frame maps 1:1 to a code line in a linked repository.
- Cross-service errors where a distributed trace already correlates the failure across BE+FE.
- Repos where Sentry, Bugsink, or Rollbar is already wired and SCM Settings can list the GitHub/GitLab repo.

## Skip If (ANY kills it)

- One-off errors below the event threshold (< 10 events) — noisy, expensive, low fixability.
- Errors with no stack trace (network timeout, OOM, kernel panic, SIGKILL) — the agent has nothing to anchor to.
- Business-logic bugs where the "fix" is a product decision, not a code edit — agent will pattern-match the wrong shape.
- Strict-compliance repos where draft PRs from bots are still treated as production code on import — escalate to human-only triage.
- Solo or hackathon repos where the operational overhead exceeds the fix value.

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
