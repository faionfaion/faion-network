# Codebase RAG with Symbol-Boundary Chunking

## Summary

When building a vector index for a coding agent, chunk by AST symbol — one chunk per top-level function, class, or method, padded with the file path, the enclosing class signature, and 1-2 sibling-doc-comments — instead of fixed character or line windows. Each chunk carries metadata `{path, symbol, kind, signature, sha}` and is keyed by `sha:path:symbol` so retrieval returns whole, compilable units, never half-functions. Re-embed only chunks whose `sha` changed; the index is rebuilt incrementally on every commit and consumed by the agent via an MCP "code search" tool, never by string-grepping the index.

## Why

Fixed-size chunking (the default in most generic RAG starter kits) splits code mid-function and ranks a chunk that ends at line 47 of an 80-line method as the top hit; the agent then tries to use a half-function as ground truth. Symbol-boundary chunking matches how humans cite code: by function, by class, by method. Anthropic's `claude-context` reference, Cursor's 2025 indexing post, and Sourcegraph Cody's chunker all converge on this pattern. The metadata-rich chunks let the agent do hybrid search (vector recall + structured filter on `kind=function AND path~auth/`), which beats pure vector top-k by 30-50% on real "find the implementation" tasks.

## When To Use

- Repos large enough that the agent cannot keep the whole tree in context (>10k LOC).
- Multi-language repos where one chunker (tree-sitter) covers everything.
- Q&A / "explain this codebase" agents that surface context to humans, not just to other agents.
- Onboarding flows where the agent narrates "here's the auth pipeline" by stitching retrieved chunks.

## When NOT To Use

- Repos under ~5k LOC — full-tree context fits in a single Claude/GPT call.
- Agents that exclusively edit code with a working LSP / symbol index — a vector index is duplicate work.
- Compliance-restricted code where the embedding model would leak source to a third-party API.

## Content

| File | What's inside |
|------|---------------|
| `content/01-symbol-chunk-rule.xml` | The mandatory chunk-by-symbol rule, the metadata schema, and the SHA-keyed dedupe pattern. |
| `content/02-incremental-index-rule.xml` | How the index is rebuilt incrementally on commit and exposed to the agent via MCP. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunk_schema.json` | JSON-Schema for the per-chunk metadata record. |
| `templates/treesitter_chunker.py` | Reference 60-line chunker that walks tree-sitter AST and emits one record per top-level symbol. |
