# Zero-Click Search Adaptation

## Summary

**One-sentence:** Produces a per-page AI Overview citation spec (target query, JSON-LD blocks, lede rewrite, KPI set) that swaps the success metric from sessions to citation rate.

**Ефективно для:** Solo SEO operators whose GSC shows impressions stable but clicks down >20% over 90 days on top-50 queries — almost always AI Overview suppression.

**One-paragraph:** AI Overviews and featured snippets have structurally reduced organic CTR — average site CTR drops ~34.5% when AI Overviews appear, and 83% of AIO-served searches end without a click. This methodology produces a per-page citation spec: target query, top-10 evidence, Article+FAQPage JSON-LD, a 40-60 word direct-answer lede, original data points with dates, and a redefined KPI set (impressions, branded queries, AI citation rate). It rejects pure session-as-success thinking and refuses to ship without verifiable JSON-LD + a named accountable owner.

## Applies If (ALL must hold)

- GSC shows impressions stable or growing while clicks drop >20% over 90 days for top-50 queries.
- Top-10 SERP for the target query contains an AI Overview or featured snippet box.
- Site has Article-shape content (blog post, guide, doc) for the target query.
- An accountable owner can be named for the page (handle / email).

## Skip If (ANY kills it)

- Brand new site with no technical SEO foundation — fix crawlability and content first.
- Local SEO (maps/places) where zero-click dynamics differ structurally.
- Niche where AI Overviews do not appear AND traffic volume is still growing.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| GSC last-90d query CSV export | csv | Google Search Console → Performance → Export |
| Top-10 SERP snapshot for target query | screenshot or HTML | incognito browser or SERP API |
| Original data points with dates | list of {stat, value, year, source} | internal research bank |
| Named accountable owner for the page | handle / email | team roster |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/seo-manager/google-ai-overviews-optimization` | Paired methodology — schema and AIO mechanics. |
| `solo/marketing/seo-manager/topical-authority` | Topic-cluster map identifying citation-worthy gaps. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `classify_aio_suppression` | haiku | Structured filter over GSC CSV — bounded rule set. |
| `draft_lede_and_faq` | sonnet | Per-page rewrite requiring topical judgment. |
| `review_citation_strategy` | opus | Cross-page synthesis when stakes are high (cohort > 20 pages). |

## Templates

| File | Purpose |
|---|---|
| `templates/zero-click-search-adaptation.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/zero-click-search-adaptation.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-zero-click-search-adaptation.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[google-ai-overviews-optimization]] — paired schema + AIO methodology.
- [[topical-authority]] — feeds the citation gap map.
- [[serp-intent-classification-rubric]] — upstream classifier.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
