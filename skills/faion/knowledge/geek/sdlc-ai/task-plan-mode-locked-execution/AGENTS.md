---
slug: task-plan-mode-locked-execution
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For any change that touches more than three files or runs longer than ~5 minutes of agent time, the agent must first enter Plan Mode (read-only — no Edit, no Write, no shell side-effects), produce an explicit plan with numbered steps, verification commands, and an Out of scope list, secure human approval, then execute the locked plan.
content_id: "8cf57e5dd871e080"
tags: [plan-mode, locked-execution, agentic-workflow, prompt-injection, approval-gate]
---
# Plan Mode Then Locked Execution

## Summary

**One-sentence:** For any change that touches more than three files or runs longer than ~5 minutes of agent time, the agent must first enter Plan Mode (read-only — no Edit, no Write, no shell side-effects), produce an explicit plan with numbered steps, verification commands, and an Out of scope list, secure human approval, then execute the locked plan.

**One-paragraph:** For any change that touches more than three files or runs longer than ~5 minutes of agent time, the agent must first enter Plan Mode (read-only — no Edit, no Write, no shell side-effects), produce an explicit plan with numbered steps, verification commands, and an Out of scope list, secure human approval, then execute the locked plan. The agent is forbidden from re-planning silently mid-execution; any deviation requires a new approved plan, not an in-flight pivot. Locking the plan before execution closes the prompt-injection window, because untrusted data the model encounters during execution cannot rewrite the agreed steps.

## Applies If (ALL must hold)

- Multi-file refactors and renames touching > 3 files.
- Schema migrations, framework upgrades, dependency major bumps with call-site rewrites.
- Anything with security or data implications (auth, secrets handling, PII flows, prod migrations).
- Long autonomous runs where the human will not review every diff line live.
- Cross-repo changes (worktree fan-out, multi-package monorepo edits).

## Skip If (ANY kills it)

- Trivial single-line edits (typo, log-string change) — plan ceremony exceeds the change.
- Inline autocomplete in an IDE (no autonomous loop, human reviews each suggestion).
- Throwaway scratch sessions on a feature branch that will be force-deleted.
- Tasks already gated by tasks.md from spec-kit — that artifact is the plan; do not double-plan.

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
