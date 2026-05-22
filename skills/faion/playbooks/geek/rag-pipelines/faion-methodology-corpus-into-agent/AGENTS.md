---
slug: faion-methodology-corpus-into-agent
tier: geek
group: rag-pipelines
persona: P7
goal: build-ship
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: No internal RAG → faion methodology corpus embedded as reasoning prior for an in-house vertical agent with ingestion, retrieval, eval, governance.
content_id: de0986df5b8c1714
methodology_refs:
  - chunking-document-structure
  - chunking-semantic
  - chunking-production-service
  - kb-codebase-rag-symbol-chunked
  - embedding-model-selection
  - embeddings-evaluation
  - embeddings-batch-and-cache
  - embedding-caching
  - hybrid-search-implementation
  - rag-architecture
  - reranking-two-stage
  - reranking-diversity-mmr
  - reranking-pipeline-integration
  - rerank-before-reasoning
  - manifest-then-fetch
  - progressive-disclosure-skills
  - file-reference-passing
  - auto-evict-tool-results
  - terse-default-tool-output
  - compaction-preserve-refs
  - rag-eval-pipeline
  - rag-eval-production-monitoring
  - rag-eval-retrieval-metrics
  - kb-versioned-agent-memory-files
  - gov-license-compliance-scan
  - eu-ai-act-compliance
---

# Methodology corpus integration: faion-into-our-agent (2 weeks)

**Playbook slug:** `faion-methodology-corpus-into-agent`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

No internal RAG → faion methodology corpus embedded as reasoning prior for an in-house vertical agent with ingestion, retrieval, eval, governance.

## Scope

Embed the faion knowledge base as a reasoning prior for an in-house vertical agent: ingestion, chunking, retrieval, reranking, eval, plus governance / licence / drift hygiene. Output: agent answers cite faion methodologies with traceable IDs.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- End-user-facing search UI — not the goal
- Multi-tenant corpus isolation — out of scope

### Prerequisites

- Existing vertical agent with at least one tool slot
- Vector DB or readiness to deploy one

## Success criteria

The playbook is done when:
- Chunked + indexed faion corpus reachable from agent
- Reranker raising P@5 over baseline
- Eval pipeline scoring retrieval and generation
- Licence + governance audit passed
- Drift alert wired on retrieval distribution

## Stages

### Stage 1: Ingest & Chunk

**Intent:** Chunk faion methodologies by document structure and semantics.

**Tasks:**
- Walk knowledge/ tree and extract semantic units
- Choose chunking strategy: structure + semantic
- Stand up production chunking service

**Methodologies in chain:**
- `chunking-document-structure` → `geek/ai/rag-engineer/chunking-document-structure`
- `chunking-semantic` → `geek/ai/rag-engineer/chunking-semantic`
- `chunking-production-service` → `geek/ai/rag-engineer/chunking-production-service`
- `kb-codebase-rag-symbol-chunked` → `geek/sdlc-ai/kb-codebase-rag-symbol-chunked`

**Outputs:**
- chunks.jsonl
- Chunking service deployed

**Decision gate:**
> Advance when chunk count and avg-token length are stable.

### Stage 2: Embed & Retrieve

**Intent:** Pick embedding model, cache aggressively, wire hybrid search.

**Tasks:**
- Pick embedding model with eval
- Batch + cache embeddings
- Wire BM25 + vector hybrid search

**Methodologies in chain:**
- `embedding-model-selection` → `geek/ai/rag-engineer/embedding-model-selection`
- `embeddings-evaluation` → `geek/ai/ml-engineer/embeddings-evaluation`
- `embeddings-batch-and-cache` → `geek/ai/ml-engineer/embeddings-batch-and-cache`
- `embedding-caching` → `geek/ai/rag-engineer/embedding-caching`
- `hybrid-search-implementation` → `geek/ai/rag-engineer/hybrid-search-implementation`
- `rag-architecture` → `geek/ai/rag-engineer/rag-architecture`

**Outputs:**
- Embedding cache
- Hybrid search endpoint

**Decision gate:**
> Advance when P@5 ≥ baseline + 10%.

### Stage 3: Rerank & Compose

**Intent:** Two-stage rerank with diversity; wire into agent context.

**Tasks:**
- Add two-stage reranker
- Add MMR diversity
- Integrate into context pipeline

**Methodologies in chain:**
- `reranking-two-stage` → `geek/ai/rag-engineer/reranking-two-stage`
- `reranking-diversity-mmr` → `geek/ai/rag-engineer/reranking-diversity-mmr`
- `reranking-pipeline-integration` → `geek/ai/rag-engineer/reranking-pipeline-integration`
- `rerank-before-reasoning` → `geek/ai/ai-agents/rerank-before-reasoning`
- `manifest-then-fetch` → `geek/ai/ai-agents/manifest-then-fetch`
- `progressive-disclosure-skills` → `geek/ai/ai-agents/progressive-disclosure-skills`
- `file-reference-passing` → `geek/ai/ai-agents/file-reference-passing`
- `auto-evict-tool-results` → `geek/ai/ai-agents/auto-evict-tool-results`
- `terse-default-tool-output` → `geek/ai/ai-agents/terse-default-tool-output`
- `compaction-preserve-refs` → `geek/ai/ai-agents/compaction-preserve-refs`

**Outputs:**
- Reranker service
- Context composition rules

**Decision gate:**
> Advance when NDCG and answer-grounding both improve.

### Stage 4: Eval & Monitor

**Intent:** End-to-end RAG eval + production monitoring + drift signal.

**Tasks:**
- Wire RAG eval pipeline
- Monitor retrieval distribution in prod
- Pin schemas + memory snapshots

**Methodologies in chain:**
- `rag-eval-pipeline` → `geek/ai/rag-engineer/rag-eval-pipeline`
- `rag-eval-production-monitoring` → `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `rag-eval-retrieval-metrics` → `geek/ai/rag-engineer/rag-eval-retrieval-metrics`
- `kb-versioned-agent-memory-files` → `geek/sdlc-ai/kb-versioned-agent-memory-files`

**Outputs:**
- Eval CI job
- Drift dashboard

**Decision gate:**
> Advance when drift signal correctly fires on a planted shift.

### Stage 5: Governance

**Intent:** Licence audit and AI Act / governance hygiene.

**Tasks:**
- Run licence-compliance scan on corpus
- Map governance obligations
- Sign off on deployment

**Methodologies in chain:**
- `gov-license-compliance-scan` → `geek/sdlc-ai/gov-license-compliance-scan`
- `eu-ai-act-compliance` → `geek/ai/ml-engineer/eu-ai-act-compliance`

**Outputs:**
- Licence report
- Governance sign-off

**Decision gate:**
> Ship only when licence + governance both pass.

## Common pitfalls

- Treating eval scores as ground truth without judge calibration
- Shipping prompt or model changes without a regression gate
- Skipping shadow rollout for routing or model swaps

## Quality checklist (self-review)

- Can I roll back this change in one step?
- Is the regression eval committed BEFORE the fix?
- Are tool / schema versions pinned in the manifest?

## Related playbooks

- `eval-harness-continuous-benchmark-suite`
- `agent-observability-drift-detection-rollout`
- `production-agent-eval-harness-week-1`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **faion-cli-as-agent-skill** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **methodology-corpus-licence-bundle** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **retrieval-drift-alerting-recipe** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

This is a build-once, maintain-forever pattern. The Ingest & Chunk stage sets the schema for everything downstream; revisiting it later means re-embedding the entire corpus, which is expensive. Pick a chunking policy with structure-awareness from day one, even if you start with a simpler semantic chunker. The faion corpus has stable directory structure (`tier/group/skill/methodology`) — exploit that as a chunk-id namespace.

Embedding model selection should be made on evaluation, not vibes. Stage 2 mandates `embeddings-evaluation` — actually run it. Default to a cacheable, batched embedding API; the cache hit rate is the main lever on ongoing cost.

The reranker stage is where most teams find their biggest quality lift. Two-stage rerank with MMR for diversity outperforms a single dense retrieval on this corpus because of the heavy topical overlap between methodologies. Plan for it; do not treat it as optional.

Drift detection is the silent killer. Retrieval distributions shift as the corpus grows; a planted-shift test in Stage 4 should be the gate. If you cannot detect the planted shift, the alert will not fire on the real one. The brainstorm flags `retrieval-drift-alerting-recipe` as a gap; until it is written, copy the input-distribution drift pattern from playbook 5.

Governance is non-optional in EU jurisdictions. Run the licence scan on every corpus update; methodology body changes can introduce new third-party citations the scan must catch.

## CLI usage

```
faion get-content faion-methodology-corpus-into-agent --format md       # human-readable rendering
faion get-content faion-methodology-corpus-into-agent --format context  # agent-optimised context bundle
faion get-content faion-methodology-corpus-into-agent --format json     # raw structured form
```
