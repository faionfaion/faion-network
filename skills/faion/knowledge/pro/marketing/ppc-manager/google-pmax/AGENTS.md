# Google Performance Max

## Summary

Performance Max (PMax) campaigns run Google's AI across all inventory (Search, Display, YouTube, Gmail, Discover, Maps) from a single campaign. They require at minimum 30 conversions/month, a rich asset library (5+ headlines, 5+ long headlines, 4+ descriptions, 4+ images), and strong audience signals from a converting customer-match list. Always start with PAUSED status, disable URL expansion for lead-gen, and keep budget at minimum 3x target CPA daily.

## Why

PMax consolidates channel arbitrage under Google's optimizer, making it efficient for e-commerce and lead-gen advertisers with enough conversion volume. It replaces Smart Shopping campaigns (deprecated 2022) and can reach inventory not covered by Search alone. The risk is opacity: PMax hides placement- and query-level data, cannibalizes branded Search, and requires 4-6 weeks learning phase that resets on pause/restart.

## When To Use

- E-commerce or lead-gen with solid conversion tracking (30+ conversions/month) wanting cross-channel reach
- Migrating legacy Smart Shopping campaigns (Google deprecated Smart Shopping to PMax in 2022)
- Established brands with rich asset libraries (5+ images, 5+ videos, multiple text variants) and audience signals
- Accounts seeking to consolidate spend and let Google's AI handle channel arbitrage

## When NOT To Use

- New accounts with fewer than 30 conversions in last 30 days — PMax cannot exit learning phase
- Brands needing channel-level transparency — PMax hides which placements and queries received spend
- Pure brand-defense Search campaigns — PMax cannibalizes branded Search and inflates CPA
- Niche B2B with narrow ICP — PMax goes broad by default, breaking targeting precision
- Compliance-heavy verticals (housing, employment, credit) — Google restricts PMax automation

## Content

| File | What's inside |
|------|---------------|
| `content/01-campaign-asset-groups.xml` | Campaign creation, asset group setup, asset type requirements and char limits |
| `content/02-audience-signals-bidding.xml` | Audience signals API, bidding strategy progression, budget rules, learning phase |
| `content/03-agent-rules.xml` | API gotchas: asset enums, customer_id format, final_urls HTTPS, account-level conversion goals |

## Templates

| File | Purpose |
|------|---------|
| `templates/asset-audit.py` | Pull asset performance labels (BEST/GOOD/LOW/PENDING) and group by type |
| `templates/asset-spec.md` | Asset group creation checklist with minimum counts per field type |
