# Chunking — Production Service

## Summary

**One-sentence:** Production orchestration layer that routes documents to per-type chunkers (Markdown/HTML/code/recursive), propagates document-level metadata, and falls back to word-split on exception with a logged warning.

**One-paragraph:** ChunkingService takes a `ChunkingConfig(strategy, chunk_size, overlap, min_chunk_size, embedding_func?)` and a per-document `metadata` dict. It dispatches to MarkdownChunker, HTMLChunker, CodeChunker, SemanticChunker, or RecursiveChunker; attaches document-level metadata to every output chunk; and on any exception logs the failure then returns a word-split fallback with `strategy_used="fallback"`. Fail-fast on missing embedding_func for SEMANTIC strategy at construction time, not at chunk time.

**Ефективно для:** RAG engineer running batch ingest over mixed content types — closes the gap between per-document chunker wiring and a single service call the pipeline layer can rely on.

## Applies If (ALL must hold)

- Pipeline processes mixed content types (markdown, code, html, prose) in one run.
- Per-document metadata (source path, ingestion timestamp, tenant) must be on every chunk.
- Batch jobs require graceful degradation rather than total failure on parse errors.
- Operators need to distinguish fallback chunks from primary chunks for monitoring.

## Skip If (ANY kills it)

- Quick prototyping with one homogeneous content type — instantiate the chunker directly.
- Single-strategy pipelines (only semantic, or only recursive).
- No need for fallback or strategy-tagged audit trail.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| ChunkingConfig | dataclass | application config |
| Sub-chunker implementations | classes | [[chunking-basics]], [[chunking-document-structure]], [[chunking-code-ast]], [[chunking-semantic]] |
| Per-document metadata | dict | upstream ingestion |
| Structured logger | logging.Logger | application bootstrap |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/chunking-basics` | Default recursive chunker + token measurement. |
| `geek/ai/rag-engineer/chunking-document-structure` | Markdown / HTML path. |
| `geek/ai/rag-engineer/chunking-code-ast` | Code path. |
| `geek/ai/rag-engineer/chunking-semantic` | Optional semantic path. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fail-fast config validation, dispatch by strategy enum, metadata propagation, logged fallback, strategy_used in output | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema unioning per-strategy chunk shapes + service envelope | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: silent fallback, missing embedding_func discovered mid-batch, metadata loss, no strategy_used field | ~700 |
| `content/04-procedure.xml` | deep | 6-step procedure: validate config → dispatch → chunk → tag metadata → catch exceptions → log + fallback | ~700 |
| `content/05-examples.xml` | medium | ChunkingService class with all dispatch + fallback paths | ~600 |
| `content/06-decision-tree.xml` | essential | Routes content type and config to strategy or fallback | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `config-validation` | haiku | Schema check, no judgement. |
| `dispatch` | haiku | Mechanical. |
| `incident-review` | sonnet | Inspect fallback log entries for re-ingest decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunking_service.py` | ChunkingService reference with dispatch + fallback + metadata propagation. |
| `templates/chunking-service-schema.json` | JSON Schema for the service output envelope. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-production-service.py` | Verify service output envelope, check fallback chunks have a warning, metadata present on every chunk. | After each ingest batch. |

## Related

- [[chunking-basics]] · [[chunking-document-structure]] · [[chunking-code-ast]] · [[chunking-semantic]] — dispatch targets.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes based on `config.strategy` (explicit) vs auto-detect (content-type sniff). Fallback is only reachable through the exception handler, never as a default.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/chunking_service.py`

```python
"""ChunkingService — production wrapper with fail-fast config + logged fallback."""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Callable

logger = logging.getLogger("chunking_service")


class Strategy(str, Enum):
    FIXED = "fixed"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"
    HTML = "html"
    CODE = "code"


@dataclass
class ChunkingConfig:
    strategy: Strategy = Strategy.RECURSIVE
    chunk_size: int = 500
    overlap: int = 50
    min_chunk_size: int = 100
    embedding_func: Callable[[str], list[float]] | None = None
    version: str = "1.0.0"


class ChunkingService:
    def __init__(self, config: ChunkingConfig, sub_chunkers: dict[Strategy, object]) -> None:
        if not isinstance(config.strategy, Strategy):
            raise ValueError("strategy must be Strategy enum")
        if config.strategy is Strategy.SEMANTIC and config.embedding_func is None:
            raise ValueError("SEMANTIC requires embedding_func at __init__")
        if config.overlap >= config.chunk_size:
            raise ValueError("overlap must be < chunk_size")
        if config.strategy not in sub_chunkers:
            raise ValueError(f"no sub-chunker registered for {config.strategy}")
        self.cfg = config
        self.sub = sub_chunkers

    def chunk(self, text: str, source: str, metadata: dict | None = None) -> dict:
        meta = dict(metadata or {})
        warnings: list[dict] = []
        try:
            chunks = self.sub[self.cfg.strategy].chunk(text, source)
            strategy_used = self.cfg.strategy.value
        except Exception as exc:
            logger.warning(
                "chunker failure -> fallback",
                extra={"source": source, "requested_strategy": self.cfg.strategy.value, "exception": str(exc)},
            )
            chunks = self._word_split(text, source)
            strategy_used = "fallback"
            warnings.append({
                "source": source, "requested_strategy": self.cfg.strategy.value, "exception": str(exc),
            })
        for c in chunks:
            chunk_meta = c.get("metadata") or {}
            chunk_meta.update(meta)
            c["metadata"] = chunk_meta
            c["strategy_used"] = strategy_used
        return {
            "requested_strategy": self.cfg.strategy.value,
            "strategy_used": strategy_used,
            "chunk_count": len(chunks),
            "chunks": chunks,
            "warnings": warnings,
        }

    def _word_split(self, text: str, source: str) -> list[dict]:
        words = text.split()
        records: list[dict] = []
        for i, start in enumerate(range(0, len(words), self.cfg.chunk_size)):
            body = " ".join(words[start:start + self.cfg.chunk_size])
            key = f"{source}|{i}|fallback@{self.cfg.version}"
            records.append({
                "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
                "text": body, "token_count": len(body.split()),
                "source": source, "strategy_used": "fallback",
                "version": self.cfg.version, "metadata": {},
            })
        return records
```

### `templates/chunking-service-schema.json`

```json
{
  "_header": {
    "purpose": "Service-level envelope schema for ChunkingService.chunk() output",
    "consumes": "envelope dict returned by ChunkingService.chunk()",
    "produces": "pass/fail validation",
    "depends-on": "content/02-output-contract.xml",
    "token-budget-impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "faion://chunking-production-service/output.schema.json",
  "type": "object",
  "required": [
    "requested_strategy",
    "strategy_used",
    "chunk_count",
    "chunks",
    "warnings"
  ],
  "properties": {
    "requested_strategy": {
      "type": "string",
      "enum": [
        "fixed",
        "sentence",
        "paragraph",
        "semantic",
        "recursive",
        "markdown",
        "html",
        "code"
      ]
    },
    "strategy_used": {
      "type": "string",
      "enum": [
        "fixed",
        "sentence",
        "paragraph",
        "semantic",
        "recursive",
        "markdown",
        "html",
        "code",
        "fallback"
      ]
    },
    "chunk_count": {
      "type": "integer",
      "minimum": 0
    },
    "chunks": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "warnings": {
      "type": "array",
      "items": {
        "type": "object"
      }
    }
  }
}
```
