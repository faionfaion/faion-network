# Placement — Graphs & Retrieval Structure
**Slice:** GraphRAG family, RAPTOR, memory graphs, code graphs · **Author pass:** 10 of 10 · **Date:** 2026-08-04

## Already covered by context-graph-engineering — do not duplicate

| Topic | Covered? | Gap remaining |
|---|---|---|
| MS GraphRAG cost, 380x spread; flat+rerank beats graph on facts | Yes — R1/R2, F1 | None |
| Warrant gate; derived-vs-extracted edges; closed vocabulary; k^h budget; CI integrity | Yes — R1, R3–R5, R7 | None |
| Bitemporal expiry (Graphiti) | Yes — R6, F4 | **Admission** — what enters memory at all (mem0/Letta disagree) |
| LazyGraphRAG | Cited in R2 only | Decision-tree says "prefer a lazy pattern", never defines it |
| RAPTOR / tree retrieval | No | Whole object: what the `warrant: none` hierarchy actually is |
| Code graphs (SCIP, stack-graphs, Aider PageRank) | Ranking function named in contract only | Whole object |
| Measuring incumbent cost | **Named a prerequisite in Skip If — supplied nowhere** | The measurement itself |

## Verdict summary

| Approach | Decision | Target path | Tier |
|---|---|---|---|
| Cost measurement (the gate's missing input) | New methodology | `knowledge/ai-core/retrieval-cost-per-answer-audit/` | solo |
| RAPTOR / tree retrieval | New methodology | `knowledge/ai-agents/hierarchical-index-compression/` | pro |
| Code graphs · Aider repo map | New methodology | `knowledge/dev/repo-map-for-coding-agents/` | pro |
| Graphiti / mem0 / Letta | New methodology (admission only) | `knowledge/ai-agents/agent-memory-admission-policy/` | pro |
| LazyGraphRAG | Extend existing | `context-graph-engineering/content/04-deferred-construction.xml` | pro |
| Cost audit as a run | New playbook | `playbooks/optimize-tune/retrieval-structure-cost-audit/` | solo |
| MS GraphRAG mechanics | Reject — four `ml-engineering/graph-rag-*` slugs exist | — | — |
| HippoRAG2 / KGP / LightRAG / nano-graphrag / HNSW | Reject as slugs; benchmark rows inside A–C | — | — |
| "Graph engineering" as a term | Reject | — | — |

## Workflow changes

**1. `workflows/idea-to-prod/content/30-token-discipline.xml`** — append a sixth section, *Index reads are dispatch costs*, after *Orchestrator does not redo subagent work*. Rule: the orchestrator MUST NOT read an L2 index above a declared ceiling (12k tokens) into its own context; it dispatches a retrieval subagent that returns **leaf paths plus one-line reasons only**. Second rule: when the leaf path is known from a prior tick, skip both levels. Rationale carries our own number — two-level retrieval costs 13–84k tokens per lookup, median ~33k, to deliver a median 3.3k-token body; `dev/INDEX.xml` alone is ~30k. The index, not the answer, is the bill. Replaces nothing: the file disciplines dispatch and summaries and is silent on retrieval.

**2. `workflows/catalog.json`** — `idea-to-prod` → `1.1.0`, `last_verified: 2026-08-04`, `content_files` unchanged. That plus a CHANGELOG entry is the whole registration for a workflow edit. No other workflow is touched by this slice.

## New content proposed

Registration is identical for every methodology below: folder shaped like `context-graph-engineering/` (`AGENTS.md` no frontmatter + `meta.json` + `content/NN-*.xml`) → `python3 scripts/regen-tier-manifest.py` → hand-add `<methodology slug=… tier=… path=…>` to the domain `INDEX.xml` and bump its `count`. Never run `build-domain-index-v2.py`.

**A. `retrieval-cost-per-answer-audit`** · `ai-core` · **solo** · *highest-value item in this slice*. `context-graph-engineering` Skip If says "measure first" — and nothing in 2,623 methodologies performs that measurement. A dangling prerequisite in our own corpus. Produces a **Retrieval Cost Ledger**: ten real queries; per query the index tokens, candidate tokens, delivered-body tokens, correctness; then the two numbers that decide everything — median tokens per lookup and *overhead ratio* (retrieval ÷ delivered body). Ships dated reference rows so a reader can place themselves: flat 879–954 · RAPTOR 3,441–3,510 · GraphRAG-local ~38.7–39.8k · GraphRAG-global ~331–333k (GraphRAG-Bench, arXiv 2506.05690, 2026-06-06, GPT-4o-mini) — and ours, 33k at 10:1, GraphRAG-local cost for plain-tree capability. Solo deliberately: it gates every pro/geek retrieval methodology downstream. Existing slugs checked, none overlap: `ai-core/rag-bench-harness-template` (quality, no token accounting), `ai-core/vector-db-tuning-runbook`, `ml-engineering/rag-eval-retrieval-metrics` (recall/MRR), `embedding-cost-optimization` (embedding spend), `optimize-tune/vector-db-query-optimization-pass` (latency). Ships `scripts/validate-retrieval-cost-per-answer-audit.py --self-test`.

**B. `hierarchical-index-compression`** · `ai-agents` · **pro**. The `warrant: none` exit says "use a hierarchy with compact indexes" and stops. This is that hierarchy. Produces an **Index Budget Record**: fan-out per level, per-entry byte cap, what lives in the index vs the leaf, shard trigger. RAPTOR (115,541 indexing tokens / 135s — 5.7x cheaper than MS-GraphRAG on the same corpus, and better than it across Medical) as the *build* pattern; sharding as the cheap pattern for corpora that already nest. Rule: an index entry restating the leaf's summary is paid twice — entries carry discriminators, not descriptions. Checked: `chunking-document-structure`, `chunking-strategies`, `llamaindex-indexes-queries`, `ai-core/agent-context-engineering-corpus-standard` — all distinct.

**C. `repo-map-for-coding-agents`** · `dev` · **pro**. The one pattern that transfers directly: Aider ranks symbols by personalized PageRank over a tree-sitter tag graph, seeded on files in context and symbols mentioned, packed into ~1k tokens. Produces a **Repo Map Spec**: derived edges only (tags, imports, call sites — R3 free), seed set, ranking function, hard token budget, refresh trigger. Compares SCIP/Sourcegraph, GitHub stack-graphs, Glean, Serena MCP on one axis: precomputed index vs per-session derivation. Checked: `dev/context-window-curation-for-coding-agents` (solo, *manual* ≤6k bundle — C is its automated upstream and must cross-reference it), `ml-engineering/chunking-code-ast` (boundaries, no ranking), `dev/blast-radius-scoring-rubric`.

**D. `agent-memory-admission-policy`** · `ai-agents` · **pro**. R6 governs how a fact expires; nothing governs how it enters. Produces an **Admission Policy**: closed list of admissible fact classes, promotion threshold from turn to durable, scope key (session/user/org), eviction rule — with a mandatory warrant cross-reference before memory is given graph shape at all. Positions Graphiti, mem0 and Letta as three admission policies, not three databases. Checked: `ml-engineering/agents-memory-system` (geek, storage tiers, admission unspecified — cross-reference, do not merge), `langchain-memory`, `filesystem-as-working-memory`.

**E. `retrieval-structure-cost-audit`** · playbook, `optimize-tune` · **solo**. A one-day run executing A against a live retriever, ending in go/no-go: compress, restructure, or leave alone. None of the 23 `optimize-tune` playbooks measures retrieval cost. Registration: folder (`AGENTS.md` + `meta.json` + `content/01-playbook.xml`) → `regen-tier-manifest.py`. `playbooks/taxonomy.xml` carries no counts and `playbooks/by-goal/optimize-tune/` is empty — no edit needed.

**F. `context-graph-engineering/content/04-deferred-construction.xml`** · extension, not a slug. Defines the lazy pattern the decision tree already routes to: index exactly as vector RAG, defer community/summary construction to query time, pay graph cost only on queries that need it. Evidence: LazyGraphRAG (Microsoft, 2024-11-25) indexed at 0.1% of full GraphRAG and queried global at 4%, beating vector RAG, RAPTOR and every GraphRAG mode. Bump `meta.json` to 1.1.0, `est_tokens` 3400 → ~3800; the `INDEX.xml` entry needs no change.

## Our own retrieval — recommendation

**Decision: compress the tree. Do not build the graph this quarter.** Three actions, in order.

1. **Cap the index tier.** L2 totals 866 KB / ~221k tokens. Shard every index above 40 KB (`dev` 122, `infra` 96, `pm` 96, `marketing` 94, `ux` 62, `ml-engineering` 62) by `group` behind a stub index carrying a group table. Target: no index read above 12k, median lookup ≤8k — a 4x cut, no new machinery.
2. **Cut per-entry cost.** Index entries carry a truncated prose summary the leaf repeats. Replace with slug + tier + a ≤90-char discriminator answering "when would I open this"; `meta.json` owns the full summary.
3. **Only then reconsider the 4,973 verified edges across 2,615 methodologies** (density 1.90/node, 266 islands). They pass R1 — cross-domain links are real — and are derivable, so R3 is free. They fail R2 today: no graph can be shown to beat a compressed tree until the tree is compressed and re-measured. The correct v1 is not a graph store but a typed `related` list in each leaf's `meta.json` under a closed vocabulary, with the R7 referential-integrity gate in CI — zero traversal cost, and the 266 islands become reportable.

Do all three before any GraphRAG-shaped work. Re-run A afterwards; the ledger decides step 3.

## Rejected

Slugs for HippoRAG2, KGP, LightRAG, nano-graphrag, HNSW, SCIP-as-such — single tools, high churn, no decision to make; dated rows inside A–C instead. A fifth GraphRAG-vendor slug in `ml-engineering` — deepens the pit R1 warns against. **"Graph engineering" as a term or slug** — "context engineering" is established; this label is months old and means different things to different people, so shipping it dates the corpus. MS-GraphRAG global search as a default. A `code-graph-database` slug — the buyer's question is what goes in the context window, answered by C. Restating the warrant gate outside `context-graph-engineering`; B–D reference it by slug.

## Risks / conflicts with other slices

- `skills/faion/knowledge/ai-agents/INDEX.xml` — two entries (B, D) and `count="103"` → 105; agent/reliability passes append here too. Hand-append, serialize the count bump.
- `skills/faion/knowledge/ai-core/INDEX.xml`, `knowledge/dev/INDEX.xml` — one entry each (A, C). `dev/INDEX.xml` is 122 KB; hand-edit only.
- `skills/tier-manifest.json` — run `scripts/regen-tier-manifest.py` **once after all ten passes**.
- `skills/faion/workflows/catalog.json` — every workflow-editing pass bumps a version here. Serialize.
- `skills/faion/workflows/idea-to-prod/content/30-token-discipline.xml` — orchestration/context passes are the likely other claimants; my edit is one appended section touching no existing rule.
- `context-graph-engineering/{meta.json,content/06-decision-tree.xml}` — F adds `content/04-*.xml` and bumps the version; no other pass may also bump it.
- `knowledge/dev/context-window-curation-for-coding-agents/` — C is its automated upstream; reconcile, do not duplicate.
- `knowledge/ml-engineering/agents-memory-system/` — D owns admission only, not storage; a memory pass may claim the same file.
- Recommendation step 1 rewrites the L2 layer every other pass appends to. **Sequence it after all ten passes land.**
