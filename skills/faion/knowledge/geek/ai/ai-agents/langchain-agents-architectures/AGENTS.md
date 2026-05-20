---
slug: langchain-agents-architectures
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement tool-using agents with LangChain and LangGraph.
content_id: "89242b38ea69b392"
tags: [langchain, langgraph, react-agents, tool-use, agent-architectures]
---
# LangChain Agent Architectures and Tools

## Summary

**One-sentence:** Implement tool-using agents with LangChain and LangGraph.

**One-paragraph:** Implement tool-using agents with LangChain and LangGraph. Three architectures: ReAct (reason + act in a loop), Plan-and-Execute (plan upfront, then execute), and LATS (tree search for complex reasoning). Master tool definition, error handling, and state management for production agent systems.

## Applies If (ALL must hold)

- Building tool-using agents with verifiable, step-by-step reasoning (ReAct via `create_react_agent`)
- Multi-step research or data-processing tasks where upfront planning reduces error propagation (Plan-and-Execute)
- Complex reasoning problems with solution uncertainty where backtracking improves quality (LATS)
- Integrating heterogeneous tools (web search, calculators, APIs, databases) behind a unified agent interface
- Replacing custom agent loops with battle-tested LangGraph state machines that handle errors, checkpoints, and retries

## Skip If (ANY kills it)

- Single-tool, single-step retrieval tasks — plain LLM call is simpler and faster
- Hard latency requirements (<1 s): ReAct + LATS add multiple round-trips
- Cases where the complete solution path is already known — use a deterministic pipeline, not an agent
- Tasks where tool schemas cannot be written (e.g. the agent must call arbitrary undocumented APIs)
- Contexts where LangChain's verbose abstraction layers increase debugging cost more than they reduce development cost

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
