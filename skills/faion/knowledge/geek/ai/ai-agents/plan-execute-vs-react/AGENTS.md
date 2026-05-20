---
slug: plan-execute-vs-react
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For tasks where the steps are predictable from the goal, use Plan-Execute: one big planning call produces a structured plan, then deterministic code executes it.
content_id: "d571655ad2e28901"
tags: [agent-loops, control-flow, planning, reasoning, exploration]
---
# Plan-Execute vs ReAct — Picking the Right Loop

## Summary

**One-sentence:** For tasks where the steps are predictable from the goal, use Plan-Execute: one big planning call produces a structured plan, then deterministic code executes it.

**One-paragraph:** For tasks where the steps are predictable from the goal, use Plan-Execute: one big planning call produces a structured plan, then deterministic code executes it. For tasks where the next step depends on what you just learned, use ReAct: interleave Thought → Action → Observation in a loop. Mixing modes for the wrong job is the #1 cause of agent runs that meander or lock in early.

## Applies If (ALL must hold)

- Goal decomposes into known sub-steps → Plan-Execute
- Sub-steps are independent (parallelizable) → Plan-Execute
- User wants to review the plan before run → Plan-Execute
- Each step's input depends on previous output → ReAct
- Tool results often surprise (search, web, codebases) → ReAct
- Cost-bounded but exploratory → ReAct (with max_turns)
- Compliance/audit requirement on intermediate work → Plan-Execute
- Long horizon, > 10 steps → Hybrid: plan top-level, ReAct each step

## Skip If (ANY kills it)

- Pure ReAct on a 30-step goal — loop wanders; no human can review trajectory
- Pure Plan-Execute on exploration — plan is invented blind; first step's reality breaks the rest
- ReAct without max_turns — infinite loops on bad tool output
- Plan-Execute that "plans inside execution" — confusing trace; plan changes mid-run
- Replan every step — same as ReAct but more expensive

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
