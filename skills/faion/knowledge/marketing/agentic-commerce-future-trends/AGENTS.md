# Agentic Commerce Future Trends

## Summary

**One-sentence:** Readiness report scoring a business on whether AI agents can discover, evaluate, and transact with it — across trust signals, machine-readable interfaces, cross-platform consistency, and review authority.

**One-paragraph:** AI agents are starting to complete entire purchase flows — comparing options, recommending, transacting — without human search. Traditional SEO optimises for keywords; agentic commerce optimises for authority, machine readability, and cross-platform consistency. This methodology produces a readiness report scoring the business across six dimensions (trust signals, API/machine-readable interfaces, NAP consistency, review authority, structured-data coverage, task-completion content) and recommends a 12-24 month investment roadmap. Output is the report the founder/CEO uses to brief budget.

**Ефективно для:** B2C and B2B businesses preparing for AI-agent discovery; founders briefing board on AI search risk; agencies pitching GEO services.

## Applies If (ALL must hold)

- Auditing readiness for AI-agent-mediated discovery and purchase
- Planning a 12-24 month GEO / SEO strategy with agentic commerce as a vector
- Cross-platform brand consistency (NAP, descriptions, schema) is partially measured
- API-first or machine-readable interface is a near-term option

## Skip If (ANY kills it)

- Pure short-term keyword SEO with no earned-media budget — wrong tool for the cycle
- Very early-stage businesses with no authority signals — fundamentals first
- Hyper-local micro-business with minimal AI search exposure — ROI may not justify
- Bespoke services (enterprise contracts, custom B2B) where AI agents do not handle the buy

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Brand inventory (NAP, descriptions, schema) | YAML / sheet | ops |
| API / data-feed inventory | YAML | engineering |
| Review presence across G2, Trustpilot, Google, niche review sites | CSV | marketing ops |
| Content library tagged by task-completion vs informational | CSV | content ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/growth-marketer` | parent role skill |
| [[ai-overview-monitoring]] | input data on AI-citation presence |

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
| `collect_inventory` | haiku | Mechanical extraction across platforms |
| `score_axis` | sonnet | Bounded judgement per axis |
| `synthesise_roadmap` | opus | Cross-axis investment narrative for executive |

## Templates

| File | Purpose |
|------|---------|
| `templates/agentic-readiness-checklist.md` | Per-axis readiness checklist with scoring guidance |
| `templates/agentic-commerce-future-trends.json` | JSON schema for the readiness report |
| `templates/_smoke-test.md` | Minimum-viable filled report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-commerce-future-trends.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[google-ai-overviews-optimization]]
- [[technical-seo-for-ai]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agentic-commerce-future-trends applies: root question — "Has the business completed ≥30 days of paid + organic across platforms AND is preparing a 12-24 month GEO strategy?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-six-axis-scoring, r2-typed-input, r3-roadmap-budgeted, r4-cross-platform-consistency, r5-versioned-record, r6-task-completion-content.
