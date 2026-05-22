---
slug: negative-result-discipline
tier: pro
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Captures every failed ML / RAG / embedding spike in a 3-line negative-result artefact (hypothesis, outcome, retry-condition) indexed by tags so the same dead-end is never re-run blind.
content_id: "ac098dee3c44e40c"
complexity: light
produces: decision-record
est_tokens: 3000
tags: [ml, experiments, knowledge-management, post-mortem, negative-results]
---
# Negative Result Discipline for ML Spikes

## Summary

**One-sentence:** Captures every failed ML / RAG / embedding spike in a 3-line negative-result artefact (hypothesis, outcome, retry-condition) indexed by tags so the same dead-end is never re-run blind.

**One-paragraph:** ML spike experiments fail more often than they succeed; the failure is the information. This methodology forces a 3-line negative-result.md per closed spike: hypothesis (what we tested), outcome (what happened, with numbers), retry-condition (what would have to change to retry). Each file lives under `negative-results/` keyed by tag, is search-indexed in the team's wiki/Slack search, and surfaces during pre-spike planning to prevent re-running known dead ends.

**Ефективно для:**

- ML teams with rotating staff (each new hire reaches for the same spike).
- RAG + embedding work where the search space is huge (BM25+E5 hybrid, FlashAttention 7B, RoBERTa fine-tune).
- Cost-sensitive teams where each spike burns $200+ in engineer-time + GPU.
- Multi-team orgs where one team's dead end is another team's first idea.

## Applies If (ALL must hold)

- Experiment is a time-boxed spike (1-10 days) with a yes/no decision at the end.
- Result is 'no' / 'not yet' / 'blocked on cost / data / latency'.
- Artefact will live in a repo or wiki the team searches.
- Experiment cost (engineer time + GPU) exceeded a $200 / 1-day threshold.

## Skip If (ANY kills it)

- Spike succeeded and shipped — write a design doc, not a negative result.
- 30-minute exploration ('does this notebook even run?') — too small to index.
- Experiment is confidential / NDA and cannot be indexed.
- Team is solo with no future hires within 12 months.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| negative-results/ dir | git repo or wiki | Team conventions |
| Tag taxonomy | list | 1 prior meeting |
| Spike close trigger | process | Team ritual |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `artefact_author` | haiku | Fill the 3-line template. |
| `index_update` | haiku | Add to tag index. |
| `pre-spike-search` | haiku | Search prior negatives before kickoff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/negative-result.md` | 3-line negative-result skeleton |
| `templates/index.md` | Tag-keyed index skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-negative-result-discipline.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[evaluation-framework]]
- [[finetuning-basics]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Did the spike cost more than $200 in engineer-time + GPU? Branches route to a rule id from `content/01-core-rules.xml` (three-lines-mandatory, retry-condition-concrete, tagged-and-indexed, ...) so every leaf is traceable to a testable statement.
