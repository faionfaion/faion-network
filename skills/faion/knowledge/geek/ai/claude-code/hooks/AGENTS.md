---
slug: hooks
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Hooks are automated scripts that execute at specific lifecycle events (PreToolUse, PostToolUse, SessionStart, Stop, etc.
content_id: "e56957852e893119"
tags: [hooks, automation, security, lifecycle-events, validation]
---
# Claude Code Hooks Reference

## Summary

**One-sentence:** Hooks are automated scripts that execute at specific lifecycle events (PreToolUse, PostToolUse, SessionStart, Stop, etc.

**One-paragraph:** Hooks are automated scripts that execute at specific lifecycle events (PreToolUse, PostToolUse, SessionStart, Stop, etc.) to enforce security policies, auto-approve safe operations, format code, inject context, and audit commands.

## Applies If (ALL must hold)

- Enforcing security policy: block dangerous commands (rm -rf, DROP TABLE) before they execute.
- Auto-approval of known-safe operations to reduce permission prompts in automated pipelines.
- Post-edit formatting: run prettier/ruff/eslint automatically after every Write or Edit.
- Injecting session context (git branch, project name, env) at session start so agents don't have to ask.
- Preventing premature agent exit when tasks are still incomplete (Stop hook).
- Audit logging: record every Bash command for compliance or debugging.

## Skip If (ANY kills it)

- Hook logic is complex enough to warrant a standalone agent — hooks are synchronous, blocking, and have a 60s default timeout.
- You need to modify the model's response rather than the tool execution — hooks operate on tool calls, not text output.
- The action should be user-triggered (on demand), not automatic — use a command or agent instead.
- Hook script has side effects that must be reversible — hooks run before confirmation dialogs.

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

- parent skill: `geek/ai/claude-code/`
