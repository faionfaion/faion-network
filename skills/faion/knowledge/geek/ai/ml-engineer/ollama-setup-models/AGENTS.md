---
slug: ollama-setup-models
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Ollama is an open-source platform for running LLMs locally.
content_id: "fffd48302168c9be"
tags: [ollama, local-llm, model-management, hardware]
---
# Ollama Setup and Model Management

## Summary

**One-sentence:** Ollama is an open-source platform for running LLMs locally.

**One-paragraph:** Ollama is an open-source platform for running LLMs locally. It bundles model weights, configuration, and data into a single Modelfile package (similar to Docker). Supports NVIDIA (CUDA), Apple Silicon (Metal), and AMD (ROCm) GPUs. Default endpoint: http://localhost:11434.

## Applies If (ALL must hold)

- Data privacy requirements where no external API calls are permitted.
- Offline or air-gapped environments (IoT, edge, secure networks).
- High-volume classification or extraction tasks where zero marginal API cost matters.
- Development and testing — no API keys, no rate limits, no costs, no internet required.
- Custom fine-tuned models that must be deployed locally after training.

## Skip If (ANY kills it)

- Best-quality responses required — even largest local models (70B) trail frontier cloud models on complex reasoning.
- Hardware is unavailable: 7B needs 8GB VRAM or RAM; 70B needs 48GB — check before planning.
- Real-time latency requirements on small hardware — CPU inference is 5-20x slower than GPU.
- Multilingual tasks across more than 20 languages — local models lag cloud providers significantly.

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
