---
slug: ai-overview-monitoring
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Weekly monitoring report covering AI Overview, Perplexity, and ChatGPT-Search citation presence across a priority query list, with a per-finding action ladder."
content_id: "3946b3f6b9dc3779"
complexity: medium
produces: report
est_tokens: 2900
tags: [aio, monitoring, perplexity, chatgpt-search, marketing, geek]
---

# AI Overview Monitoring

## Summary

**One-sentence:** Weekly monitoring report covering AI Overview, Perplexity, and ChatGPT-Search citation presence across a priority query list, with a per-finding action ladder.

**One-paragraph:** Optimisation without monitoring is theatre. This methodology defines the monitoring stack: a priority + watch query list, three citation sources (AIO, Perplexity, ChatGPT-Search), a weekly cadence, a per-query record (cited / partial / not_cited), and an action ladder that fires when presence drops. Output is a `aio-monitoring/` folder with weekly snapshots, a trend report, and a per-query investigation log that feeds the sibling `ai-overview-content-template` retrofit work.

**Ефективно для:** growth teams running AIO retrofits; SEO managers measuring AI search visibility; agencies reporting AIO progress to clients.

## Applies If (ALL must hold)

- Marketer has 10+ priority queries with measurable AIO / Perplexity presence
- Content cluster has been retrofit per `ai-overview-content-template` for ≥30 days
- Monitoring stack (manual or BrightEdge/sistrix/custom Playwright) is reachable
- Team can act on monitoring findings (rewrite sections, re-publish, update citations)

## Skip If (ANY kills it)

- Priority list <5 queries — overhead exceeds signal
- Niche has zero AIO / Perplexity coverage in geo — monitor coverage, not presence
- Monitoring stack varies >50% week-over-week without content changes — fix the stack first
- Team cannot act on findings — monitor is wasted

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Priority + watch query lists | YAML | aio-monitoring/queries.yaml |
| Citation-source adapters (google-aio-fetch, perplexity-fetch, chatgpt-search-fetch) | Python or shell | tools/ |
| Weekly snapshot storage (Git or DB) | Repo path or DB connection | ops |
| Action ladder doc (which findings trigger what action) | Markdown | growth playbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-overview-content-template]] | retrofit upstream |
| [[ai-overview-risk-scoring]] | scoring upstream — informs which queries to monitor closely |

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
| `scrape-aio-perplexity-chatgpt` | haiku | Mechanical HTTP + parse |
| `classify-citation-status` | sonnet | Bounded judgement: cited / partial / not_cited |
| `trend-narrative` | sonnet | Bounded week-over-week synthesis |
| `action-ladder-decide` | sonnet | Bounded mapping of drop → action |

## Templates

| File | Purpose |
|------|---------|
| `templates/queries.yaml` | Priority + watch query lists |
| `templates/weekly-snapshot.json` | Per-query citation status across the three sources |
| `templates/action-ladder.md` | Documented action mapping for each finding type |
| `templates/_smoke-test.json` | Minimum-viable filled snapshot |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-overview-monitoring.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[ai-overview-content-template]]
- [[ai-overview-risk-scoring]]
- [[google-ai-overviews-optimization]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-overview-monitoring applies: root question — "Is the priority query list ≥10 queries with ≥30 days of retrofit AND the monitoring stack working?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-weekly-cadence, r2-three-sources-required, r3-snapshot-immutability, r4-action-ladder-discipline, r5-human-review, r6-versioned-record.
