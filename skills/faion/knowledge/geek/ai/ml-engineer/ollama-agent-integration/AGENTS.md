---
slug: ollama-agent-integration
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Ollama exposes an OpenAI-compatible endpoint at http://localhost:11434/v1, enabling drop-in replacement of the OpenAI SDK by changing one environment variable.
content_id: "6e010360cfba2299"
tags: [ollama, agents, openai-compatible, fallback]
---
# Ollama Agent Integration

## Summary

**One-sentence:** Ollama exposes an OpenAI-compatible endpoint at http://localhost:11434/v1, enabling drop-in replacement of the OpenAI SDK by changing one environment variable.

**One-paragraph:** Ollama exposes an OpenAI-compatible endpoint at http://localhost:11434/v1, enabling drop-in replacement of the OpenAI SDK by changing one environment variable. This methodology covers the integration pattern, health-check with automatic cloud fallback, agent-specific gotchas, and the ecosystem of tools (LiteLLM, Langfuse, Qdrant) that work with Ollama.

## Applies If (ALL must hold)

- Existing OpenAI-based agent code that needs to run against local models for privacy or cost.
- Any extraction or classification sub-agent where input data must not leave the machine.
- Local test agents in CI pipelines that mock cloud LLM behavior without API costs.
- Agent prototyping before committing to cloud provider pricing.
- Hybrid local/cloud setups where the agent uses the best available endpoint.

## Skip If (ANY kills it)

- Best-quality responses required for complex reasoning — even 70B local models trail frontier cloud models.
- Multilingual tasks across more than 20 languages — local models lag cloud providers significantly.
- Fine-tuned custom behavior needed but GPU for fine-tuning is unavailable.
- Real-time latency requirements on small hardware — CPU inference is 5-20x slower than GPU.

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
