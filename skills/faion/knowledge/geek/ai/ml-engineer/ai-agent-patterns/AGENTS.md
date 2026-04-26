# AI Agent Design Patterns

## Summary

Six structured patterns for building agentic AI systems: ReAct (Thought-Action-Observation loop), Chain-of-Thought, Tool Use, Plan-Execute, Reflection, and Tree-of-Thoughts — plus multi-agent coordination topologies (Sequential, Parallel, Supervisor, Hierarchical). Choosing the right pattern at design time is more important than implementation details.

## Why

Ad-hoc "call LLM in a loop" code lacks explicit exit conditions, error recovery, and observability hooks. Named patterns enforce structure: ReAct requires an iteration cap; Reflection requires explicit criteria; Plan-Execute separates planning model from execution model for cost tiering. Structured patterns produce debuggable, cost-predictable agents.

## When To Use

- Selecting an architecture before building any agentic system
- Replacing informal LLM loops with debuggable, observable patterns
- Multi-step workflows where intermediate results determine next steps (ReAct, Plan-Execute)
- Quality-critical outputs where first-pass is insufficient (Reflection)
- Multi-agent coordination with specialized workers

## When NOT To Use

- Single LLM call with deterministic output — patterns add latency and cost without benefit
- Full input fits in one context window with no tool calls — just prompt directly
- Real-time inference under 200ms — ReAct, Reflection, and ToT require multiple round-trips
- Reproducible outputs for strict auditing — agent non-determinism conflicts with reproducibility requirements

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | ReAct, CoT, Tool Use, Plan-Execute: structure, triggers, trade-offs, gotchas |
| `content/02-advanced-patterns.xml` | Reflection, Tree-of-Thoughts, multi-agent topologies, model tiering |
| `content/03-implementation.xml` | Per-pattern implementation checklist, observability, safety, testing rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/react-system-prompt.txt` | ReAct system prompt with Thought/Action/Observation format |
| `templates/reflection-critic-prompt.txt` | Structured critic prompt returning JSON pass/fail with defect list |
| `templates/plan-execute-skeleton.py` | Plan-Execute with model tiering (Opus planner, Haiku executor) |
| `templates/tool-definition.json` | Tool definition schema for OpenAI/Anthropic function calling |
