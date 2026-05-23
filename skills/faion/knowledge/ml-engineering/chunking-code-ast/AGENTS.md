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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-code-ast.py` | Validate emitted chunk list against schema; warn on missing docstring; check dedup. | After chunker run, before embedding. |

## Related

- [[chunking-basics]] — token + metadata invariants.
- [[chunking-document-structure]] — sibling for Markdown / HTML.
- [[chunking-production-service]] — wraps this chunker in a service.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides between Python AST, JS/TS tree-sitter, JS/TS regex fallback, and generic line-based on syntax error. Always use the tree before instantiating a chunker so the fallback path is intentional, not accidental.
