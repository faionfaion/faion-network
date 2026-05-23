---
slug: decision-analysis
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 6-step decision-matrix process — define decision, options, weighted criteria locked pre-scoring, evidence-per-cell scores, sensitivity Monte Carlo, signed rationale.
content_id: "540833b2f15e6888"
complexity: deep
produces: decision-record
est_tokens: 4400
tags: [decision-making, option-evaluation, sensitivity-analysis, monte-carlo, decision-matrix]
---
# Decision Analysis

## Summary

**One-sentence:** 6-step decision-matrix process — define decision, options, weighted criteria locked pre-scoring, evidence-per-cell scores, sensitivity Monte Carlo, signed rationale.

**One-paragraph:** Structured option evaluation: define the decision and its reversal cost, enumerate options (with explicit "do nothing"), define and FREEZE weighted criteria before scoring, score each option×criterion cell with evidence URL, run ±20% weight Monte Carlo to surface ranking instability, and capture rationale in a signed decision-record. Output is a `decision-record` artefact that survives audit and prevents post-hoc rationalization.

**Ефективно для:**

- Strategic option choice ≥$10k or irreversible (architecture, vendor, hiring).
- Multi-criterion trade-offs де gut feel divergent across stakeholders.
- Post-incident decision audit ("why did we choose X?").
- Compliance / governance requiring documented rationale.

## Applies If (ALL must hold)

- Decision has ≥2 viable options + "do nothing" baseline.
- Decision is non-trivial (stakes ≥$10k, reversal cost meaningful, or strategic).
- Criteria can be enumerated and weighted (5-9 dimensions typical).
- Evidence (data, citations, benchmarks) is reachable per cell.

## Skip If (ANY kills it)

- Single-criterion decision (price-only, deadline-only).
- Reversible low-stakes choice (under $1k, undo cost ≈ 0).
- Time-critical incident response — pick fast, document later.
- Decisions where stakeholders refuse to commit weights — full rubric becomes theater.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision brief | 1-page Markdown | sponsor |
| Option catalogue | list with descriptions + costs | proposers |
| Criteria + draft weights | spreadsheet / YAML | BA + sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-acceptance-criteria-generator-reviewer]] | Sibling rubric pattern this methodology shares discipline with |
| [[ba-planning]] | Upstream BA governance that scopes who weighs in on the decision |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: weights locked pre-scoring, evidence per cell, "do nothing" included, sensitivity ±20%, signoff | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: weight reverse-engineering, missing "do nothing", anchor drift, single-rater high-stakes | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 750 |
| `content/05-examples.xml` | essential | Worked example: vendor selection across 3 options × 6 criteria | 700 |
| `content/06-decision-tree.xml` | essential | Routing on weight lock + evidence + Monte Carlo | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `criteria_definition` | sonnet | Light judgment on dimension naming + anchors. |
| `evidence_extraction` | haiku | Mechanical retrieval of evidence URLs per cell. |
| `sensitivity_analysis` | opus | Monte Carlo + rank-flip detection requires careful reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Markdown skeleton (decision, options, criteria, scores, sensitivity, signoff) |
| `templates/_smoke-test.json` | Minimum viable decision-record JSON |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-analysis.py` | Validate decision-record against output-contract + sensitivity threshold | Pre-commit; before stakeholder sign-off |

## Related

- [[ai-acceptance-criteria-generator-reviewer]]
- [[ba-planning]]
- [[business-process-analysis]]
- [[interface-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (weight lock timestamp, evidence completeness, sensitivity rank-flips) to the active rule. Use when in doubt whether the record is ready for sign-off.
