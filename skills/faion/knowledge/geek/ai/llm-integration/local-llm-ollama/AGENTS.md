---
slug: local-llm-ollama
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an Ollama local-LLM integration — model pull + Modelfile, OpenAI-compatible client config, GPU/CPU/RAM sanity guard, fallback to cloud.
content_id: "4c1211984d932ca9"
complexity: medium
produces: code
est_tokens: 2900
tags: [ollama, local-llm, on-prem, openai-compatible, fallback]
---
# Local LLM with Ollama

## Summary

**One-sentence:** Produces an Ollama local-LLM integration — model pull + Modelfile, OpenAI-compatible client config, GPU/CPU/RAM sanity guard, fallback to cloud.

**One-paragraph:** Ollama exposes an HTTP API on localhost:11434 with both native and OpenAI-compatible (`/v1`) endpoints. Swapping between local and cloud is a base_url change. Production wires: pull only models that fit the host VRAM (8B/13B for 8-16GB; 70B requires 48GB+); declare a Modelfile pinning quantisation + system prompt + template; health-probe the daemon before each call; fall back to a cloud model when local fails or context exceeds local capacity. Cost: ~free per call after hardware sunk cost; latency depends on GPU; quality lags cloud by months.

**Ефективно для:** privacy-bound classifiers, offline pipelines, dev/test loops without API budget, custom fine-tuned model serving, latency-sensitive on-device assistants.

## Applies If (ALL must hold)

- Privacy or air-gap requirement, OR very high-volume low-stakes task where cost dominates.
- Host has ≥8GB RAM (≥16GB recommended) and a sane GPU (or accept CPU latency).
- A cloud-fallback path exists for tasks that exceed local capability or context.
- An ops owner can maintain `ollama pull` and Modelfile updates.

## Skip If (ANY kills it)

- Frontier-reasoning task — 7B/13B local models underperform.
- Tight latency on CPU-only — under-sized hardware makes local unusable.
- Bursty load — local GPU is not elastically scalable.
- Need bleeding-edge model — open-weights lag cloud by months.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Host inventory (RAM/GPU/disk) | doc | infra registry |
| Ollama daemon installed | binary | install script |
| Modelfile template | text | repo |
| Cloud fallback model | string | architecture decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[function-calling-patterns]]` | OpenAI-compatible mode supports the same tool-call patterns. |
| `[[ai-cost-attribution-schema]]` | Local calls still record per-tenant attribution (cost ≈ 0). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: model fits VRAM, Modelfile pinned, health-probe, OpenAI-compat endpoint preferred, cloud fallback path declared, quantisation chosen | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for ollama-config.json | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: oversize model, daemon-down silent, no fallback, untrusted Modelfile, q4 default for serious tasks | ~600 |
| `content/04-procedure.xml` | medium | 6-step: spec hardware → pick model + quant → write Modelfile → pull + verify → wire client + fallback → monitor | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "privacy/cost forces local AND hardware sufficient?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Pick model + quantisation | opus | Hardware/quality tradeoff. |
| Author Modelfile | sonnet | Template fill. |
| Wire fallback | sonnet | Mechanical. |
| Monitor health | runtime | Mechanical. |

## Templates

| File | Purpose |
|---|---|
| `templates/Modelfile` | Reference Modelfile pinning quant + system prompt + template. |
| `templates/ollama-client.py` | OpenAI-compatible client with health-probe + cloud fallback. |
| `templates/ollama-config.schema.json` | JSON Schema for ollama-config.json. |
| `templates/_smoke-test.json` | Minimum valid ollama-config. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-local-llm-ollama.py` | Validates ollama-config: model_size_fits_vram, Modelfile path exists, fallback model set, openai_compat flag. | Pre-commit on config. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[function-calling-patterns]]`
- `[[ai-cost-attribution-schema]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides local-vs-cloud: privacy required + hardware sufficient → run local; bursty / frontier-reasoning → skip; mixed → use local primary + cloud fallback.
