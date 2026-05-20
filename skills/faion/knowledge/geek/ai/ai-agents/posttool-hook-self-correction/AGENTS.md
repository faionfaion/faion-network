---
slug: posttool-hook-self-correction
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Wire PostToolUse hooks (matcher "Write|Edit") to run linters, formatters, and typecheckers automatically after every file mutation.
content_id: "5bedda8c612d749b"
tags: [hooks, self-correction, validation, code-editing, feedback-loop]
---
# PostToolUse Hook as Self-Correction Loop

## Summary

**One-sentence:** Wire PostToolUse hooks (matcher "Write|Edit") to run linters, formatters, and typecheckers automatically after every file mutation.

**One-paragraph:** Wire PostToolUse hooks (matcher "Write|Edit") to run linters, formatters, and typecheckers automatically after every file mutation. Hook stderr is fed back to the agent as a tool-result error message, so the model SEES the failure on its next turn and rewrites the bad change without needing a manual "now run lint" prompt. This turns a code-editing agent into a self-correcting loop using the deterministic hook layer instead of relying on the model to remember.

## Applies If (ALL must hold)

- Any code-editing agent run with Claude Code's hook system (Bash, Edit, Write tools).
- CI bots and headless runs where no human is around to catch a missed lint.
- Strict-format pipelines: doc generators that must obey markdownlint, JSON producers that must validate against a schema.
- Prepush gates: typecheck on every Edit prevents shipping any or unused imports.

## Skip If (ANY kills it)

- Read-only research agents — there's no mutation to validate, hooks add latency for nothing.
- Slow validators (>5s per call) — hook stalls every Edit; move slow checks to a background job and gate on commit instead.
- Model-driven exploratory tasks where lint failures are expected mid-flight (refactors that span many files) — relax the hook with matcher: "" or scope it to specific paths.

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

- parent skill: `geek/ai/ai-agents/`
