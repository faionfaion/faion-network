---
slug: claude-code-hooks
tier: geek
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Claude Code hooks are user-defined shell scripts that execute synchronously at specific lifecycle events (PreToolUse, PostToolUse, UserPromptSubmit, SubagentStart, Stop, SessionStart, PreCompact, PostCompact).
content_id: "38fef7c8a4025908"
tags: [claude-code, hooks, quality-gates, automation, shell-scripting]
---
# Claude Code Hooks

## Summary

**One-sentence:** Claude Code hooks are user-defined shell scripts that execute synchronously at specific lifecycle events (PreToolUse, PostToolUse, UserPromptSubmit, SubagentStart, Stop, SessionStart, PreCompact, PostCompact).

**One-paragraph:** Claude Code hooks are user-defined shell scripts that execute synchronously at specific lifecycle events (PreToolUse, PostToolUse, UserPromptSubmit, SubagentStart, Stop, SessionStart, PreCompact, PostCompact). The core rule: always read stdin fully with `INPUT=$(cat)` as the first command and always return valid JSON on stdout — hooks that ignore stdin or emit invalid JSON break the Claude Code session.

## Applies If (ALL must hold)

- Auto-formatting code after Claude edits a file (PostToolUse + Edit/Write matcher)
- Blocking dangerous git commands before execution (PreToolUse + Bash matcher)
- Saving tmux session state during long agent runs (UserPromptSubmit, SubagentStart)
- Auto-running tests after code changes (PostToolUse + Edit matcher)
- Enforcing coding standards on every edit without manual invocation

## Skip If (ANY kills it)

- Logic that belongs in CI/CD pipelines — hooks run locally and do not replace remote quality gates
- Actions taking more than 10 seconds — blocking hooks make the entire Claude session unresponsive
- Network-dependent validation (external API calls, remote test runners) — latency is unpredictable
- Operations requiring human judgment — hooks are automatic and cannot pause mid-execution
- Environments without `jq` installed — most hook patterns depend on it for JSON parsing

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

- parent skill: `geek/infra/server-craft/`
