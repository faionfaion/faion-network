---
slug: agents-framework-selection
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The 2025-2026 Python agent ecosystem has consolidated around six frameworks.
content_id: "ca44e6e5a90e8170"
tags: [agents, langgraph, crewai, autogen, framework-selection]
---
# Agent Framework Selection — LangGraph, CrewAI, AutoGen, DSPy

## Summary

**One-sentence:** The 2025-2026 Python agent ecosystem has consolidated around six frameworks.

**One-paragraph:** The 2025-2026 Python agent ecosystem has consolidated around six frameworks. LangGraph is the production default for state-machine workflows with persistence. CrewAI is the fastest path to role-based multi-agent teams. AutoGen handles conversational multi-agent research. DSPy is for teams that need automatic prompt optimization. Framework lock-in is real — LangGraph state schemas and CrewAI role configs are not portable across frameworks; choose deliberately.

## Applies If (ALL must hold)

- Starting a new agent project and needing to select the framework before writing implementation code.
- Evaluating whether to migrate from an ad-hoc LangChain loop to a structured framework.
- Adding a multi-agent pattern to an existing single-agent system.
- Selecting observability tooling for agent debugging and evaluation.

## Skip If (ANY kills it)

- Already committed to a framework — switching mid-project is more expensive than finishing.
- Simple single LLM call with no tools — no framework needed.

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

- parent skill: `geek/ai/ml-engineer/`
