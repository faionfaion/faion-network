# Auto-Evict Tool Results at Token Threshold

## Summary

**One-sentence:** Runtime middleware that auto-evicts any tool result over N tokens (default 20k) to disk and substitutes {path, preview, total_tokens, evicted:true} into the agent's message history before the LLM ever sees the oversized payload.

**One-paragraph:** LLMs cannot reliably self-truncate large tool returns; the result is context corruption, blown context windows, and incoherent later turns. This methodology installs the enforced sibling of voluntary "filesystem as memory": a deterministic decorator wraps the agent's tool runtime, checks token count on every return, persists oversized payloads to a scratch directory keyed by tool_call_id, and feeds a typed pointer into the agent. The agent recovers slices via a paired `read_file(path, lines)` tool. Output is one config artifact + middleware reference embedded in the agent harness.

**Ефективно для:** Команд, де агент іноді отримує 200k токенів з одного tool call і потім весь run йде нанівець; middleware вирішує цей клас bugs раз і назавжди — не людська дисципліна, а runtime constraint.

## Applies If (ALL must hold)

- Agent calls tools that occasionally return very large payloads (file reads, web scrape, DB query, log search).
- Long-horizon runs (>5 iterations) where one oversized return blows multiple subsequent turns.
- Scratch storage (local disk, S3, in-process content store) is available.
- A paired read-file tool can be added to the agent's toolbelt.
- Token counter is available for the model in use.

## Skip If (ANY kills it)

- Tools have hard size caps in the tool definition (e.g. always returns ≤2k).
- Short single-turn agents where the result is consumed immediately.
- Agent has no filesystem-equivalent storage available.
- No paired read tool can be added (model not allowed to access scratch).

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Tool registry | JSON list of tools | Tool catalogue |
| Token counter | callable token_count(text) → int | Provider SDK |
| Scratch storage path | URL / local path | Ops |
| Threshold N | int (default 20000) | Tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/filesystem-as-working-memory/AGENTS.md` | Voluntary sibling pattern. |
| `geek/ai/ai-agents/file-reference-passing/AGENTS.md` | Pointer-passing convention used by the evict decorator. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 rules: middleware, deterministic write, paired read tool | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the eviction config + the evicted pointer shape | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: wire middleware → expose read tool → test → tune N → ship | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: large payloads possible? → storage available? → read-tool addable? → install/skip | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `instrument_token_counter` | haiku | Mechanical. |
| `tune_threshold_N` | sonnet | Per-agent tuning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the eviction config. |
| `templates/output.example.json` | Filled example. |
| `templates/evict-middleware.py` | Python middleware skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate eviction config. | After wiring, before ship. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[filesystem-as-working-memory]] — voluntary sibling.
- peer: [[file-reference-passing]] — pointer convention.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) can any tool return >N tokens? (2) is scratch storage available? (3) can a paired read-tool be exposed? Leaves point to "install", "raise hard tool caps instead", or "skip — not applicable".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/auto-evict-tool-results/output.json",
  "title": "Auto Evict Tool Results Output",
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
  "artefact_id": "auto-evict-tool-results-example-001",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "version_stamp": "auto-evict-tool-results@1.0.0",
  "produced_at": "2026-05-22T12:00:00Z",
  "fields": {
    "placeholder_field": "filled-by-author"
  },
  "rationale": "Example output for Auto Evict Tool Results; references at least one named input.",
  "inputs_used": [
    "docs/brief.md"
  ]
}
```

### `templates/evict-middleware.py`

```python
"""Minimal eviction middleware for agent tool runtimes.

Usage:
    @evict(threshold=20_000, scratch="/tmp/agent")
    def my_tool(...): ...

Pair with a `read_file(path, lines)` tool exposed to the agent so it can
recover slices on demand. Source pattern: LangChain Deep Agents
filesystemMiddleware (`toolTokenLimitBeforeEvict`, default 20000).
"""

from __future__ import annotations

import functools
import json
import uuid
from pathlib import Path
from typing import Any, Callable


def count_tokens(text: str) -> int:
    """Replace with your tokeniser (tiktoken, anthropic, etc.)."""
    # Cheap heuristic: ~4 chars per token.
    return max(1, len(text) // 4)


def evict(
    threshold: int = 20_000,
    scratch: str = "/tmp/agent",
    preview_chars: int = 400,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    Path(scratch).mkdir(parents=True, exist_ok=True)

    def decorator(tool: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(tool)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            raw = tool(*args, **kwargs)
            text = raw if isinstance(raw, str) else json.dumps(raw)
            n = count_tokens(text)
            if n <= threshold:
                return raw
            path = Path(scratch) / f"{tool.__name__}_{uuid.uuid4().hex}.txt"
            path.write_text(text)
            return {
                "path": str(path),
                "preview": text[:preview_chars],
                "total_tokens": n,
                "evicted": True,
            }

        return wrapper

    return decorator


def read_file(path: str, start: int = 0, end: int | None = None) -> str:
    """Recovery tool — agent calls this to pull a slice from an evicted result."""
    lines = Path(path).read_text().splitlines()
    return "\n".join(lines[start:end])
```
