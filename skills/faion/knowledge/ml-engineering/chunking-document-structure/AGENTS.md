# Chunking — Document Structure (Markdown / HTML)

## Summary

**One-sentence:** Splits Markdown by header hierarchy and HTML by sectioning elements, propagating parent header paths into every chunk to preserve navigational context for retrieval.

**One-paragraph:** MarkdownChunker splits at header boundaries (`#`, `##`, `###`) and prepends the parent `header_path` (joined by ` > `) into every chunk so queries that reference section context retrieve correctly. HTMLChunker uses BeautifulSoup to walk `<section>`, `<article>`, and `<div>` boundaries. Both attach min_chunk_size guards to drop near-empty chunks (single list items) that pollute nearest-neighbour scores.

**Ефективно для:** RAG engineer indexing docs site / wiki / API reference — closes the gap between flat character chunking (loses hierarchy) and the navigational anchors users actually query with.

## Applies If (ALL must hold)

- Corpus is Markdown documentation, wiki, README, or HTML with semantic sectioning elements.
- Retrieval queries reference section context ("what does the auth section say about tokens?").
- BeautifulSoup4 is available for the HTML path.
- min_chunk_size guard is configured (default 100 tokens) to filter near-empty chunks.

## Skip If (ANY kills it)

- Corpus is unstructured prose with no headers — load [[chunking-semantic]] or [[chunking-basics]].
- Source is code — load [[chunking-code-ast]].
- Flat HTML pages with no sectioning elements — HTMLChunker emits one giant chunk; pre-split with [[chunking-basics]] recursive.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Markdown / HTML files | text | docs repo / web crawl |
| beautifulsoup4 | python pkg | `pip install beautifulsoup4` |
| Max chunk size (token band) | int | matches embedding model |
| min_chunk_size guard | int | default 100 |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/chunking-basics` | Token measurement, metadata-at-creation, content-based IDs apply here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: header_path propagation, min_chunk_size guard, BeautifulSoup for HTML, oversized-block subdivision, version bump | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema with header_path field + section_id | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: lost header_path, no min guard, regex on HTML, no oversized subdivision | ~700 |
| `content/04-procedure.xml` | medium | 5 steps: detect → walk headers/sections → propagate path → subdivide oversize → emit | ~600 |
| `content/06-decision-tree.xml` | essential | Routes file type → Markdown or HTML chunker, and chooses subdivision threshold | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect-structure` | haiku | Header / DOM pattern detection. |
| `chunk-and-tag` | haiku | Mechanical walk + metadata attach. |

## Templates

| File | Purpose |
|------|---------|
| `templates/markdown_chunker.py` | MarkdownChunker reference with header_path propagation. |
| `templates/html_chunker.py` | HTMLChunker reference using BeautifulSoup4. |
| `templates/doc-chunk-schema.json` | JSON Schema for one document-structure chunk. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-document-structure.py` | Verify chunks match schema, header_path present, min_size respected. | After chunker run. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[chunking-basics]] — base invariants.
- [[chunking-code-ast]] — code path.
- [[chunking-semantic]] — fallback when no structure present.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by file type (markdown vs html vs other) and by header-density (deep hierarchy vs flat). Use it to decide whether MarkdownChunker, HTMLChunker, or a fallback to chunking-basics applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/markdown_chunker.py`

```python
"""MarkdownChunker — header-aware splitter that propagates parent header_path into every chunk."""
from __future__ import annotations

import hashlib
import re

HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")


class MarkdownChunker:
    def __init__(self, max_chunk_size: int = 1000, min_chunk_size: int = 100, version: str = "1.0.0") -> None:
        self.max = max_chunk_size
        self.min = min_chunk_size
        self.version = version

    def chunk(self, text: str, source: str) -> list[dict]:
        path_stack: list[tuple[int, str]] = []
        sections: list[tuple[str, str]] = []
        buf: list[str] = []
        current_path = ""
        for line in text.splitlines():
            m = HEADER_RE.match(line)
            if m:
                if buf:
                    sections.append((current_path, "\n".join(buf).strip()))
                    buf = []
                depth = len(m.group(1))
                title = m.group(2).strip()
                while path_stack and path_stack[-1][0] >= depth:
                    path_stack.pop()
                path_stack.append((depth, title))
                current_path = " > ".join(t for _, t in path_stack)
            else:
                buf.append(line)
        if buf:
            sections.append((current_path, "\n".join(buf).strip()))

        chunks: list[dict] = []
        for header_path, body in sections:
            if not body:
                continue
            if len(body.split()) <= self.max:
                chunks.append(self._record(source, header_path, None, body))
            else:
                parts = self._sub_split(body, self.max)
                for i, p in enumerate(parts):
                    chunks.append(self._record(source, header_path, i, p))
        return self._merge_below_min(chunks)

    def _sub_split(self, body: str, size: int) -> list[str]:
        words = body.split()
        return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

    def _record(self, source: str, header_path: str, part_index: int | None, body: str) -> dict:
        section_id = re.sub(r"[^a-z0-9-]", "-", header_path.lower())
        text = f"{header_path}\n\n{body}" if header_path else body
        key = f"{source}|{section_id}|{part_index}|markdown@{self.version}"
        return {
            "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
            "text": text,
            "header_path": header_path,
            "section_id": section_id,
            "token_count": len(text.split()),
            "source": source,
            "strategy": "markdown",
            "version": self.version,
            "part_index": part_index,
        }

    def _merge_below_min(self, chunks: list[dict]) -> list[dict]:
        out: list[dict] = []
        for c in chunks:
            if out and c["token_count"] < self.min and out[-1]["header_path"] == c["header_path"]:
                out[-1]["text"] += "\n\n" + c["text"].split("\n\n", 1)[-1]
                out[-1]["token_count"] += c["token_count"]
            else:
                out.append(c)
        return out
```

### `templates/html_chunker.py`

```python
"""HTMLChunker — DOM-walk via BeautifulSoup; never regex over HTML."""
from __future__ import annotations

import hashlib

from bs4 import BeautifulSoup


class HTMLChunker:
    SECTION_SELECTORS = ("section", "article", "main")

    def __init__(self, max_chunk_size: int = 1000, min_chunk_size: int = 100, version: str = "1.0.0") -> None:
        self.max = max_chunk_size
        self.min = min_chunk_size
        self.version = version

    def chunk(self, html: str, source: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        sections = []
        for sel in self.SECTION_SELECTORS:
            sections.extend(soup.find_all(sel))
        if not sections:
            sections = [soup]
        chunks: list[dict] = []
        for sec in sections:
            heading = sec.find(["h1", "h2", "h3", "h4"])
            header_path = heading.get_text(strip=True) if heading else ""
            body = sec.get_text("\n", strip=True)
            if not body:
                continue
            if len(body.split()) <= self.max:
                chunks.append(self._record(source, header_path, None, body))
            else:
                parts = self._sub_split(body, self.max)
                for i, p in enumerate(parts):
                    chunks.append(self._record(source, header_path, i, p))
        return chunks

    def _sub_split(self, body: str, size: int) -> list[str]:
        words = body.split()
        return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

    def _record(self, source: str, header_path: str, part_index: int | None, body: str) -> dict:
        section_id = header_path.lower().replace(" ", "-")
        text = f"{header_path}\n\n{body}" if header_path else body
        key = f"{source}|{section_id}|{part_index}|html@{self.version}"
        return {
            "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
            "text": text,
            "header_path": header_path,
            "section_id": section_id,
            "token_count": len(text.split()),
            "source": source,
            "strategy": "html",
            "version": self.version,
            "part_index": part_index,
        }
```

### `templates/doc-chunk-schema.json`

```json
{
  "_header": {
    "purpose": "JSON Schema for one document-structure chunk",
    "consumes": "chunk dict from MarkdownChunker / HTMLChunker",
    "produces": "pass/fail validation",
    "depends-on": "content/02-output-contract.xml",
    "token-budget-impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "faion://chunking-document-structure/chunk.schema.json",
  "type": "object",
  "required": [
    "id",
    "text",
    "header_path",
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
    "header_path": {
      "type": "string"
    },
    "section_id": {
      "type": "string"
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
      "enum": [
        "markdown",
        "html"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "part_index": {
      "type": [
        "integer",
        "null"
      ],
      "minimum": 0
    }
  }
}
```
