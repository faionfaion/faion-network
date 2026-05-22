---
slug: chunking-code-ast
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: CodeChunker splits Python source via the `ast` module at FunctionDef, AsyncFunctionDef, and ClassDef boundaries, emitting chunks with name, type, docstring, and line range.
content_id: "3f02c6312ddf157e"
tags: [chunking, code-chunking, ast, rag, code-search]
---
# Code Chunking via AST and Function Boundaries

## Summary

**One-sentence:** CodeChunker splits Python source via the `ast` module at FunctionDef, AsyncFunctionDef, and ClassDef boundaries, emitting chunks with name, type, docstring, and line range.

**One-paragraph:** CodeChunker splits Python source via the `ast` module at FunctionDef, AsyncFunctionDef, and ClassDef boundaries, emitting chunks with name, type, docstring, and line range. JavaScript and TypeScript fall back to regex patterns for function and class extraction. Generic line-based splitting handles unsupported languages or parse errors.

## Applies If (ALL must hold)

- Ingesting source code repositories into a code-search RAG (Python AST, JS/TS function-level splitting).
- Building a code documentation assistant that answers "what does function X do?" or "show me examples of pattern Y".
- Any pipeline where the retrieval query maps naturally to function or class units (e.g., finding all async route handlers).
- Multi-language codebases where Python is the primary language and JS/TS is secondary.

## Skip If (ANY kills it)

- Code chunking via JS regex patterns on TypeScript with decorators or generics — AST parsers handle those correctly; regex does not. Use tree-sitter bindings instead.
- Corpora entirely in languages not supported by ast or the JS regex patterns — the generic line-based fallback silently drops class and function metadata.
- Documentation or prose files — use chunking-document-structure or chunking-semantic instead.
- Files with syntax errors that prevent ast.parse — the fallback to generic splitting silently drops all metadata; surface this to the caller as a warning.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/rag-engineer/`
