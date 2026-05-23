# Embedding Models

## Summary

**One-sentence:** Picks embedding model for a corpus class (general/code/multilingual) — pins model+version, handles Cohere input_type, OpenAI dimensions, Mistral/Voyage caveats, SentenceTransformer singleton.

**One-paragraph:** Each provider has quirks that, when missed, cost recall silently: OpenAI returns batches out of order, Cohere ignores input_type → 5–10% loss, Mistral truncates at 512 tokens, BGE-M3 sparse format mismatches dense DB clients. This methodology produces a `ModelSelector` artefact + bench harness that pins model name + version, applies provider tuning, and benchmarks Recall@10 against the domain set.

**Ефективно для:**

- New project — pick embedding model + provider.
- Migration between providers — confirm portability.
- Code corpora — Voyage-code-3, OpenAI text-embedding-3-large.
- Multilingual — Voyage, BGE-M3, Cohere embed-multilingual.
- High-storage-cost corpus — Matryoshka dim reduction with OpenAI v3.

## Applies If (ALL must hold)

- New project OR provider migration.
- Domain bench set available (≥50 pairs).
- Vector DB chosen with metric pinned.
- Named owner.

## Skip If (ANY kills it)

- Existing model meets recall target + no migration pending.
- No bench set.
- Single-provider lock-in for regulatory reasons.
- Greenfield prototype.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Candidate model catalog | YAML | platform |
| Domain bench set | JSONL | eval repo |
| Vector DB config (metric + dim) | YAML | platform |
| Token budget for bench | int | finops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-generation]]` | Calling convention. |
| `[[embedding-applications]]` | Pipeline that uses the choice. |
| `[[rag-bench-harness-template]]` | Bench. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 rules + run/skip terminals | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for model-selection artefact | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 5-step: shortlist → tune → bench → pick winner → deploy | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus class to model family | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shortlist` | sonnet | Provider-aware judgment. |
| `run-bench` | haiku | Numeric. |
| `pick-winner` | opus | Multi-axis trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_pipeline.py` | Pipeline class with bench + selection. |
| `templates/model-selection.json` | Selection artefact skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-models.py` | Validate model-selection artefact | Pre-commit + CI |

## Related

- [[embedding-generation]]
- [[embedding-applications]]
- [[embedding-caching]]
- [[embedding-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes corpus class (general/code/multilingual/legal-biomedical) to candidate family. The bench gate picks the winner within family.
