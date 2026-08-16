# Gemini API Integration

## Summary

**One-sentence:** Produces a working Gemini API integration — model selection (Pro vs Flash), 1M-context handling, Files API upload pattern, generation config + safety settings.

**One-paragraph:** Google's Gemini API is the canonical entry point to gemini-2.x-pro and gemini-2.x-flash. Distinct shape vs Anthropic/OpenAI: large 1M-token context, Files API for video/audio uploads (vs inline base64), `generation_config` block (temperature, top_p, top_k, max_output_tokens, response_mime_type), and explicit `safety_settings` per category. This methodology produces a baseline integration: pick Flash for cost-sensitive paths and Pro for quality-sensitive; upload large media via Files API with TTL tracking; set generation_config defaults; configure safety thresholds to avoid silent BLOCK_REASON returns.

**Ефективно для:** ingesting long documents and full codebases, video analysis pipelines, cost-sensitive bulk classification, Vertex-anchored stacks.

## Applies If (ALL must hold)

- Gemini is the chosen vendor for this call site (cost, context, multimodal, or compliance reason).
- Either google-genai SDK or Vertex AI client is acceptable.
- Network access to Google AI endpoint.
- A response-handling layer can detect BLOCK_REASON and surface it.

## Skip If (ANY kills it)

- Pure text Q&A at &lt;8k context — Anthropic/OpenAI are equally fine and often faster at p50.
- Hard regulatory exclusion of Google AI in scope.
- Fine-tuning required as a first-class need — Gemini's fine-tuning is region-restricted.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Google AI / Vertex credentials | secret | secrets manager |
| Use case + expected context size | doc | spec |
| Latency budget per call site | ms | SLO |
| Safety policy (per category) | doc | safety review |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[gemini-basics]]` | Sibling baseline on SDK usage. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: pick model by cost+context, Files API for &gt;10MB, generation_config default, safety_settings explicit, retry on 429, block_reason surfaced | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for gemini-config.json + response-handler shape | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: inline base64 for big media, missing safety_settings, BLOCK_REASON swallowed, no retry on 429, model-mix on same call site | ~600 |
| `content/04-procedure.xml` | medium | 6-step: pick model → set generation_config → handle Files API → wire safety → handle block reasons → retry + monitor | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "Gemini is the chosen vendor for this call site?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Pick Pro vs Flash | sonnet | Cost/quality tradeoff. |
| Upload via Files API | runtime | Mechanical. |
| Surface BLOCK_REASON | sonnet | Pattern code. |
| Tune safety thresholds | opus | Policy reasoning. |

## Templates

| File | Purpose |
|---|---|
| `templates/gemini-config.schema.json` | JSON Schema for gemini-config.json. |
| `templates/gemini-client.py` | Reference Python integration with Files API + safety. |
| `templates/safety-defaults.yaml` | Default safety thresholds per category. |
| `templates/_smoke-test.json` | Minimum valid gemini-config. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gemini-api-integration.py` | Validates gemini-config.json against schema and asserts safety_settings cover all 4 standard categories. | Pre-commit on config; CI before deploy. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[gemini-basics]]`
- `[[gemini-multimodal]]`
- `[[gemini-function-calling]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` selects this methodology when Gemini is the chosen vendor. Branches by model choice (Pro vs Flash) given cost/quality budget; routes media-heavy calls to use Files API; skips when vendor is not Gemini.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/gemini-config.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/gemini-config",
  "_purpose": "Schema for the per-call-site Gemini config.",
  "_consumes": "operator-authored gemini-config.json",
  "_produces": "validation verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "validator only",
  "type": "object",
  "required": [
    "model",
    "generation_config",
    "safety_settings"
  ],
  "properties": {
    "model": {
      "type": "string",
      "pattern": "^gemini-"
    },
    "generation_config": {
      "type": "object",
      "required": [
        "temperature",
        "max_output_tokens"
      ],
      "properties": {
        "temperature": {
          "type": "number",
          "minimum": 0,
          "maximum": 2
        },
        "max_output_tokens": {
          "type": "integer",
          "minimum": 1
        },
        "response_mime_type": {
          "enum": [
            "text/plain",
            "application/json"
          ]
        }
      }
    },
    "safety_settings": {
      "type": "array",
      "minItems": 4,
      "items": {
        "type": "object",
        "required": [
          "category",
          "threshold"
        ],
        "properties": {
          "category": {
            "enum": [
              "HARM_CATEGORY_HARASSMENT",
              "HARM_CATEGORY_HATE_SPEECH",
              "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              "HARM_CATEGORY_DANGEROUS_CONTENT"
            ]
          },
          "threshold": {
            "enum": [
              "BLOCK_NONE",
              "BLOCK_LOW_AND_ABOVE",
              "BLOCK_MEDIUM_AND_ABOVE",
              "BLOCK_ONLY_HIGH"
            ]
          }
        }
      }
    }
  }
}
```

### `templates/gemini-client.py`

```python
"""
from __future__ import annotations

import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def make_client(api_key: str):
    if genai is None:
        raise SystemExit("google-genai required: pip install google-genai")
    return genai.Client(api_key=api_key)


def upload_if_large(client, path: Path, threshold_kb: int = 10240):
    size_kb = path.stat().st_size / 1024
    if size_kb < threshold_kb:
        return path.read_bytes()
    return client.files.upload(file=str(path))


def call_with_retry(client, model: str, contents, gen_cfg: dict, safety: list[dict], max_attempts: int = 5) -> dict:
    for attempt in range(max_attempts):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(**gen_cfg, safety_settings=[types.SafetySetting(**s) for s in safety]),
            )
            cand = resp.candidates[0]
            return {
                "text": resp.text if cand.finish_reason.name == "STOP" else "",
                "finish_reason": cand.finish_reason.name,
                "block_reason": getattr(resp.prompt_feedback, "block_reason", None),
            }
        except Exception as e:
            if "429" in str(e) and attempt < max_attempts - 1:
                time.sleep(min(2 ** attempt, 60))
                continue
            raise
    return {"text": "", "finish_reason": "RETRY_EXHAUSTED", "block_reason": None}
```

### `templates/safety-defaults.yaml`

```yaml
safety_settings:
  - category: HARM_CATEGORY_HARASSMENT
    threshold: BLOCK_MEDIUM_AND_ABOVE
  - category: HARM_CATEGORY_HATE_SPEECH
    threshold: BLOCK_MEDIUM_AND_ABOVE
  - category: HARM_CATEGORY_SEXUALLY_EXPLICIT
    threshold: BLOCK_MEDIUM_AND_ABOVE
  - category: HARM_CATEGORY_DANGEROUS_CONTENT
    threshold: BLOCK_MEDIUM_AND_ABOVE
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum valid gemini-config that passes the validator.",
  "_consumes": "validate-gemini-api-integration.py",
  "_produces": "ok verdict",
  "_depends_on": "templates/gemini-config.schema.json",
  "_token_budget_impact": "docs-only",
  "model": "gemini-2.5-flash",
  "generation_config": {
    "temperature": 0.2,
    "max_output_tokens": 2048
  },
  "safety_settings": [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
```
