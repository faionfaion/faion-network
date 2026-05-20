---
slug: claude-code-headless-default
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When you need an autonomous agent for a coding, devops, or research task, invoke `claude -p` with a prompt string as a subprocess instead of writing a custom Agent SDK loop.
content_id: "58b86b1a689281ec"
tags: [claude-code, agents, headless, orchestration, sdk]
---
# Claude Code Headless As Default Agent Runtime

## Summary

**One-sentence:** When you need an autonomous agent for a coding, devops, or research task, invoke `claude -p` with a prompt string as a subprocess instead of writing a custom Agent SDK loop.

**One-paragraph:** When you need an autonomous agent for a coding, devops, or research task, invoke `claude -p` with a prompt string as a subprocess instead of writing a custom Agent SDK loop. The Claude Code CLI ships with a battle-tested harness — filesystem, bash, git, MCP, plan mode, sub-agents, hooks, skills, automatic compaction — already wired together. Drop down to the Claude Agent SDK only when you have a concrete reason the CLI cannot satisfy: a non-coding domain, custom tools beyond MCP, programmatic control of the inner loop, or embedding inside a SaaS product that cannot shell out.

## Applies If (ALL must hold)

- Coding, devops, refactoring, or research tasks runnable from a shell.
- Cron jobs, GitHub Actions, queue workers, internal automation.
- Any task that benefits from filesystem + git + bash context out of the box.
- Multi-agent pipelines where the orchestrator can shell out to subprocesses.
- Prototyping an agent before deciding whether a custom SDK loop is justified.

## Skip If (ANY kills it)

- Non-coding business workflows (sales triage, claims, invoice routing) — Agent SDK + custom tools is leaner.
- SaaS product embedding where the host process cannot fork subprocesses.
- Custom inner-loop control (intercept every tool call, branch the conversation tree) — needs SDK.
- Domains needing non-MCP tools that cannot be expressed as MCP servers.

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
