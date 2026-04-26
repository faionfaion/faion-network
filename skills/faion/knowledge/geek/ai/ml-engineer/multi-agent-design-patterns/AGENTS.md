# Multi-Agent Design Patterns

## Summary

Four canonical patterns for orchestrating multiple AI agents: Supervisor (centralized routing), Hierarchical (multi-level decomposition), Sequential (pipeline), and Peer-to-Peer (decentralized). Choose the simplest pattern that solves the problem — sequential before supervisor before hierarchical; peer-to-peer only when resilience outweighs debugging complexity.

## Why

Single agents fail on complex enterprise workflows because of context window limits, tool access isolation requirements, and latency constraints. Multi-agent systems apply the microservices principle: specialized agents collaborate through typed shared state, with each agent owning a narrow domain. Gartner recorded a 1,445% surge in multi-agent inquiries from Q1 2024 to Q2 2025.

## When To Use

- Single agent context window is insufficient for the full task
- Tasks have parallelizable subtasks (research + writing + validation can run concurrently)
- Domain expertise must be isolated — a billing agent must not have access to CRM tools
- Enterprise workflows map naturally to organizational units (teams, departments, roles)
- Reliability requires cross-checking: parallel agents can validate each other's outputs

## When NOT To Use

- Simple single-step tasks — multi-agent adds coordination overhead with no benefit
- Latency is critical (<2s) — agent-to-agent round trips add 500ms–2s each
- The problem is not well-decomposed yet — build a working single agent first, then extract workers
- Token budget is constrained — multi-agent systems use significantly more tokens per task
- Infrastructure cannot reliably run concurrent agent processes

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Supervisor, Hierarchical, Sequential, Peer-to-Peer — description, use cases, tradeoffs |
| `content/02-implementation-checklist.xml` | Per-pattern design, implementation, and production-readiness checklists |

## Templates

| File | Purpose |
|------|---------|
| `templates/pipeline-state.py` | Pydantic state models for all four patterns |
| `templates/langgraph-supervisor.py` | Minimal LangGraph supervisor graph (<50 lines) |
| `templates/agents-config.yaml` | YAML configuration for agent roles and routing rules |
