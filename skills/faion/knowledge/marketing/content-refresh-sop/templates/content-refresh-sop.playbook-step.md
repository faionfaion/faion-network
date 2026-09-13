<!-- purpose: content refresh playbook-step skeleton — thresholds and windows, one row per evergreen URL with the three-source dataset, signals, one verdict and its block (nine-step refresh with baseline, consolidate with redirects, kill with 410, leave with reason) -->
<!-- consumes: evergreen inventory with ages, persisted Search Console export, GA4 landing-page report, rank tracker, the three thresholds -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/06-decision-tree.xml -->
<!-- token-budget-impact: ~900 tokens when loaded -->
# Content Refresh SOP — Playbook step for <site_domain>, cycle <cycle_date>

## Thresholds (written before any URL is scored)
- impressions_trend_pct: <impressions_trend_pct> (negative; period-over-period change)
- position_decay_positions: <position_decay_positions> (positive; trailing avg_position minus prior)
- intent_shift_query_mix_pct: <intent_shift_query_mix_pct> (positive; change in query mix or SERP result type)

## Window
- trailing_days / prior_days: <trailing_days> / <trailing_days> (equal length)
- span_months: <total months compared>
- source: persisted_export | search_console_ui (persisted_export required above 16 months)

## Decision branches (one per signal, each with its number)

| signal | when | then |
|---|---|---|
| intent_shift | query mix changed by more than <intent_shift_query_mix_pct> percent or the SERP turned to a different result type | kill |
| impressions_trend | impressions down more than <impressions_trend_pct> percent with no intent shift | refresh |
| top_position_decay | average position worse by more than <position_decay_positions> positions with no intent shift | refresh |
| impressions_trend | all three signals inside thresholds | leave |

## URL rows (evergreen only, url_age_months at least 12; one verdict each)

| url | url_age_months | trailing gsc clicks / impressions / avg_position | prior gsc clicks / impressions / avg_position | trailing ga4 sessions / key_events | prior ga4 sessions / key_events | rank target_query: trailing / prior position | impressions_trend_pct | position_decay_positions | intent_shift (note) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| <https url> | <n> | <n> / <n> / <x.x> | <n> / <n> / <x.x> | <n> / <n> | <n> / <n> | <query>: <n> / <n> | <(trailing - prior) / prior x 100> | <trailing - prior> | <true/false (why)> | refresh / consolidate / kill / leave |

### refresh block (URL unchanged; dateModified only with substantive change)
- url_unchanged: true; substantive_change: <true/false>; date_modified_updated: <true only if substantive>; title_changed_for_intent: <true/false>

| step | name | exit_criterion | done | skipped_reason |
|---|---|---|---|---|
| 1 | re-run query and intent research | <SERP captured on date; intent stated> | true | |
| 2 | update facts, statistics, prices, dates | <n facts replaced with dated sources> | true | |
| 3 | rewrite title, meta description, intro | <rewritten to the current intent> | true | |
| 4 | add sections top-ranking pages cover | <sections added; gap list closed> | true | |
| 5 | refresh screenshots, media, examples | <n assets retaken> | true | |
| 6 | update internal links in and out | <n newer pages link in; dead links replaced> | true | |
| 7 | fix technical issues on the URL | <links, alt text, structured data, CWV> | true | |
| 8 | update dateModified and append changelog | <dateModified; changelog lists edited steps> | true | |
| 9 | request re-indexing and record baseline | <re-index requested; 28-day baseline stored> | true | |

- baseline (28 days from published_at): published_at <YYYY-MM-DD>, clicks <n>, impressions <n>, avg_position <x.x>, sessions <n>, key_events <n>
- reevaluation_at: <published_at + 90 days>

### consolidate block
- survivor_url: <url>; merged_urls: <list>; redirects: <from -> survivor, 301 or 308, one per merged URL>; internal_links_rewritten: true
- baseline and reevaluation_at as for a refresh

### kill block
- http_status: 410 (404 acceptable); removed_from_sitemap: true; removed_from_navigation: true; internal_links_dropped: true; redirect_target: null

### leave block
- reason: <which signals stayed inside thresholds>; next_review_at: <YYYY-MM-DD>
