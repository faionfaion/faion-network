# Vector Database Comparison

## Summary

**One-sentence:** Picks a vector database (Chroma / Qdrant / Weaviate / pgvector / Pinecone / Milvus) from a scored matrix anchored on year-1 scale, hosting model, hybrid-search need, and existing infra.

**One-paragraph:** Produces a one-page decision record: candidate DBs scored across {year_one_scale, hosting (self/managed), hybrid_search, payload_filter_perf, multi_tenant, existing_postgres, team_familiarity}. Output is a structured `decision.json` with the chosen DB + 1–3 fallbacks + rationale + migration plan. Reusable: re-run when corpus crosses a scale threshold or vendor pricing shifts.

**Ефективно для:** Founder picking the vector DB before signing any contract or writing ingest code — closes the gap between "Pinecone is best" vendor claims and a defensible, infra-anchored decision.

## Applies If (ALL must hold)

- New RAG project OR existing prototype crossing a scale / tenancy threshold.
- ≥2 DB candidates are on the table.
- A representative query pattern is known (latency + filter + hybrid needs).
- Named decision owner with sign-off authority.

## Skip If (ANY kills it)

- DB is already deployed and migration cost dominates any quality gain.
- Corpus is < 10k vectors — any DB works; pick the simplest.
- No representative queries available — benchmarks without queries mislead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Year-1 vector count + growth | int | product roadmap |
| Query pattern | list of representative queries + filters | UX research |
| Existing infra | list (Postgres, Kubernetes, Vercel, etc.) | architecture review |
| Hosting policy | self vs managed | security/finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/db-chroma` · `db-qdrant` · `db-weaviate` | Per-DB tradeoffs feed the matrix. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: anchor on year-1 scale not peak, score with weighted criteria, document fallbacks, named owner, version on re-decide | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision.json | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vendor-claim only, benchmarks without queries, no fallback, missing migration plan | ~700 |
| `content/06-decision-tree.xml` | essential | Routes by scale + hosting + hybrid + existing-postgres | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `populate-matrix` | sonnet | Multi-criteria scoring with judgement. |
| `recommend` | opus | Strategic justification + migration plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision.md` | Markdown decision record skeleton. |
| `templates/decision-schema.json` | JSON Schema for `decision.json`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-db-comparison.py` | Verify decision.json fields, fallback present, migration plan non-empty. | Pre sign-off. |

## Related

- [[db-chroma]] · [[db-qdrant]] · [[db-weaviate]] · [[rag-architecture]] · [[ai-option-cost-grid-template]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by year-1 vectors, hybrid-search need, existing Postgres footprint, and hosting policy to a DB recommendation with 1–3 fallbacks.
