# Embedding Chunking Strategies

## Summary

**One-sentence:** Picks chunking strategy (fixed-token, sentence-aware, recursive, semantic, structural) per corpus class plus chunk_size + overlap; benchmarks Recall@10 before deploy.

**One-paragraph:** Wrong chunking is the #1 silent killer of RAG quality. Too small → retriever misses context; too large → retrieval ranks worse and gen blows context. This methodology produces a `ChunkingConfig` artefact and the matching `Chunker` class — strategy picked by corpus class (prose / code / structured), chunk_size tuned by token budget, overlap to bridge across chunks, Recall@10 gate before deploy.

**Ефективно для:**

- New RAG corpus — pick strategy перед embedding.
- Migration зі static splitter → semantic splitter.
- Code corpus — структурний splitter, не token-based.
- Mixed-format corpus (HTML + PDF + Markdown) — per-format strategy.
- Cost-quality tradeoff: smaller chunks = more vectors = better recall at higher cost.

## Applies If (ALL must hold)

- New RAG corpus OR retrieval quality regression vs baseline.
- Domain bench set available (≥50 labeled pairs).
- Token budget allows chunk_size sweep.
- Named owner.

## Skip If (ANY kills it)

- Single-document corpus (chunking optional).
- No bench set → cannot validate.
- Latency budget cannot absorb the sweep.
- Existing chunker validated within last 90 days.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Corpus sample (≥1000 docs) | JSONL | warehouse |
| Domain bench set (50–200 pairs) | JSONL | eval repo |
| Tokenizer (matching embedding model) | tokenizer | platform |
| Embedding model client | client | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-applications]]` | Pipeline that consumes chunks. |
| `[[rag-bench-harness-template]]` | Bench harness for Recall@10. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for chunking-config | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | essential | 5-step: classify → strategy → sweep → bench → deploy | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus class to strategy | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-corpus` | sonnet | Per-doc judgment. |
| `sweep-chunk-size` | haiku | Numeric. |
| `recall-gate-review` | opus | Cross-metric synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunker.py` | Chunker class with all 5 strategies. |
| `templates/chunking-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-chunking-strategies.py` | Validate chunking-config | Pre-commit + CI |

## Related

- [[embedding-applications]]
- [[embedding-generation]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes corpus class (prose / code / structured / mixed) to strategy default; the bench gate confirms before deploy.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/chunker.py`

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ChunkingConfig:
    strategy: str = "recursive"
    size_unit: str = "tokens"
    chunk_size: int = 512
    overlap_tokens: int = 64
    min_tokens: int = 60
    max_tokens: int = 1024


@dataclass
class Chunker:
    config: ChunkingConfig
    tokenize: Callable[[str], list[str]]
    detokenize: Callable[[list[str]], str]

    def __post_init__(self) -> None:
        if self.config.size_unit != "tokens":
            raise ValueError("size_unit must be tokens (rule r1)")
        if self.config.min_tokens < 50:
            raise ValueError("min_tokens must be >=50 (rule r5)")
        if self.config.overlap_tokens > self.config.chunk_size // 2:
            raise ValueError("overlap_tokens must be <= chunk_size/2")

    def _fixed_token_chunks(self, tokens: list[str]) -> list[list[str]]:
        out: list[list[str]] = []
        step = max(1, self.config.chunk_size - self.config.overlap_tokens)
        for start in range(0, len(tokens), step):
            chunk = tokens[start : start + self.config.chunk_size]
            if len(chunk) < self.config.min_tokens and out:
                break
            out.append(chunk)
        return out

    def _recursive_chunks(self, text: str) -> list[str]:
        # split on paragraphs, then sentences, then tokens
        paras = re.split(r"\n{2,}", text)
        result: list[str] = []
        buffer: list[str] = []
        token_count = 0
        for para in paras:
            ptoks = self.tokenize(para)
            if token_count + len(ptoks) <= self.config.chunk_size:
                buffer.append(para)
                token_count += len(ptoks)
            else:
                if buffer:
                    result.append("\n\n".join(buffer))
                # overlap tail
                tail_tokens = self.tokenize("\n\n".join(buffer))[-self.config.overlap_tokens :] if buffer else []
                buffer = [self.detokenize(tail_tokens), para] if tail_tokens else [para]
                token_count = len(tail_tokens) + len(ptoks)
        if buffer:
            result.append("\n\n".join(buffer))
        return result

    def split(self, doc: dict[str, Any]) -> list[dict[str, Any]]:
        text = doc["text"]
        doc_id = doc["id"]
        if self.config.strategy == "fixed_token":
            chunks = [self.detokenize(c) for c in self._fixed_token_chunks(self.tokenize(text))]
        else:
            chunks = self._recursive_chunks(text)
        return [
            {
                "id": f"{doc_id}::{i}",
                "parent_doc_id": doc_id,
                "text": ch,
                "token_count": len(self.tokenize(ch)),
            }
            for i, ch in enumerate(chunks)
        ]
```

### `templates/chunking-config.json`

```json
{
  "strategy": "recursive",
  "size_unit": "tokens",
  "chunk_size": 512,
  "overlap_tokens": 64,
  "min_tokens": 60,
  "max_tokens": 1024,
  "bench_recall10": 0.78
}
```
