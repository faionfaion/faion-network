# Meta Audience Targeting

## Summary

Audience construction for Meta campaigns via the Marketing API: demographic targeting, interest and behavior lookups, custom audiences (website, CRM, engagement, app), lookalike audiences, exclusion logic, and reach estimation. The core rule is: always exclude recent purchasers from prospecting ad sets — failing to do so wastes budget on users who have already converted.

## Why

Meta's auction system allocates impressions based on audience overlap, bid, and relevance. Using the wrong audience type — or forgetting exclusions — inflates CPAs and triggers audience fatigue. Custom audiences built from pixel events or hashed CRM data consistently outperform broad interest targeting for retargeting. Lookalikes built from high-value source audiences (purchasers, not all visitors) produce 2-5x better ROAS than interest-only cold targeting.

## When To Use

- Building or auditing any Meta ad set audience via the Marketing API
- Creating custom audiences from pixel events, customer lists, or engagement sources
- Generating lookalike audiences from a qualified source audience
- Constructing full-funnel audience stacks (cold → warm → hot)
- Estimating reach before launching using the `reachestimate` endpoint
- Setting up Special Ad Category campaigns (housing, credit, employment) with restricted targeting

## When NOT To Use

- Campaign or ad set creation structure — use `ads-meta-campaign-setup` for the full three-tier setup
- Budget allocation across audiences — use `ads-budget-optimization`
- Instagram-specific placement targeting — use `instagram-ads` for placement-level API details
- Audience analysis or reporting post-launch — this covers construction only

## Content

| File | What's inside |
|------|---------------|
| `content/01-demographics.xml` | Geo, age/gender, language, device targeting JSON with API syntax |
| `content/02-interests-behaviors.xml` | Interest search API, behavior targeting, flexible vs layered logic |
| `content/03-custom-audiences.xml` | Website WCA, CRM upload (hashed PII), engagement, app activity audience API calls |
| `content/04-lookalikes.xml` | Lookalike creation, sizing table, multi-country spec, best practices |
| `content/05-exclusions-reach.xml` | Exclusion targeting, connection exclusions, reach estimate endpoint, audience size guidelines |

## Templates

| File | Purpose |
|------|---------|
| `templates/audience-naming.txt` | Naming convention for audiences: type, source, timeframe, size |
