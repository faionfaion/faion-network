# Google AI Overviews Optimization

## Summary

**One-sentence:** Spec for structuring content so Google's AI Overviews extract and cite it: direct answers after every section heading, Article + FAQ schema, and a 30-day content freshness cycle.

**One-paragraph:** AI Overview panels do not cite essay-style posts; they extract direct answers, table data, and FAQ snippets. This methodology specifies the structural requirements: a 1-2 sentence direct answer immediately after each section heading, Article + FAQ schema on every page, FAQ pages mapping query patterns 1:1, a 30-day freshness cycle, and entity consistency across the cluster. Output is the spec the content team and the engineering team implement against.

**Ефективно для:** content marketers preparing pillar pages for AIO; SEO managers running a cluster refresh; agencies pitching AIO services.

## Applies If (ALL must hold)

- Target queries show AI Overview panels but site content is not cited
- Launching content in niches with high AIO presence (Science, Tech, Health, Computers)
- Running a content freshness audit — pages >30 days old losing citations
- Tracking infrastructure for AI Overview impressions in GSC is in place
- Preparing FAQ / Q&A content that maps directly to user queries

## Skip If (ANY kills it)

- YMYL queries requiring months of domain authority — quick optimisations will not move citations
- Domain authority too low for Google's citation algorithm — fix off-page authority first
- Navigational queries (brand names) — AIO rarely appears
- Site penalised or under manual review
- Content purely promotional with no informational substance

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Priority query list with current AIO citation status | YAML / CSV | ai-overview-monitoring |
| Content inventory tagged by topic cluster | YAML | content ops |
| Schema markup audit baseline | JSON-LD samples | engineering |
| GSC freshness query (impressions, clicks per piece per 30-day window) | GSC export | Search Console |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[technical-seo-for-ai]] | technical layer this spec sits on |
| [[ai-overview-content-template]] | section-level realisation of this spec |

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
| `audit_existing_pages` | haiku | Mechanical: structure + schema scan |
| `draft_direct_answers` | sonnet | Bounded synthesis from research notes |
| `write_executive_brief` | opus | Cross-section narrative for content owner |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-audit-prompt.txt` | Prompt template for auditing existing pages |
| `templates/gsc-fetch.sh` | Shell script to pull GSC freshness data |
| `templates/google-ai-overviews-optimization.json` | JSON schema for the AIO spec |
| `templates/_smoke-test.md` | Minimum-viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-ai-overviews-optimization.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[ai-overview-content-template]]
- [[ai-overview-monitoring]]
- [[technical-seo-for-ai]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether google-ai-overviews-optimization applies: root question — "Does the target query show AIO panels AND is the site in scope for revision?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-direct-answer-after-heading, r2-article-faq-schema, r3-30-day-freshness, r4-entity-consistency, r5-author-credentials, r6-tracking-impressions.
