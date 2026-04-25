# Agent Integration — Google Ads Keyword Strategy

## When to use
- Building a new search campaign from scratch — seed → expand → cluster → match-type → negatives.
- Weekly Search Terms Report mining: extract negatives, promote winners to exact, find new themes.
- Migrating broad-only spend to a phrase + exact + tight-negatives structure.
- Reorganizing an over-grown account where one ad group has 100+ keywords across mixed intents.
- Cross-platform keyword harvest — pulling SEO data and converting to paid keyword plans.

## When NOT to use
- Performance Max — pmax doesn't expose keywords; use audience signals + asset groups instead.
- Smart campaigns — Google picks keywords for you, your input is themes.
- Display / YouTube — keywords on display are hint-only; topics + audiences dominate.
- Brand-only campaigns — already converged to a tight list, agent loops add noise.

## Where it fails / limitations
- Match types post-2021 are fuzzier: phrase ≈ old broad-modifier, exact matches "close variants" — agents over-trusting strict containment will over-prune.
- Search Terms Report only shows queries with material impressions; long-tail negatives are invisible until they spend money.
- Keyword Planner volume is quantized into buckets ("100-1K") — agents that compute precise CPC × volume math get garbage estimates.
- Google enforces 4000-character limit per keyword and 5000 keywords per ad group; bulk-uploads from agents need pre-validation.
- The same query can match multiple keywords across ad groups; "winner promotion" without account-wide dedupe creates internal competition.

## Agentic workflow
Two loops: **build** (one-shot per ad group) and **harvest** (weekly). Build: agent takes seed keywords + landing page + competitor scrape, expands via Keyword Planner API + autocomplete, clusters by intent (BERT embeddings or simple n-gram), assigns match types, drafts negative list. Harvest: agent pulls Search Terms via GAQL, classifies each query (relevant/negative/new theme), produces a diff (add as exact, add as negative, leave). Always require human approval before pushing > 50 changes per push to prevent runaway pruning.

### Recommended subagents
- `faion-ads-agent` — runs Google Ads API mutations (add keywords, add negatives, change match type).
- `faion-seo-manager` (knowledge tier) — supplies organic keyword data + SERP intent classification.
- `faion-improver` — owns the weekly Search Terms harvest loop.

### Prompt pattern
```
Build a keyword plan for landing page {url} on theme "{theme}". Output:
12-20 phrase-match keywords (high commercial intent), 5-10 exact-match
(top performers / brand+modifier), 30+ negatives split into Unqualified /
Wrong-Intent / Wrong-Audience / Wrong-Product. Group by single intent —
no informational mixed with transactional.
```

```
Process Search Terms for last 14 days from campaign {id}. For each query
with > 5 clicks: classify (KEEP_AS_EXACT / ADD_NEGATIVE_PHRASE /
ADD_NEGATIVE_EXACT / NEW_THEME / IGNORE). Output as CSV with proposed
action. Don't apply — return for review.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` SDK | Keyword + negative mutations, GAQL Search Terms | `pip install google-ads` |
| Google Keyword Planner | Volume + competition data (UI + API via `KeywordPlanIdeaService`) | https://ads.google.com/home/tools/keyword-planner/ |
| `gaarf` | Templated Search Terms → CSV/BigQuery | `pip install google-ads-api-report-fetcher` |
| Google Ads Editor | Bulk paste keywords across ad groups | https://ads.google.com/home/tools/ads-editor |
| Ahrefs / SEMrush APIs | Competitor keyword lists | SaaS |
| `keywordtool.io` API | Autocomplete-based expansion | SaaS |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads API | SaaS API | Yes | `KeywordPlanService`, `AdGroupCriterionService` |
| SpyFu | SaaS | Yes | Competitor keywords + their ad copy via API |
| SEMrush API | SaaS | Yes | Domain → keywords, expensive but rich |
| Ahrefs API | SaaS | Yes | Best SERP intent data |
| Optmyzr Keyword Lasso | SaaS | Partial | UI-driven Search Terms classifier |
| Adalysis | SaaS | Limited | Audit suggestions, manual export |

## Templates & scripts
See `templates.md` for keyword-plan + negatives-list structure. Inline Search Terms harvester — the weekly heart-of-the-loop:

```python
def harvest_search_terms(client, customer_id, days=7, min_clicks=3):
    """Pull queries that spent money but aren't yet keywords or negatives."""
    ga = client.get_service("GoogleAdsService")
    q = f"""
        SELECT search_term_view.search_term, search_term_view.status,
               campaign.name, ad_group.name,
               metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_{days}_DAYS
          AND metrics.clicks >= {min_clicks}
    """
    rows = []
    for r in ga.search(customer_id=customer_id, query=q):
        rows.append({
            "query": r.search_term_view.search_term,
            "campaign": r.campaign.name,
            "ad_group": r.ad_group.name,
            "clicks": r.metrics.clicks,
            "cost": r.metrics.cost_micros / 1_000_000,
            "conv": r.metrics.conversions,
            "status": r.search_term_view.status.name,  # NONE | ADDED | EXCLUDED
        })
    # Hand to LLM classifier or rule engine
    return rows
```

## Best practices
- Start everything in phrase match. Promote queries with proven CTR + conversions to exact. Use broad only with a tight, well-maintained negative list — and only after 30 days of phrase-data.
- Cap ad groups at 10-20 keywords with a single intent. If your agent generates 50, it's clustering wrong.
- Build a shared negative list ("Always Negatives": jobs, careers, free, salary, tutorial, DIY, reddit, wiki) and apply across all search campaigns.
- Run the Search Terms harvest weekly. Anything that spent > 1× target CPA without conversion → negative immediately.
- Keep one campaign per language and one per major geo. Cross-language keyword pollution is the #1 cause of low Quality Score.
- Match keyword theme to landing page; mismatch is the #2 cause of low Quality Score.

## AI-agent gotchas
- LLMs invent keywords that don't exist in the wild ("ai-driven enterprise solution platform") — always validate against Keyword Planner volume before publishing.
- Agents pruning via "exact-string" matching miss close-variants — Google matches "running shoes" to "shoes for running" by default. Use the API's `query_match_type_with_variant` flag.
- Don't let an agent push > N changes per run without approval; one runaway loop can dump 5000 negatives and gut the campaign.
- An agent adding queries as exact keywords without checking for duplicates across ad groups creates internal competition; dedupe account-wide first.
- Human-in-loop checkpoint: any negative-keyword push, any match-type change on a top-spend keyword, any new ad group with > 20 keywords.
- Watch for `INVALID_KEYWORD_TEXT` errors on long-tail with punctuation — strip everything except letters/digits/spaces before submit.

## References
- https://developers.google.com/google-ads/api/docs/keyword-planning/overview
- https://support.google.com/google-ads/answer/7478529 (match types)
- https://support.google.com/google-ads/answer/2453972 (negative keywords)
- https://support.google.com/google-ads/answer/140351 (Quality Score)
- https://developers.google.com/google-ads/api/fields/v17/search_term_view
