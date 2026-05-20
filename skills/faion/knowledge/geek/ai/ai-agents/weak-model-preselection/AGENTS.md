---
slug: weak-model-preselection
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use a small cheap model to filter, classify, or extract references from long inputs, then pass only the filtered result to the expensive strong model.
content_id: "908a535433860e8b"
tags: [multi-model-orchestration, cost-optimization, preselection, weak-strong-cascade, llm-routing]
---
# Weak-Model Preselection

## Summary

**One-sentence:** Use a small cheap model to filter, classify, or extract references from long inputs, then pass only the filtered result to the expensive strong model.

**One-paragraph:** Use a small cheap model to filter, classify, or extract references from long inputs, then pass only the filtered result to the expensive strong model. This inverts the typical pipeline to optimize cost: the weak model says what to look at, and the strong model does the reasoning.

## Applies If (ALL must hold)

- Long input with mostly irrelevant noise such as search over docs, dedupe news, or pick code files to read.
- Pre-classification before downstream-model branching: route, then dispatch.
- High-volume preselection where every token saved compounds, such as RSS pipelines or log analysis.
- Any pipeline where the strong model receives more than approximately 5K tokens of input of which most is irrelevant.

## Skip If (ANY kills it)

- Short inputs, under 1K tokens: the routing overhead exceeds the savings.
- Tasks where the cheap model's filter mistakes are catastrophic such as medical, legal, or security gates: use cheap model only as ranker, never sole gatekeeper.
- When the strong model needs the full context for emergent insights, for example long-context literary analysis.

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
