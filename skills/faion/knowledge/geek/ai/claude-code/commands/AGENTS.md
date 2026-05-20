---
slug: commands
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use this reference when creating a new command, editing or updating an existing command, or fixing or improving a command.
content_id: "d1ebdd83eaa335b8"
tags: [commands, slash-commands, quick-actions, argument-syntax, tool-whitelisting]
---
# Creating or Updating Commands

## Summary

**One-sentence:** Use this reference when creating a new command, editing or updating an existing command, or fixing or improving a command.

**One-paragraph:** Use this reference when creating a new command, editing or updating an existing command, or fixing or improving a command. Commands are short manual /invoke actions with optional arguments and whitelisted tools. Keep them concise: under 150 lines ideal, max 250.

## Applies If (ALL must hold)

- Exposing a repeatable action to developers with a predictable interface such as /deploy, /commit, /review.
- Wrapping a complex Bash plus context injection sequence that would be tedious to type every session.
- Creating lightweight project-specific shortcuts that do not need the overhead of a full skill or agent.
- Injecting live context, current branch, diff, or environment, at invocation time via !-prefix bash execution.

## Skip If (ANY kills it)

- Workflow requires multiple sequential agents, memory between steps, or parallel subtasks: use a skill or agent instead.
- Action must run automatically, not via manual /invoke: use hooks.
- Logic exceeds approximately 250 lines: split into a skill with SKILL.md.
- Command is project-private and the team does not use faion-network: store locally, gitignore it.

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
