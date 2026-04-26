# Google Search Ads

## Summary

Python patterns for creating SEARCH campaigns with budget, building ad groups with CPC bids, managing keywords with BROAD/PHRASE/EXACT match types, adding campaign-level negative keywords, running keyword planner queries, retrieving quality scores, and pulling search terms reports.

## Why

Search campaigns require explicit network_settings to stay on Google Search only (not content/partner network). Keyword match types control traffic volume and intent; using BROAD without negatives wastes budget on irrelevant queries. Quality Score (1-10) directly affects ad rank and CPC — low scores require landing page or ad relevance fixes.

## When To Use

- Creating text ad campaigns on Google Search results
- Adding, modifying, or negating keywords in an existing ad group
- Diagnosing low Quality Score (below 6) by component (expected CTR, ad relevance, landing page)
- Mining the search terms report for new keywords or negatives

## When NOT To Use

- Display banner ads — use google-display-ads methodology
- Automated cross-channel campaigns — use google-pmax methodology
- Shopping product ads — use google-shopping-ads methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-campaign-and-adgroups.xml` | Search campaign creation, ad group setup, bid management |
| `content/02-keywords.xml` | Match types, keyword CRUD, negative keywords, keyword planner, quality score |

## Templates

| File | Purpose |
|------|---------|
| `templates/keyword-list.py` | Keyword dict format expected by add_keywords() |
