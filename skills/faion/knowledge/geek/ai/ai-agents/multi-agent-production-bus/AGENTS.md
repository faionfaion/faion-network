---
slug: multi-agent-production-bus
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A central MessageBus handles async agent-to-agent communication via three modes: direct (point-to-point), broadcast (fan-out to all except sender), and request.
content_id: "739c8c546f1937c5"
tags: [multi-agent, message-bus, async, production, orchestration]
---
# Production Multi-Agent System with Message Bus

## Summary

**One-sentence:** A central MessageBus handles async agent-to-agent communication via three modes: direct (point-to-point), broadcast (fan-out to all except sender), and request.

**One-paragraph:** A central MessageBus handles async agent-to-agent communication via three modes: direct (point-to-point), broadcast (fan-out to all except sender), and request. ProductionMultiAgentSystem wraps the bus with three switchable execution strategies — hierarchical (orchestrator plan + worker dispatch + synthesis), parallel (asyncio.gather fan-out), and sequential (pipeline chain) — selected at run_task() call time.

## Applies If (ALL must hold)

- Production systems that need to switch coordination strategy at runtime without rewriting agent code — the strategy parameter selects hierarchical, parallel, or sequential.
- Systems requiring an audit trail of every inter-agent message (sender, receiver, content, type) for compliance or debugging.
- Async environments where worker blocking is unacceptable — the bus decouples send from receive, preventing circular waits.
- Cost-sensitive deployments where per-agent token usage must be attributed and budget-gated.

## Skip If (ANY kills it)

- Simple two-agent pipelines — the bus adds subscription setup overhead with no value for point-to-point synchronous chains.
- Prototypes where iteration speed matters more than auditability — set up a plain ManagerAgent or CollaborativeGroup first.
- Synchronous-only environments where asyncio is unavailable or forbidden — the bus is async-native.

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
