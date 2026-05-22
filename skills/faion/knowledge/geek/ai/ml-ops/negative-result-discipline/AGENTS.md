---
slug: negative-result-discipline
tier: pro
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "8eb9609bb9132af7"
summary: A 3-line negative-result convention for ML / RAG / embedding spike experiments so the same dead-end never gets retried six months later.
tags: [ml, experiments, knowledge-management, post-mortem, negative-results]
---

# Negative Result Discipline for ML Spikes

## Summary

**One-sentence:** Standardize a 3-line `negative-result.md` artifact for every failed ML / RAG / embedding spike so the team has an indexed record of what was tried, why it failed, and the condition under which it might be revisited.

**One-paragraph:** ML spike experiments fail more often than they succeed; the failure is the information. Without a discipline, the same spike (BM25+E5 hybrid retrieval, FlashAttention on the 7B model, RoBERTa fine-tune on a 200-sample dataset) gets re-run 3-12 months later by the same person or a new hire, because there is no easy way to discover the prior outcome. Mechanism: at spike close, the engineer records three lines (hypothesis, outcome, retry-condition) plus a small data footprint, and indexes the artifact in a single `negative-results/` directory queryable by tag. Primary output: one Markdown file per closed spike, plus an updated index, plus tags surfaced in the team's wiki / Slack search.

## Applies If (ALL must hold)

- experiment is a time-boxed spike (1-10 days) with a yes/no decision at the end
- result is "no" or "not yet" or "blocked on cost / data / latency"
- artefact will live in a repo or wiki the rest of the team searches
- experiment cost (engineer time + GPU spend) exceeded a $200 / 1-day threshold

## Skip If (ANY kills it)

- spike succeeded and shipped — write a normal design doc, not a negative result
- ad-hoc 30-minute exploration ("does this notebook even run?") — too small to index, write a one-line note in your scratchpad
- the experiment is confidential / under-NDA and cannot be indexed — handle via private knowledge base, not this convention
- team is solo and has no future hires within 12 months — diminishing returns; record but skip the index ceremony

## Prerequisites

- `negative-results/` directory exists in a repo or wiki the team actually searches
- a tag taxonomy (retrieval, embeddings, fine-tune, agent-framework, etc.) agreed in 1 prior meeting
- spike had a written hypothesis BEFORE work started — without it, the negative-result writeup will be retrofitted and misleading

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/embeddings-evaluation` | Common source of negative results worth recording — embedding-model comparisons |
| `geek/ai/rag-engineer/rag-eval-strategy` | RAG spike results frequently end up as negative-result entries |
| `pro/dev/software-architect/adr-staleness-audit` | Sibling pattern: ADRs for decisions, negative results for non-decisions |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 3-line format, retry-condition required, data footprint capped, tag-vocabulary closed, index-on-close | ~800 |
| `content/02-output-contract.xml` | essential | Negative-result Markdown schema with required frontmatter, forbidden patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: retroactive hypothesis, vague retry-condition, untaggable entries, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_hypothesis_from_pre_spike_doc` | haiku | Mechanical extraction |
| `summarize_outcome_from_spike_notebook` | sonnet | Bounded summary; needs judgment on what counts as the failure mode |
| `propose_retry_condition` | sonnet | Per-experiment judgment on what would change the answer |
| `cross_link_to_prior_results` | sonnet | Search-then-link; bounded |

## Templates

| File | Purpose |
|------|---------|
| `templates/negative-result.md` | 3-line skeleton with frontmatter (tags, owner, date, cost) |
| `templates/index-row.yaml` | one row per result for the `index.yaml` lookup file |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/index-rebuild.py` | Walks `negative-results/`, regenerates index.yaml + a Markdown TOC by tag | On every PR that adds a negative-result file |
| `scripts/check-frontmatter.py` | Validates each negative-result has all required frontmatter fields | Pre-commit hook |

## Related

- parent skill: `geek/ai/ml-ops/SKILL.md`
- peer methodologies: `geek/ai/ml-engineer/embeddings-evaluation`, `pro/dev/software-architect/adr-staleness-audit`
- external: [Stephen J. Mildenhall, "The Failure Museum"] · [Andy Matuschak working notes on negative-result archives] · [DeepMind "Ten Lessons from a Decade of Deep Learning" (Lessons 7 + 8 on dead-end documentation)]
