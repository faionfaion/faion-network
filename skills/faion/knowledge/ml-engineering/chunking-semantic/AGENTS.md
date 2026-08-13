# Chunking — Semantic (Embedding Similarity)

## Summary

**One-sentence:** Splits text where cosine similarity between adjacent sentence embeddings drops below a threshold, so chunks capture coherent concepts instead of arbitrary token windows.

**One-paragraph:** SemanticChunker embeds every sentence, computes pairwise cosine similarity for adjacent pairs, and places a boundary where similarity drops below `similarity_threshold` (default 0.75). Size guards subsplit chunks exceeding max_chunk_size and merge those below min_chunk_size. Empty / 1-sentence documents return a single chunk without calling the embedding function. Uses the same embedding model as retrieval so chunk boundaries align with the query-time similarity signal.

**Ефективно для:** RAG engineer running legal / medical / scientific RAG where mid-concept splits ruin answer quality — closes the gap between structure-blind fixed-size chunking and the conceptual flow of prose.

## Applies If (ALL must hold)

- High-stakes retrieval domain (legal / medical / scientific) where mid-concept splits degrade answers.
- Prose-heavy corpus without reliable headers or code structure.
- Embedding API budget allows one call per sentence at index time.
- Sentence tokenizer is reliable for the corpus language (NLTK punkt, spaCy).

## Skip If (ANY kills it)

- Quick prototyping with ≤10k docs — [[chunking-basics]] recursive is sufficient.
- Corpus language lacks reliable sentence tokenization — semantic boundaries become noise.
- Structured documents (Markdown / HTML / code) — load the structure-specific chunker; structure is a stronger signal than similarity.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Embedding function | callable str -> list[float] | matches retrieval model |
| Sentence tokenizer | nltk punkt / spaCy | language-appropriate |
| similarity_threshold | float (0..1) | default 0.75 |
| max_chunk_size / min_chunk_size | tokens | size guards |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/chunking-basics` | Token measurement + metadata invariants. |
| `geek/ai/rag-engineer/embedding-generation` | Embedding function semantics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: same model as retrieval, threshold band, size guards, empty-doc short-circuit, version | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema with similarity_threshold + embedding_model fields | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: model drift, no size guard, oversized sentences, mismatched tokenizer | ~700 |
| `content/04-procedure.xml` | deep | 6-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus profile + budget | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sentence-tokenize` | haiku | Mechanical text split. |
| `embed-sentences` | embedding-model | Direct embed call. |
| `threshold-tuning` | sonnet | Judgement on threshold across a sample. |

## Templates

| File | Purpose |
|------|---------|
| `templates/semantic_chunker.py` | SemanticChunker reference with size guards and empty-doc handling. |
| `templates/semantic-chunk-schema.json` | JSON Schema for one semantic chunk. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-semantic.py` | Verify schema; flag chunks below min or above max; check embedding_model field present. | After chunker run. |

## Related

- [[chunking-basics]] · [[chunking-document-structure]] · [[chunking-code-ast]] · [[chunking-production-service]] · [[embedding-generation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether semantic chunking is justified (high-stakes domain + budget + reliable tokenizer) or whether the cheaper recursive splitter from chunking-basics suffices.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/semantic_chunker.py`

```python
"""SemanticChunker — adjacent-sentence cosine boundary detector with size guards."""
from __future__ import annotations

import hashlib
from typing import Callable

import nltk
import numpy as np


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


class SemanticChunker:
    def __init__(
        self,
        embedding_func: Callable[[str], list[float]],
        embedding_model: str,
        similarity_threshold: float = 0.75,
        max_chunk_size: int = 1000,
        min_chunk_size: int = 100,
        version: str = "1.0.0",
    ) -> None:
        if not 0.6 <= similarity_threshold <= 0.85:
            raise ValueError("similarity_threshold must be in [0.6, 0.85]")
        self.embed = embedding_func
        self.model = embedding_model
        self.th = similarity_threshold
        self.max = max_chunk_size
        self.min = min_chunk_size
        self.version = version

    def chunk(self, text: str, source: str) -> list[dict]:
        sentences = [s for s in nltk.sent_tokenize(text) if s.strip()]
        if len(sentences) <= 1:
            if not sentences:
                return []
            return [self._record(source, 0, sentences, 1)]
        embeddings = [np.array(self.embed(s)) for s in sentences]
        boundaries = [i + 1 for i in range(len(embeddings) - 1) if _cosine(embeddings[i], embeddings[i + 1]) < self.th]
        groups: list[list[str]] = []
        start = 0
        for b in boundaries:
            groups.append(sentences[start:b])
            start = b
        groups.append(sentences[start:])
        chunks: list[dict] = []
        for idx, grp in enumerate(groups):
            chunks.append(self._record(source, idx, grp, len(grp)))
        return self._apply_size_guards(chunks)

    def _record(self, source: str, idx: int, sentences: list[str], sentence_count: int) -> dict:
        body = " ".join(sentences)
        key = f"{source}|{idx}|semantic@{self.version}"
        return {
            "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
            "text": body,
            "embedding_model": self.model,
            "similarity_threshold": self.th,
            "token_count": len(body.split()),
            "source": source,
            "strategy": "semantic",
            "version": self.version,
            "sentence_count": sentence_count,
        }

    def _apply_size_guards(self, chunks: list[dict]) -> list[dict]:
        out: list[dict] = []
        for c in chunks:
            if c["token_count"] > self.max:
                words = c["text"].split()
                for j in range(0, len(words), self.max):
                    sub = dict(c)
                    sub["text"] = " ".join(words[j:j + self.max])
                    sub["token_count"] = len(sub["text"].split())
                    out.append(sub)
            elif out and c["token_count"] < self.min:
                out[-1]["text"] += " " + c["text"]
                out[-1]["token_count"] += c["token_count"]
            else:
                out.append(c)
        return out
```

### `templates/semantic-chunk-schema.json`

```json
{
  "_header": {
    "purpose": "JSON Schema for one semantic chunk",
    "consumes": "chunk dict from SemanticChunker.chunk()",
    "produces": "pass/fail validation",
    "depends-on": "content/02-output-contract.xml",
    "token-budget-impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "faion://chunking-semantic/chunk.schema.json",
  "type": "object",
  "required": [
    "id",
    "text",
    "embedding_model",
    "similarity_threshold",
    "token_count",
    "source",
    "strategy",
    "version"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-f0-9]{32}$"
    },
    "text": {
      "type": "string",
      "minLength": 1
    },
    "embedding_model": {
      "type": "string",
      "minLength": 1
    },
    "similarity_threshold": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "token_count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4000
    },
    "source": {
      "type": "string",
      "minLength": 1
    },
    "strategy": {
      "type": "string",
      "const": "semantic"
    },
    "version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "sentence_count": {
      "type": "integer",
      "minimum": 1
    }
  }
}
```
