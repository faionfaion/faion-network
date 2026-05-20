---
slug: kb-codebase-rag-symbol-chunked
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When building a vector index for a coding agent, chunk by AST symbol — one chunk per top-level function, class, or method, padded with the file path, the enclosing class signature, and 1-2 sibling-doc-comments — instead of fixed character or line windows.
content_id: "d0df6586e4f756c5"
tags: [rag, codebase-indexing, symbol-chunking, mcp, vector-search]
---
# Codebase RAG with Symbol-Boundary Chunking

## Summary

**One-sentence:** When building a vector index for a coding agent, chunk by AST symbol — one chunk per top-level function, class, or method, padded with the file path, the enclosing class signature, and 1-2 sibling-doc-comments — instead of fixed character or line windows.

**One-paragraph:** When building a vector index for a coding agent, chunk by AST symbol — one chunk per top-level function, class, or method, padded with the file path, the enclosing class signature, and 1-2 sibling-doc-comments — instead of fixed character or line windows. Each chunk carries metadata {path, symbol, kind, signature, sha} and is keyed by sha:path:symbol so retrieval returns whole, compilable units, never half-functions. Re-embed only chunks whose sha changed; the index is rebuilt incrementally on every commit and consumed by the agent via an MCP "code search" tool, never by string-grepping the index.

## Applies If (ALL must hold)

- Repos large enough that the agent cannot keep the whole tree in context (>10k LOC).
- Multi-language repos where one chunker (tree-sitter) covers everything.
- Q&A / "explain this codebase" agents that surface context to humans, not just to other agents.
- Onboarding flows where the agent narrates "here's the auth pipeline" by stitching retrieved chunks.

## Skip If (ANY kills it)

- Repos under ~5k LOC — full-tree context fits in a single Claude/GPT call.
- Agents that exclusively edit code with a working LSP / symbol index — a vector index is duplicate work.
- Compliance-restricted code where the embedding model would leak source to a third-party API.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
