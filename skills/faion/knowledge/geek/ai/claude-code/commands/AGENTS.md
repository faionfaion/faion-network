---
slug: commands
tier: geek
group: ai
domain: claude-code
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Spec for /invoke commands under 250 lines: clear argument syntax, tool whitelist, !-prefix bash for live context, no overhead of skills or agents.
content_id: "5899863bc6c17640"
complexity: medium
produces: config
est_tokens: 4400
tags: [claude-code, commands, slash-commands, quick-actions, tool-whitelisting]
---
# Creating or Updating Claude Code Commands

## Summary

**One-sentence:** Spec for /invoke commands under 250 lines: clear argument syntax, tool whitelist, !-prefix bash for live context, no overhead of skills or agents.

**One-paragraph:** Commands are short manual /invoke actions with optional arguments and whitelisted tools. They are the lightest-weight Claude Code primitive: under 150 lines is ideal, 250 max. Past 250, split into a skill. Misuse — wrapping multi-stage workflows, expecting auto-trigger, padding with marketing prose — bloats the context budget and confuses users. This methodology codifies the line-count cap, the argument-syntax convention, the !-prefix bash pattern for live context, and the tool-whitelist rule. Output is a command file validated against the schema.

**Ефективно для:**

- Repeatable shortcut actions: /deploy, /commit, /review — predictable interface.
- Wrapping bash + context injection: !-prefix dynamic execution.
- Project-specific shortcuts, які не варті повноцінного skill'у.
- Live context injection (current branch, diff, env) на invocation time.

## Applies If (ALL must hold)

- Action is manual (/invoke) and small (&lt; 250 lines).
- Action has predictable interface — same arguments each time.
- Tool surface is tightly bounded (≤ 5 tools).

## Skip If (ANY kills it)

- Workflow needs multiple sequential agents OR memory between steps — use a Skill or Agent.
- Action must auto-run (not /invoke) — use Hooks.
- Logic &gt; 250 lines — split into a Skill with SKILL.md + reference.md.
- Project-private + team doesn't use faion-network — store locally + gitignore.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Action spec | one-paragraph description | team / product |
| Argument spec | list of named args + types | design |
| Tool whitelist | list of allowed tools | permissions policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: line-count-cap, explicit-argument-syntax, bash-prefix-for-live-context, tool-whitelist-required, no-marketing-prose | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `declare-frontmatter` | haiku | Template fill. |
| `write-body` | sonnet | Light judgment to stay terse. |

## Templates

| File | Purpose |
|------|---------|
| `templates/command.md` | Command Markdown template (frontmatter + arguments + body) |
| `templates/command-deploy.md` | Worked example: /deploy command |
| `templates/command-commit.md` | Worked example: /commit command with bash-prefix context |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-commands.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[agents]]
- [[skills]]
- [[hooks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
