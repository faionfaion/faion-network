# Codebase RAG with Symbol-Boundary Chunking

## Summary

**One-sentence:** Build the coding-agent vector index by chunking on AST symbol boundaries — one chunk per function/class/method — padded with file path, enclosing class signature, and sibling doc comments.

**One-paragraph:** Codebase RAG with Symbol-Boundary Chunking produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Building or rebuilding a vector index for a coding agent on a real codebase ≥ 50 KLOC.
- Replacing a sliding-window or fixed-line chunker that yields poor recall.
- Multi-language repo where one chunker must work across languages.
- Agent needs to retrieve self-contained, runnable code units — not arbitrary slices.

## Applies If (ALL must hold)

- Codebase ≥ 50 KLOC where fixed-window chunks lose semantic boundaries.
- An AST parser exists for every language in the repo (tree-sitter, LSP, or native).
- Vector store supports metadata filters (file path, symbol kind).
- Coding agent consumes top-K chunks and needs each chunk to be self-contained.

## Skip If (ANY kills it)

- Codebase < 5 KLOC — full-file context fits the model window.
- Repo is mainly prose / config — symbol chunking gains nothing.
- AST parser unavailable for the dominant language — fall back to line chunks.
- Real-time latency budget < 50 ms per query — symbol chunking adds index-time cost.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Codebase clone | git repo | source control |
| AST parser config | tree-sitter grammars or LSP | language-eng |
| Vector store | Qdrant / Weaviate / pgvector | platform |
| Embedding model | bge-large or voyage-code-3 etc. | ml-eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kb-symbol-index-fresh-tags]] | Symbol index is the upstream artefact |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ast_parse_repo` | haiku | Mechanical AST walk. |
| `chunk_padding_strategy` | sonnet | Choose context windows per symbol. |
| `metadata_attach` | haiku | Add file path + symbol kind attrs. |
| `retrieval_eval` | opus | MRR / recall@K eval design. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunker-config.yaml` | Tree-sitter / LSP chunker configuration. |
| `templates/retrieval-eval-set.jsonl` | Sample eval set (query → expected chunk ids). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-codebase-rag-symbol-chunked.py` | Validate the chunker config against the schema. | pre-merge of chunker change |

## Related

- [[kb-symbol-index-fresh-tags]]
- [[kb-agents-md-context-pyramid]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
