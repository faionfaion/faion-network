---
slug: rag-chunking-strategy-bench
tier: geek
group: rag-pipelines
persona: P7
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Fixed corpus + frozen test queries → decide which chunking + retrieval combo wins this week and ship the winner behind a flag.
content_id: 8e7782fcb57ffc0f
methodology_refs:
  - schema-version-pinning
  - rag-eval-test-set-generation
  - chunking-document-structure
  - chunking-semantic
  - chunking-code-ast
  - chunking-production-service
  - hybrid-search-implementation
  - reranking-two-stage
  - reranking-diversity-mmr
  - rag-eval-retrieval-metrics
  - rag-eval-generation-metrics
  - rag-eval-ab-testing
---

# RAG chunking strategy bench

**Playbook slug:** `rag-chunking-strategy-bench`  
**Tier:** geek  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

Fixed corpus + frozen test queries → decide which chunking + retrieval combo wins this week and ship the winner behind a flag.

## Scope

On a fixed corpus + frozen test queries, decide which chunking + retrieval combo wins this week and ship the winner behind a flag. Champion-challenger discipline.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Building the eval set itself — see playbook 1
- Multi-tenant corpus design

### Prerequisites

- Frozen test set with judge rubrics
- Indexable corpus snapshot

## Success criteria

The playbook is done when:
- ≥3 chunking + retrieval combos run
- Champion picked by NDCG + groundedness
- Pinned schema + version manifest
- Shipped behind flag with rollback

## Stages

### Stage 1: Setup

**Intent:** Snapshot corpus + queries + judge.

**Tasks:**
- Lock corpus snapshot
- Freeze query set + judges
- Pin schema version

**Methodologies in chain:**
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`
- `rag-eval-test-set-generation` → `geek/ai/rag-engineer/rag-eval-test-set-generation`

**Outputs:**
- Corpus snapshot id
- Frozen test set

**Decision gate:**
> Advance only when inputs are frozen.

### Stage 2: Chunk Variants

**Intent:** Build 3+ chunking variants.

**Tasks:**
- Document-structure variant
- Semantic variant
- Code-AST variant if applicable
- Production-service chunking variant

**Methodologies in chain:**
- `chunking-document-structure` → `geek/ai/rag-engineer/chunking-document-structure`
- `chunking-semantic` → `geek/ai/rag-engineer/chunking-semantic`
- `chunking-code-ast` → `geek/ai/rag-engineer/chunking-code-ast`
- `chunking-production-service` → `geek/ai/rag-engineer/chunking-production-service`

**Outputs:**
- Variant index set

**Decision gate:**
> Advance only when each variant indexed cleanly.

### Stage 3: Retrieve & Rerank

**Intent:** Hybrid retrieval + rerank for each variant.

**Tasks:**
- Run hybrid search
- Two-stage rerank
- Diversity rerank with MMR

**Methodologies in chain:**
- `hybrid-search-implementation` → `geek/ai/rag-engineer/hybrid-search-implementation`
- `reranking-two-stage` → `geek/ai/rag-engineer/reranking-two-stage`
- `reranking-diversity-mmr` → `geek/ai/rag-engineer/reranking-diversity-mmr`

**Outputs:**
- Per-variant retrieval traces

**Decision gate:**
> Advance only when each variant produces comparable traces.

### Stage 4: Score

**Intent:** Eval each variant on retrieval + generation metrics.

**Tasks:**
- Retrieval metrics (recall, NDCG)
- Generation metrics (groundedness)
- A/B significance check

**Methodologies in chain:**
- `rag-eval-retrieval-metrics` → `geek/ai/rag-engineer/rag-eval-retrieval-metrics`
- `rag-eval-generation-metrics` → `geek/ai/rag-engineer/rag-eval-generation-metrics`
- `rag-eval-ab-testing` → `geek/ai/rag-engineer/rag-eval-ab-testing`

**Outputs:**
- Scorecard

**Decision gate:**
> Advance only when one variant clearly wins or is tied.

### Stage 5: Ship Winner

**Intent:** Promote winner behind feature flag with rollback.

**Tasks:**
- Land winner behind flag
- Document rollback

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Flag-gated rollout

**Decision gate:**
> Ship only after rollback is exercised.

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
- **rag-bench-harness-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **champion-challenger-pattern-rag** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Champion-challenger discipline is the entire point. Without a frozen corpus snapshot and a frozen test set, you cannot tell whether week-over-week scores moved because the chunking changed or because the corpus did. Stage 1 enforces both freezes; do not skip them.

Three variants is the minimum because two-variant comparisons are too easily dominated by noise on a single rough query. Pick variants that differ on real axes: chunk size, structure-awareness, semantic similarity threshold. Code-AST chunking is the right fourth variant when the corpus is heavily code-shaped.

Retrieval metrics alone do not pick the winner. A variant that improves recall but degrades groundedness in the generated answer is a regression downstream. Stage 4 mandates both retrieval and generation metrics; weight by which side of the pipeline you are optimizing.

A/B significance check matters because chunking lifts are usually small (2-5%). With small lifts you need real statistical care or the winner you ship is noise. Default to ≥1000 evaluated queries per variant before calling a winner. Brainstorm flags rag-bench-harness-template and a champion-challenger pattern for RAG as open gaps.

Ship behind a feature flag with documented rollback. The first week of production traffic on a new chunker is the real test; the bench is a filter, not a guarantee.

## CLI usage

```
faion get-content rag-chunking-strategy-bench --format md       # human-readable rendering
faion get-content rag-chunking-strategy-bench --format context  # agent-optimised context bundle
faion get-content rag-chunking-strategy-bench --format json     # raw structured form
```
