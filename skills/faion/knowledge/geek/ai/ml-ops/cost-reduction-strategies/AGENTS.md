---
slug: cost-reduction-strategies
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Applies four orthogonal cost levers — response caching, prompt compression, async batching, and model routing — and reports per-lever savings against a baseline.
content_id: "4550c133417111d3"
complexity: deep
produces: report
est_tokens: 4800
tags: [cost-optimization, llm-cost, prompt-caching, model-routing, batching]
---
# LLM Cost Reduction Strategies

## Summary

**One-sentence:** Applies four orthogonal cost levers — response caching, prompt compression, async batching, and model routing — and reports per-lever savings against a baseline.

**One-paragraph:** Production LLM cost is rarely solved by one technique. This methodology audits the request stream, identifies cache-able patterns (SHA-256 prompt+model+temp key), compresses prompts (whitespace + boilerplate removal), batches non-interactive calls, and routes to cheaper models when the simpler model passes a confidence gate. Reports total $ saved per lever vs baseline plus latency / quality delta.

**Ефективно для:**

- Pipelines past $1k/mo where finance asks for a 30%+ reduction.
- RAG systems where 30-50% of queries are near-duplicates.
- Batch enrichment jobs that can tolerate 1-min latency.
- Tiered SaaS where free users should not get opus.

## Applies If (ALL must hold)

- Monthly LLM spend > $500 and growing.
- Request stream is mixed (interactive + batchable).
- Quality metric exists (eval harness or LLM-as-judge).

## Skip If (ANY kills it)

- Spend < $100/mo — engineering time outweighs savings.
- Every call is unique (no cache potential) and SLA blocks batching.
- Single model already cheapest tier — no routing headroom.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Request log | JSONL of {prompt, model, ts, tokens} | Observability stack |
| Quality eval | harness | evaluation-framework methodology |
| Cost baseline | USD/mo | Last 30 days invoice |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit_request_log` | haiku | Cluster by prompt similarity; cheap. |
| `design_cache_layer` | sonnet | Key scheme + TTL + eviction. |
| `design_router` | sonnet | Confidence-gated cascade. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cache-config.yaml` | Redis cache config skeleton |
| `templates/router-policy.yaml` | Confidence-gated routing policy |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-reduction-strategies.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[llm-cost-basics]]
- [[evaluation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Does the request stream contain repeat prompts (cache potential)? Branches route to a rule id from `content/01-core-rules.xml` (cache-key-sha256, compress-whitespace-first, batch-only-non-interactive, ...) so every leaf is traceable to a testable statement.
