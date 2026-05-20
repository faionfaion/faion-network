---
slug: agents
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use this reference when creating a new agent or subagent, editing an existing agent, fixing or improving an agent, or adding functionality to an agent.
content_id: "37259ea365fc4323"
tags: [agents, subagents, autonomous-workers, task-delegation, parallel-execution]
---
# Creating or Updating Agents

## Summary

**One-sentence:** Use this reference when creating a new agent or subagent, editing an existing agent, fixing or improving an agent, or adding functionality to an agent.

**One-paragraph:** Use this reference when creating a new agent or subagent, editing an existing agent, fixing or improving an agent, or adding functionality to an agent. Agents are autonomous workers with isolated contexts, whitelisted tools, and designated roles.

## Applies If (ALL must hold)

- Parallelizing independent tasks that do not share state, such as three modules implemented simultaneously.
- Context isolation: preventing unrelated research from polluting the primary agent's context window.
- Role specialization: a reviewer agent that only reads, a coder agent that only writes.
- Long-running background work dispatched from an orchestrator, such as research, web scraping, or report generation.
- Sequential pipeline stages where each stage needs a clean context: spec, then design, then implement, then test.

## Skip If (ANY kills it)

- Simple single-step tasks that complete in one tool call: agent overhead is not justified.
- The subtask requires interactive user input mid-execution: agents run autonomously.
- Real-time streaming output is required: Task tool is async; results return on completion.
- Task needs to share mutable in-memory state with the parent: agents are isolated, use files as IPC.

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
