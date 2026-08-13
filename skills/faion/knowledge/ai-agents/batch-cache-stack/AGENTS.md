# Batch API + Prompt Caching Stack

## Summary

**One-sentence:** Sends non-real-time agent workloads through the provider's Message Batches API with cache_control on the longest stable prefix — stacks the 50% batch discount with the 90% cache-read discount for ~5% of synchronous-uncached cost on cached portion.

**One-paragraph:** Overnight pipelines, eval harnesses, content backfills, dataset labelling — none of these need synchronous latency, but most still send synchronous uncached requests and pay 20× what they could. This methodology wires two stacking optimisations: (1) submit through Message Batches / Batch Mode (50% off, 24h SLA); (2) pin `cache_control` on the longest byte-identical prefix shared across batch items (90% off prefill on cache reads). Output is a config block + reference code that an engineer applies to an existing pipeline.

**Ефективно для:** Команд, де щоночі AI-pipeline жере $400 OpenAI/Anthropic — без батчей і без кешу; правильно зібраний stack зрізає це до $20-$40 за один день переробки.

## Applies If (ALL must hold)

- Workload is asynchronous (24h turnaround acceptable).
- ≥100 items per batch (cache amortisation requires volume).
- A stable prefix exists across items (system prompt + tools + canonical instructions).
- Provider supports batch + caching (Anthropic, OpenAI, etc).
- A finance / cost owner is interested in the savings.

## Skip If (ANY kills it)

- Workload is user-facing real-time (sub-second).
- Each item has a unique prefix (no caching opportunity).
- Batch size <50 (overhead exceeds savings).
- Provider doesn't support both batch and caching.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Workload sample | jsonl with prompts | Pipeline owner |
| Provider model + version | string | Tech lead |
| Cost dashboard | URL | Finance |
| Batch endpoint credentials | API key | Ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/prompt-cache-prefix-order/AGENTS.md` | Prefix ordering rules for cache hits. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: batch route, prefix byte-identical, cache_control marker, monitor hit rate | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the batch+cache config | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: async? → volume? → stable prefix? → install/skip | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_prefix` | haiku | Mechanical. |
| `verify_byte_identical` | haiku | Mechanical diff. |
| `tune_cache_marker_position` | sonnet | Per-pipeline judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the config. |
| `templates/output.example.json` | Filled example. |
| `templates/batch_with_cache.py` | Python skeleton for batch submission with cache_control. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the config. | Before pipeline switch. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[prompt-cache-prefix-order]] — prefix ordering rules.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is the workload async (24h ok)? (2) is per-batch volume ≥100? (3) is there a byte-identical stable prefix? Leaves point to "install stack", "use batch only / cache only", or "skip".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/batch-cache-stack/output.json",
  "title": "Batch Cache Stack Output",
  "description": "purpose=schema; consumes=brief+context; produces=artefact; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "version",
    "version_stamp",
    "produced_at",
    "rationale",
    "inputs_used"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "version_stamp": {
      "type": "string"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "fields": {
      "type": "object"
    },
    "rationale": {
      "type": "string",
      "minLength": 20
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  }
}
```

### `templates/output.example.json`

```json
{
  "artefact_id": "batch-cache-stack-example-001",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "version_stamp": "batch-cache-stack@1.0.0",
  "produced_at": "2026-05-22T12:00:00Z",
  "fields": {
    "placeholder_field": "filled-by-author"
  },
  "rationale": "Example output for Batch Cache Stack; references at least one named input.",
  "inputs_used": [
    "docs/brief.md"
  ]
}
```

### `templates/batch_with_cache.py`

```python
"""Anthropic Messages Batches with prompt caching — canonical stack.

Effective input cost on cached tokens: 0.5 (batch) * 0.1 (cache read) = 0.05x of
synchronous-uncached price. The first item pays cache-write (1.25x) once.

Required for the stack to fire:
1. system + tools are byte-identical across all items in the batch
2. cache_control sits on the LAST static block (system here)
3. variable content lives only in the user message at the end
"""
from __future__ import annotations

import hashlib
import json

from anthropic import Anthropic
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

client = Anthropic()

SYSTEM_PROMPT = (
    "You are a precise document analyst. "
    "Return JSON matching the schema in the user message."
)

TOOLS: list[dict] = []  # populate with static tool defs; do not sort at runtime


def _prefix_hash(system: str, tools: list[dict]) -> str:
    payload = json.dumps({"system": system, "tools": tools}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def submit_batch(docs: list[dict]) -> str:
    expected = _prefix_hash(SYSTEM_PROMPT, TOOLS)
    requests: list[Request] = []
    for i, doc in enumerate(docs):
        params = MessageCreateParamsNonStreaming(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=TOOLS,
            messages=[{"role": "user", "content": doc["text"]}],
        )
        assert _prefix_hash(SYSTEM_PROMPT, TOOLS) == expected
        requests.append(Request(custom_id=f"doc-{i}", params=params))

    batch = client.messages.batches.create(requests=requests)
    return batch.id
```
