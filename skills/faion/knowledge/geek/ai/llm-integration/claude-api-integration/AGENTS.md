---
slug: claude-api-integration
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Full Claude API integration patterns with client initialization, sync/async completions, streaming, tool use, vision (URL and base64), Extended Thinking for complex reasoning, Prompt Caching for cost reduction, and the Batch API for offline jobs.
content_id: "61654613d863fbeb"
tags: [claude, api, integration, tool-use, streaming]
---
# Claude API Integration

## Summary

**One-sentence:** Full Claude API integration patterns with client initialization, sync/async completions, streaming, tool use, vision (URL and base64), Extended Thinking for complex reasoning, Prompt Caching for cost reduction, and the Batch API for offline jobs.

**One-paragraph:** Full Claude API integration patterns with client initialization, sync/async completions, streaming, tool use, vision (URL and base64), Extended Thinking for complex reasoning, Prompt Caching for cost reduction, and the Batch API for offline jobs. The core rule: always check stop_reason — "max_tokens" is silent truncation; "tool_use" means the agent loop must continue; only "end_turn" is normal completion.

## Applies If (ALL must hold)

- Tasks requiring deep instruction-following across long contexts (up to 200K tokens).
- Code generation, review, or refactoring where nuance and safety matter.
- Multi-turn conversation pipelines where system prompt stability is critical.
- Long document processing (legal, technical, medical) in a single shot.
- Extended Thinking tasks: multi-step math, architecture decisions, strategic planning.
- When Anthropic's safety defaults are a feature, not a bug (enterprise, sensitive data).

## Skip If (ANY kills it)

- High-volume, low-cost inner loops where gpt-4o-mini is sufficient (Claude Haiku excepted).
- When OpenAI Structured Outputs (beta.parse) schema enforcement is required — Claude lacks this.
- Tasks needing OpenAI Assistants' persistent thread and file storage model.
- When Google Search grounding is required — use Gemini instead.

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
