---
slug: ai-agent-patterns
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Picks one of four control-flow patterns (CoT / ReAct / Plan-and-Execute / Tool Use) and a matching framework (raw SDK / LangGraph / AutoGen / CrewAI / OpenAI Agents SDK) for a new agent task.
content_id: "ae3d45909ea9b747"
complexity: medium
produces: decision-record
est_tokens: 5000
tags: [agents, patterns, frameworks, orchestration]
---
# AI Agent Patterns

## Summary

**One-sentence:** Picks one of four control-flow patterns (CoT / ReAct / Plan-and-Execute / Tool Use) and a matching framework (raw SDK / LangGraph / AutoGen / CrewAI / OpenAI Agents SDK) for a new agent task.

**One-paragraph:** Single prompt-response is insufficient for any non-trivial agent task; choosing the right control-flow pattern matters more than upgrading the underlying model. This methodology classifies the task on three axes (needs-tools, step-count, branching), maps to CoT / ReAct / Plan-and-Execute / Tool Use, and then maps the chosen pattern to a framework that fits team experience and dependency budget. Output is one decision record committed alongside the agent code.

**Ефективно для:** Команд, які тиждень обговорюють «який фреймворк взяти» замість «яка форма агента нам потрібна»; за годину дає named pattern + framework з обґрунтуванням, прив'язаним до конкретних характеристик задачі.

## Applies If (ALL must hold)

- New agent feature being scoped (no pattern committed yet).
- Task is non-trivial — at least one of: needs tools, has multi-step plan, requires iteration.
- Team is willing to commit to a single pattern for the feature (no parallel experiments).
- Latency budget allows ≥2 LLM round-trips.
- Owner can review the chosen framework's dependency cost.

## Skip If (ANY kills it)

- Task is solvable in one LLM call (no tools, single-shot output).
- Hard real-time SLA < 500ms — multi-iteration patterns are too slow.
- One-off script where framework dependency cost exceeds project lifetime.
- Creative generation where strict control flow degrades quality.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Task brief | natural language ≤500 chars | Operator |
| Tool inventory | JSON list `{name, description, schema}` | Tool registry |
| Latency budget | seconds | SLA owner |
| Framework experience matrix | team handles → familiar frameworks | Tech lead |
| Named owner | handle | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-patterns/AGENTS.md` | Sibling — pattern selection logic; this methodology extends it with framework choice. |
| `geek/ai/ai-agents/agent-shape-decision-frame/AGENTS.md` | Shape selection runs first; pattern runs inside chosen shape. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: classified-in-writing, comment-pattern-at-top, framework-pinned, schema-tools, max-steps-guard | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the pattern+framework decision record | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (no classification, framework first, no max-steps, vague tool desc, no tracing) | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: classify → pick pattern → pick framework → define tools → ship behind flag | ~1000 |
| `content/05-examples.xml` | medium | Three worked examples (CoT, ReAct, Plan-and-Execute) | ~1000 |
| `content/06-decision-tree.xml` | essential | Pattern tree + framework tree | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task` | haiku | Three-question classification. |
| `pick_pattern_and_framework` | sonnet | Per-instance judgment. |
| `author_decision_record` | sonnet | Final composition. |
| `executive_review` | opus | For multi-agent / framework-with-runtime-cost decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the decision record. |
| `templates/decision-record.example.json` | Filled minimal valid example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the decision record. | After subagent emits record. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-patterns]] — narrower scope, three patterns only.
- peer: [[plan-execute-vs-react]] — deeper on Plan-and-Execute vs ReAct trade-off.

## Decision tree

See `content/06-decision-tree.xml`. First tree: pattern selection on three axes (needs-tools, step-count, branching). Second tree: framework selection given chosen pattern + team experience + dependency budget.
