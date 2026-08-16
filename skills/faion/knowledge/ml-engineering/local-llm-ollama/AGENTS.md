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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-local-llm-ollama.py` | Validates ollama-config: model_size_fits_vram, Modelfile path exists, fallback model set, openai_compat flag. | Pre-commit on config. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[function-calling-patterns]]`
- `[[ai-cost-attribution-schema]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides local-vs-cloud: privacy required + hardware sufficient → run local; bursty / frontier-reasoning → skip; mixed → use local primary + cloud fallback.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Modelfile`

```text
FROM llama3.1:8b

# Pin sampling defaults for deterministic outputs
PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER num_ctx 8192

SYSTEM """You are a concise assistant. Answer in the user's language. Refuse unsafe requests."""

# Optional Modelfile template override for chat
TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
<|assistant|>
{{ end }}"""
```

### `templates/ollama-client.py`

```python
"""
from __future__ import annotations

import requests
from openai import OpenAI

OLLAMA_BASE = "http://localhost:11434"


def ollama_ready(base_url: str = OLLAMA_BASE) -> bool:
    try:
        return requests.get(f"{base_url}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False


def make_local_client(base_url: str = OLLAMA_BASE) -> OpenAI:
    """OpenAI SDK pointed at local /v1 endpoint."""
    return OpenAI(base_url=f"{base_url}/v1", api_key="ollama")


def generate(prompt: str, model: str = "llama3.1:8b", cloud_fallback: OpenAI | None = None,
             cloud_model: str = "claude-sonnet-4-6") -> str:
    if not ollama_ready():
        if cloud_fallback is None:
            raise RuntimeError("Ollama not running. Start with: systemctl start ollama")
        return _cloud(cloud_fallback, prompt, cloud_model)
    local = make_local_client()
    try:
        resp = local.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content or ""
    except Exception:
        if cloud_fallback is not None:
            return _cloud(cloud_fallback, prompt, cloud_model)
        raise


def _cloud(client: OpenAI, prompt: str, model: str) -> str:
    resp = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content or ""
```

### `templates/ollama-config.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/local-llm-ollama-config",
  "_purpose": "Schema for ollama-config.json; enforces /v1 endpoint, ram floor, fallback.",
  "_consumes": "ollama-config.json from caller",
  "_produces": "validation report for validate-local-llm-ollama.py",
  "_depends_on": "content/01-core-rules.xml r1-r5",
  "_token_budget_impact": "0 \u2014 schema-only file",
  "type": "object",
  "required": [
    "base_url",
    "model",
    "ram_floor_gb",
    "health_check_required",
    "openai_compat",
    "fallback_cloud_model"
  ],
  "properties": {
    "base_url": {
      "type": "string",
      "format": "uri"
    },
    "model": {
      "type": "string",
      "minLength": 1
    },
    "modelfile_path": {
      "type": "string"
    },
    "quantisation": {
      "enum": [
        "q4_K_M",
        "q5_K_M",
        "q6_K",
        "q8_0",
        "f16"
      ]
    },
    "ram_floor_gb": {
      "type": "integer",
      "minimum": 4
    },
    "health_check_required": {
      "type": "boolean",
      "const": true
    },
    "openai_compat": {
      "type": "boolean",
      "const": true
    },
    "systemd_service": {
      "type": "boolean"
    },
    "fallback_cloud_model": {
      "type": "string",
      "minLength": 1
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum valid ollama-config \u2014 used by validate-local-llm-ollama.py --self-test.",
  "_consumes": "none",
  "_produces": "passes validator",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0",
  "base_url": "http://localhost:11434/v1",
  "model": "llama3.1:8b",
  "modelfile_path": "templates/Modelfile",
  "quantisation": "q5_K_M",
  "ram_floor_gb": 8,
  "health_check_required": true,
  "openai_compat": true,
  "systemd_service": true,
  "fallback_cloud_model": "claude-sonnet-4-6"
}
```
