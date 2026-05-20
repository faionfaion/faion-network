---
slug: gemini-api
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Google Gemini API for multimodal AI applications.
content_id: "b9a7e77288f3ae4b"
tags: [gemini, llm-api, multimodal, real-time, long-context]
---
# Gemini API Integration

## Summary

**One-sentence:** Google Gemini API for multimodal AI applications.

**One-paragraph:** Google Gemini API for multimodal AI applications. Models: Gemini 3 Pro/Flash (1M+ context, dynamic thinking), Gemini 2.0 Flash (fast, agentic), Gemini 1.5 Pro (2M context). Key differentiators: native video/audio input, Live API for real-time voice/video, code execution sandbox, Google Search grounding, context caching (75% cost reduction).

## Applies If (ALL must hold)

- Processing documents, codebases, or video that exceeds 128K tokens (use Gemini 1.5 Pro at 2M)
- Real-time voice/video applications requiring low latency (use Live API with Gemini 2.0 Flash)
- Applications needing code execution in a sandboxed Python environment
- Grounding responses in live Google Search results (use grounding tools)
- High-volume production with cost sensitivity (Gemini 2.0 Flash at $0.10/$0.40 per 1M tokens)

## Skip If (ANY kills it)

- Agent tooling accuracy is critical: OpenAI and Claude have more mature tool-use ecosystems
- Need the strongest available reasoning: use Claude Opus or o3 for frontier reasoning tasks
- Enterprise compliance requiring no Google data processing — use Azure OpenAI or Claude on AWS

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
