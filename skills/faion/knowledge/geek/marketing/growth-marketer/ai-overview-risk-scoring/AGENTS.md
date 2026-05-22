---
slug: ai-overview-risk-scoring
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Decision record classifying each priority query as skip / target / hedge based on AIO zero-click risk across six scoring axes, so content effort reallocates away from queries that no longer pay."
content_id: "aab1d9ae7ccd14b0"
complexity: medium
produces: decision-record
est_tokens: 2900
tags: [aio, risk-scoring, zero-click, seo, marketing, geek]
---

# AI Overview Risk Scoring

## Summary

**One-sentence:** Decision record classifying each priority query as skip / target / hedge based on AIO zero-click risk across six scoring axes, so content effort reallocates away from queries that no longer pay.

**One-paragraph:** Some queries are now zero-click: AIO answers them inline, the user never visits a site. Writing for them is wasted unless the goal is AIO citation itself. This methodology scores each query on six axes (intent_class, panel_persistence, snippet_length, monetisation_potential, our_citation_eligibility, alternative_value), produces a single risk index, and recommends one of three actions: skip (do not write), target (write for citation hunting), hedge (write but invest in middle-funnel CTAs). Output: per-query decision rows that feed the topic-cluster plan.

**Ефективно для:** growth marketers deciding where to invest content; founders deprioritising losing queries; agencies preparing topic-cluster proposals.

## Applies If (ALL must hold)

- Marketer has ≥30 priority + candidate queries to evaluate
- AIO presence data exists for the queries (from sibling tracker)
- Topic-cluster planning cadence exists where decisions land
- Team has political capacity to deprioritise queries

## Skip If (ANY kills it)

- Priority list <10 queries — scoring overhead exceeds signal
- Niche has no AIO coverage — risk score collapses to 0, not useful
- Team contractually obligated to write on all queries — cannot act on score
- Strategy is pure brand / persona content — risk is orthogonal

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AIO presence data per query | YAML / CSV | ai-overview-monitoring tracker |
| Query-intent classification (informational / commercial-informational / transactional) | CSV | keyword ops |
| Monetisation per click per query | CSV | analytics / revenue model |
| Topic-cluster plan | YAML | content strategy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-overview-monitoring]] | source of presence + position data |
| [[ai-overview-content-template]] | what 'target' queries get retrofit with |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-single-query` | sonnet | Bounded judgement across six axes |
| `decision-map` | haiku | Mechanical: index → action |
| `cluster-rollup-narrative` | opus | Cross-query synthesis for topic-cluster owner |

## Templates

| File | Purpose |
|------|---------|
| `templates/scoring-rubric.json` | Six-axis scoring definition + thresholds |
| `templates/decision-row.json` | Per-query decision row schema |
| `templates/quarterly-review.md` | Markdown template for the quarterly re-score review |
| `templates/_smoke-test.json` | Minimum-viable filled decision row |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-overview-risk-scoring.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[ai-overview-monitoring]]
- [[ai-overview-content-template]]
- [[google-ai-overviews-optimization]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-overview-risk-scoring applies: root question — "Is the candidate list ≥30 queries AND AIO presence data exists?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-six-axis-scoring, r2-decision-mapping, r3-periodic-rescore, r4-monetisation-grounded, r5-document-the-decision, r6-versioned-record.
