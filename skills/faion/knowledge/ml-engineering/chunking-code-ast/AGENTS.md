# Code Chunking via AST and Function Boundaries

## Summary

**One-sentence:** Splits source code at function and class boundaries via Python `ast` (or tree-sitter for JS/TS), emitting chunks carrying name, type, docstring, and line range for code-search RAG.

**One-paragraph:** CodeChunker dispatches by language. Python uses `ast.parse` on the full source and walks FunctionDef, AsyncFunctionDef, ClassDef nodes. JavaScript/TypeScript use tree-sitter (regex is a last-resort fallback). Each chunk carries name, type, docstring, start_line, end_line. SyntaxError or unsupported language falls back to a generic line splitter that MUST emit a warning so the caller can flag unindexed metadata. Overlapping class/method chunks are deduplicated by (name, start_line) before indexing.

**Ефективно для:** RAG engineer ingesting a code repo for "what does function X do" / "show examples of pattern Y" queries — closes the gap between line-based chunkers (which destroy function boundaries) and human code-search intent.

## Applies If (ALL must hold)

- Ingesting source code into a RAG / semantic code-search index.
- Primary language is Python OR JS/TS with tree-sitter available.
- Queries map naturally to function or class units (e.g. "find all async route handlers").
- Caller is prepared to handle a warning when AST parse fails.

## Skip If (ANY kills it)

- Corpus is prose or documentation — load [[chunking-document-structure]] or [[chunking-semantic]].
- TypeScript with decorators / generics AND tree-sitter unavailable — regex path fails silently; defer until tree-sitter is installed.
- Files with syntax errors with no fallback policy — generic line-based output silently drops metadata.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source files | .py / .js / .ts / .tsx | repo checkout |
| Language detector | extension map | file scan |
| tree-sitter bindings | python wheel | `pip install tree-sitter` for JS/TS |
| Embedding model token cap | int | matches downstream embedder |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/chunking-basics` | Token measurement + metadata-at-creation invariants apply here too. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: dispatch by language, AST primary path, dedup overlapping chunks, log on fallback, version on strategy change | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for a code chunk: id, text, type, name, docstring, start_line, end_line, language, source | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: regex on complex TS, silent fallback, no dedup, ignoring max_chunk_size on long functions | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: detect lang → parse → walk nodes → emit records → dedup → log | ~800 |
| `content/05-examples.xml` | medium | Worked example: CodeChunker on a Django views.py emitting class + 3 method chunks | ~500 |
| `content/06-decision-tree.xml` | essential | Routes language + parse-status to strategy + fallback path | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect-language` | haiku | Extension + shebang classification. |
| `parse-and-chunk` | haiku | Mechanical AST walk, no LLM judgement. |
| `summarise-docstring` | sonnet | When docstring missing, generate one-line synopsis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/code_chunker.py` | CodeChunker reference with Python AST + JS/TS tree-sitter dispatch and generic fallback. |
| `templates/code-chunk-schema.json` | JSON Schema for the per-chunk output record. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-code-ast.py` | Validate emitted chunk list against schema; warn on missing docstring; check dedup. | After chunker run, before embedding. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[chunking-basics]] — token + metadata invariants.
- [[chunking-document-structure]] — sibling for Markdown / HTML.
- [[chunking-production-service]] — wraps this chunker in a service.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides between Python AST, JS/TS tree-sitter, JS/TS regex fallback, and generic line-based on syntax error. Always use the tree before instantiating a chunker so the fallback path is intentional, not accidental.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/code_chunker.py`

```python
"""CodeChunker — AST-first dispatch with logged generic fallback."""
from __future__ import annotations

import ast
import hashlib
import logging

logger = logging.getLogger("chunking_code_ast")


class CodeChunker:
    def __init__(self, language: str = "python", version: str = "1.0.0", max_chunk_size: int = 800) -> None:
        self.language = language
        self.version = version
        self.max_chunk_size = max_chunk_size

    def chunk(self, code: str, source: str) -> list[dict]:
        if self.language == "python":
            return self._chunk_python(code, source)
        if self.language in {"javascript", "typescript"}:
            return self._chunk_generic(code, source, reason="tree-sitter-not-wired-in-template")
        return self._chunk_generic(code, source, reason="unsupported-language")

    def _chunk_python(self, code: str, source: str) -> list[dict]:
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            logger.warning("fallback to generic", extra={"file": source, "language": "python", "reason": f"SyntaxError: {exc}"})
            return self._chunk_generic(code, source, reason="syntax-error")
        lines = code.split("\n")
        records: list[dict] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno
                end_line = getattr(node, "end_lineno", start_line)
                text = "\n".join(lines[start_line - 1:end_line])
                kind = (
                    "class" if isinstance(node, ast.ClassDef)
                    else "async_function" if isinstance(node, ast.AsyncFunctionDef)
                    else "function"
                )
                records.append({
                    "id": self._cid(source, start_line),
                    "text": text,
                    "type": kind,
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or "",
                    "start_line": start_line,
                    "end_line": end_line,
                    "language": "python",
                    "source": source,
                    "strategy": "ast",
                    "version": self.version,
                    "fallback": False,
                })
        return self._dedup(records)

    def _chunk_generic(self, code: str, source: str, reason: str) -> list[dict]:
        logger.warning("generic fallback", extra={"file": source, "language": self.language, "reason": reason})
        lines = code.split("\n")
        records: list[dict] = []
        buf: list[str] = []
        size = 0
        start_line = 1
        for i, line in enumerate(lines, start=1):
            buf.append(line)
            size += len(line.split())
            if size >= self.max_chunk_size:
                records.append(self._generic_record(source, start_line, i, "\n".join(buf)))
                buf, size, start_line = [], 0, i + 1
        if buf:
            records.append(self._generic_record(source, start_line, len(lines), "\n".join(buf)))
        return records

    def _generic_record(self, source: str, start: int, end: int, text: str) -> dict:
        return {
            "id": self._cid(source, start),
            "text": text, "type": "code_block", "name": "",
            "docstring": "", "start_line": start, "end_line": end,
            "language": "generic", "source": source,
            "strategy": "generic", "version": self.version, "fallback": True,
        }

    def _dedup(self, records: list[dict]) -> list[dict]:
        seen: set[tuple[str, int]] = set()
        keep: list[dict] = []
        # policy A: drop class chunk when its range fully contains other records
        class_records = [r for r in records if r["type"] == "class"]
        contained_lines: set[tuple[str, int]] = set()
        for c in class_records:
            for other in records:
                if other is c:
                    continue
                if other["source"] == c["source"] and c["start_line"] < other["start_line"] <= c["end_line"]:
                    contained_lines.add((c["source"], c["start_line"]))
        for r in records:
            key = (r["source"], r["start_line"])
            if (r["source"], r["start_line"]) in contained_lines:
                continue
            if key in seen:
                continue
            seen.add(key)
            keep.append(r)
        return keep

    def _cid(self, source: str, start_line: int) -> str:
        key = f"{source}|{start_line}|ast@{self.version}"
        return hashlib.md5(key.encode("utf-8")).hexdigest()
```

### `templates/code-chunk-schema.json`

```json
{
  "_header": {
    "purpose": "JSON Schema for one code chunk emitted by CodeChunker",
    "consumes": "chunk dict from CodeChunker.chunk()",
    "produces": "pass/fail validation result",
    "depends-on": "content/02-output-contract.xml",
    "token-budget-impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "faion://chunking-code-ast/chunk.schema.json",
  "type": "object",
  "required": [
    "id",
    "text",
    "type",
    "language",
    "source",
    "start_line",
    "end_line",
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
    "type": {
      "type": "string",
      "enum": [
        "function",
        "async_function",
        "class",
        "method",
        "arrow_function",
        "code_block"
      ]
    },
    "name": {
      "type": "string"
    },
    "docstring": {
      "type": "string"
    },
    "start_line": {
      "type": "integer",
      "minimum": 1
    },
    "end_line": {
      "type": "integer",
      "minimum": 1
    },
    "language": {
      "type": "string",
      "enum": [
        "python",
        "javascript",
        "typescript",
        "generic"
      ]
    },
    "source": {
      "type": "string",
      "minLength": 1
    },
    "strategy": {
      "type": "string",
      "enum": [
        "ast",
        "tree-sitter",
        "regex",
        "generic"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "fallback": {
      "type": "boolean"
    }
  }
}
```
