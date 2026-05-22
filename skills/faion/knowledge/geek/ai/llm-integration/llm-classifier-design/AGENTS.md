---
slug: llm-classifier-design
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An LLM classifier should answer one question per item with the smallest possible payload.
content_id: "65ffa4c52aba6b6d"
tags: [classifier, structured-output, tool-use, context-minimisation, prompt-caching, claude-agent-sdk]
---
# LLM Classifier Design (tool-use, minimum context, batched)

## Summary

**One-sentence:** An LLM classifier should answer one question per item with the smallest possible payload.

**One-paragraph:** An LLM classifier should answer one question per item with the smallest possible payload. The right design decisions — pick the model that just barely meets the bar, force the answer through a single tool call, replace the SDK's default system prompt with your own, disable auto-loaded project context, batch items by numeric ID, and accept that an SDK turn includes the user message — collapse a multi-step agent loop into a single forced tool_use response and let prompt caching amortise the system prefix across the run.

## Applies If (ALL must hold)

- Yes/no or small-enum classification across many items (sufficiency audit, spam triage, intent detection, content gating, deduplication).
- Document scoring where the score is a fixed-shape object (rubric grading, relevance ranking, safety verdict).
- Bulk extraction with a known schema (named entities, citations, contact details).
- Any pipeline where the model's job is "look at this and produce one structured answer," not "have a conversation."

## Skip If (ANY kills it)

- Open-ended generation where the answer shape is unknown — use plain text completion.
- Multi-step reasoning where the model genuinely benefits from intermediate scratchpad turns — use Extended Thinking, not a forced single tool call.
- Tiny one-shot requests where building a tool schema and an SDK config costs more developer time than the cost saved.

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

- parent skill: `geek/ai/llm-integration/`
