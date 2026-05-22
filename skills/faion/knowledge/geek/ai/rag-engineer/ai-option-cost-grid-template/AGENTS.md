---
slug: ai-option-cost-grid-template
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Builds an apples-to-apples cost+quality grid across AI option families (prompt-eng, RAG, SFT, DPO, vendor swap) so a decision memo cites a defensible comparison instead of vendor claims.
content_id: "a94aaeead99dfc9a"
complexity: medium
produces: spec
est_tokens: 3200
tags: [ai, template, decision-memo, cost-grid, vendor-comparison]
---
# AI Option Cost Grid Template

## Summary

**One-sentence:** Builds an apples-to-apples cost+quality grid across AI option families (prompt-eng, RAG, SFT, DPO, vendor swap) so a decision memo cites a defensible comparison instead of vendor claims.

**One-paragraph:** A fixed-shape grid where each row is an option (e.g. "GPT-4o + prompt-eng", "Llama-3-70B SFT on 5k labelled", "OpenAI Embeddings + RAG"), and columns are normalised metrics: dev_cost_usd, infra_cost_usd_per_1k_calls, latency_p95_ms, quality_score_on_eval_set, vendor_lock_risk, ttv_weeks, maintenance_load. Every cell either filled, marked N/A with reason, or absent — no `TBD` ships. Each instance carries `template_version` + `eval_set_hash`. Bundles a worked example so reviewers see one filled grid as the spec.

**Ефективно для:** Solopreneur founder picking between prompt-eng vs RAG vs SFT before signing a vendor contract — closes the gap between vendor pitch decks and a normalised comparison with named owner + named eval set.

## Applies If (ALL must hold)

- Multiple AI options are on the table (≥2) for the same business need.
- A named eval set exists (or can be built within the decision window) to compare quality.
- The decision will be signed off by a named human (founder / CTO / lead engineer).
- The grid will be re-used: tracked under version control, refreshed as vendor pricing changes.

## Skip If (ANY kills it)

- One-shot prototype, no follow-up — write a 1-pager, not a versioned grid.
- No eval set possible (e.g. brand-new domain) — pick the option with lowest lock-in, defer the grid.
- Regulated procurement requires a specific procurement template — use that template's fields.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval set | jsonl with {input, expected, score_fn} | hand-built or auto-derived |
| Vendor pricing (per provider) | table | vendor docs |
| Internal dev cost rates | hourly USD | finance |
| Named decision owner | role + person | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/rag-architecture` | Defines what "RAG" means as a row in the grid. |
| `geek/ai/ml-engineering/eval-set-design` | Defines what makes a defensible eval set. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: no TBDs, named consumer, template_version, worked example | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the grid: rows, columns, eval_set_hash, decision metadata | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Decides whether the grid applies vs a 1-pager | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `populate-rows` | haiku | Mechanical fill from vendor docs. |
| `quality-score` | sonnet | Run eval set; multi-criteria judgement. |
| `recommendation-narrative` | opus | Strategic memo body, multi-stakeholder voice. |

## Templates

| File | Purpose |
|------|---------|
| `templates/grid.md` | Markdown grid skeleton with every column header + N/A discipline. |
| `templates/output-schema.json` | JSON Schema for the structured grid. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-option-cost-grid-template.py` | Verify no TBDs, all required columns present, template_version stamped, worked example reachable. | Pre-commit + pre-sign-off. |

## Related

- [[rag-architecture]] · [[embedding-cost-optimization]] · [[ml-engineering/eval-set-design]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether to ship the full grid (≥2 options + eval set + named owner) or a lightweight 1-pager. Use it as the gate before any vendor contract conversation.
