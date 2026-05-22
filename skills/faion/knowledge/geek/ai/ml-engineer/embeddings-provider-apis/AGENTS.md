---
slug: embeddings-provider-apis
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-ready integration patterns for the four main embedding provider categories: OpenAI (symmetric, Matryoshka dims), Voyage AI (asymmetric, quantization), Cohere (multimodal, input types, multilingual), and local sentence-transformers (GPU, BGE-M3 dense+sparse).
content_id: "74d57f10ce7119b1"
tags: [embeddings, openai, voyage-ai, cohere, sentence-transformers]
---
# Embedding Provider API Integration

## Summary

**One-sentence:** Production-ready integration patterns for the four main embedding provider categories: OpenAI (symmetric, Matryoshka dims), Voyage AI (asymmetric, quantization), Cohere (multimodal, input types, multilingual), and local sentence-transformers (GPU, BGE-M3 dense+sparse).

**One-paragraph:** Production-ready integration patterns for the four main embedding provider categories: OpenAI (symmetric, Matryoshka dims), Voyage AI (asymmetric, quantization), Cohere (multimodal, input types, multilingual), and local sentence-transformers (GPU, BGE-M3 dense+sparse). Each provider requires a different client setup and has distinct capabilities.

## Applies If (ALL must hold)

- Building a new embedding pipeline and need provider-specific client code.
- Implementing asymmetric search (different representation for query vs document).
- Adding GPU acceleration for local models or quantized output for storage savings.
- Integrating multimodal embeddings (text + image in the same vector space).

## Skip If (ANY kills it)

- When you need a unified multi-provider abstraction — use litellm instead of implementing per-provider wrappers.
- When you have not yet selected a model — see embeddings-model-selection first.

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
