---
slug: ai-overview-risk-scoring
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "aab1d9ae7ccd14b0"
summary: A scoring approach that classifies each priority query as skip / target / hedge based on zero-click risk from AIO, so the marketer redirects wasted effort to AIO-citation hunting on queries that pay.
tags: [aio, risk-scoring, zero-click, seo, growth, geek]
---
# AI Overview Risk Scoring

## Summary

**One-sentence:** A scoring approach that classifies each priority query as `skip` / `target` / `hedge` based on AIO zero-click risk, so the marketer reallocates content effort away from queries where Google's panel will eat every click.

**One-paragraph:** `google-ai-overviews-optimization` covers AIO as opportunity; this methodology covers it as risk. Some queries are now zero-click — AIO answers them inline, the user never visits a site. Writing for those queries is wasted unless the goal is AIO citation itself. The methodology scores every query on six axes (intent_class, panel_persistence, snippet_length, monetisation_potential, our_citation_eligibility, alternative_value), produces a single risk index, and recommends one of three actions: `skip` (don't write), `target` (write only for citation hunting), or `hedge` (write but invest in middle-funnel CTAs that AIO won't intercept). Output: a per-query decision row that feeds into the topic-cluster plan. Closes the rationality gap between "optimise for AIO" and "we wrote three pillar posts that send zero traffic."

## Applies If (ALL must hold)

- Marketer has &gt;= 30 priority + candidate queries to evaluate.
- AIO presence data exists for the queries (from sibling tracker).
- A topic-cluster planning cadence exists where decisions land.
- The team has the capacity to deprioritize queries — political latitude is required.

## Skip If (ANY kills it)

- Priority list &lt; 10 queries — scoring overhead exceeds the signal.
- Niche has no AIO coverage — risk score collapses to 0 for everything; not useful.
- Team is contractually obligated to write on all queries (client commitment) — note risk but cannot act.
- Strategy is pure brand / persona content — AIO risk is orthogonal.

## Prerequisites

- AIO presence data per query from `ai-overview-presence-tracker` or `ai-overview-monitoring`.
- Query-intent classification (informational / commercial-informational / transactional).
- Estimated monetisation per click per query (from analytics or revenue model).
- A documented topic-cluster plan to feed decisions into.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/growth-marketer/ai-overview-monitoring` | Source of presence + position data; primary input. |
| `geek/marketing/growth-marketer/ai-overview-content-template` | What `target` queries get retrofit with. |
| `pro/marketing/growth-marketer/ai-overview-presence-tracker` | Operational tracker for presence data. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: six-axis scoring, decision-mapping, periodic re-score, monetisation-grounded, document-the-decision | ~1100 |
| `content/02-output-contract.xml` | essential | Decision-row schema, action-mapping rule, re-score cadence | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: optimism bias, panel-position confusion, sunk-cost retention | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-single-query` | sonnet | Bounded judgement across six axes |
| `decision-map` | haiku | Mechanical: index → action |
| `cluster-rollup-narrative` | opus | Cross-query synthesis for the topic-cluster owner |

## Templates

| File | Purpose |
|------|---------|
| `templates/scoring-rubric.json` | Six-axis scoring definition + thresholds |
| `templates/decision-row.json` | Per-query decision row schema |
| `templates/quarterly-review.md` | Markdown template for the quarterly re-score review |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score.py` | Run scoring on the query list; emit decision rows | Quarterly + on tracker drift |
| `scripts/rollup.py` | Cluster-level aggregation; emit narrative | Quarterly |

## Related

- parent skill: `geek/marketing/growth-marketer/`
- peer methodologies: `ai-overview-monitoring`, `ai-overview-content-template`, `ai-overview-presence-tracker`, `google-ai-overviews-optimization`
- external: [Rand Fishkin zero-click study](https://sparktoro.com/blog/zero-click-search-study/) · [Sparktoro AIO data 2025](https://sparktoro.com/) · [Ahrefs AIO impact](https://ahrefs.com/blog/)
