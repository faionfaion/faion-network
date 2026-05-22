---
slug: agent-observability-stack-blueprint
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Wires OTel + judge + cost + trajectory storage + drift dashboard into a single deployable stack with vendor decision-tree (LangSmith / Langfuse / Helicone / Phoenix).
content_id: "7bd9cb9908a70ee5"
tags: [agent-observability-stack-blueprint, ai, geek]
---

# Agent Observability Stack Blueprint

## Summary

**One-sentence:** Wires OTel + judge + cost + trajectory storage + drift dashboard into a single deployable stack with vendor decision-tree (LangSmith / Langfuse / Helicone / Phoenix).

**One-paragraph:** faion has reference catalogues (llm-observability-stack-2026, llm-observability) but no buildable blueprint. Engineers can't evaluate options without reading 5 docs. Mechanism: deployable stack diagram + opinionated vendor pick per use case + minimum data model. Output: stack-decision artefact + integration plan + week-1 eval-loop wiring.

## Applies If (ALL must hold)

- team shipping an LLM agent to production OR pre-prod with paying users
- ≥1 engineer ≥20% time on ops/observability
- trace volume ≥1k spans/day OR ≥10 unique tools
- cost tracking is a stated requirement (board/finance/SLO)

## Skip If (ANY kills it)

- single-prompt chatbot with <100 calls/day — use vendor dashboard only
- team has zero infra (no logging/metrics) — set up basic logging first
- compliance overrides (HIPAA/PCI in flight) — defer to regulated stack patterns

## Prerequisites

- stack inventory: model provider(s), framework, language
- trace volume estimate + cost run-rate
- 1 sample failing trace from production to validate against

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/llm-observability` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/llm-observability-stack-2026` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer methodology: `geek/ai/llm-observability`
- peer methodology: `geek/ai/llm-observability-stack-2026`
- external: https://opentelemetry.io/docs/specs/semconv/gen-ai/ (OTel GenAI semconv); https://langfuse.com/docs; https://docs.smith.langchain.com
