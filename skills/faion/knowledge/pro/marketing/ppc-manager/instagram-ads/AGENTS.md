# Instagram Ads

## Summary

Instagram advertising via the Meta Marketing API: placements (Feed, Stories, Explore, Reels, Search), creative specifications, ad set targeting, shopping creatives, and placement-level reporting. The core rule is: match creative format and ratio to each placement — wrong aspect ratios cause rejection or cropped visuals that kill performance.

## Why

Instagram has five distinct placement surfaces, each with different aspect ratios, safe zones, and audience behaviors. A single ad set can serve all five, but only if creative dimensions match each placement's spec. Mismatched creative triggers automatic rejection or cropping; placement-level reporting (using `breakdowns=platform_position`) is the only way to allocate budget correctly across stream, story, explore, and reels.

## When To Use

- Creating or auditing Instagram ad sets via the Meta Marketing API
- Uploading creative assets and need spec validation before submission
- Running Instagram-only vs. cross-platform (Facebook + Instagram) campaigns
- Setting up Instagram Shopping or Collection ads with product catalogs
- Reporting on placement-level performance with `publisher_platform` + `platform_position` breakdown

## When NOT To Use

- Facebook-only campaigns — use `ads-meta-campaign-setup` for full campaign structure
- Audience construction — use `meta-audience-targeting` for custom/lookalike audience setup
- Cross-platform budget allocation decisions — use `ads-budget-optimization`
- Creative strategy ideation (not API configuration) — this covers specs and API calls, not copywriting

## Content

| File | What's inside |
|------|---------------|
| `content/01-placements.xml` | Placement positions, format specs, and safe-zone rules per placement |
| `content/02-ad-set-api.xml` | Ad set creation API calls, Instagram-only vs multi-platform targeting JSON |
| `content/03-shopping.xml` | Shopping creative API calls, Collection ads, product catalog linkage |
| `content/04-performance.xml` | Bid strategies, budget allocation by placement, reporting API with breakdowns |

## Templates

| File | Purpose |
|------|---------|
| `templates/adset-instagram.json` | Ad set targeting JSON for Instagram-only placement |
| `templates/adset-multi-platform.json` | Ad set targeting JSON for Instagram + Facebook |
