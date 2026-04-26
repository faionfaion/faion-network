# Google Shopping Ads

## Summary

Product listing campaigns for e-commerce where ads are generated automatically from a Merchant Center product feed. Feed quality drives 80% of performance — title, image, category, GTIN, and price accuracy matter more than bids. Requires two separate API auth flows: Content API for Shopping (Merchant Center) and Google Ads API. Product partition trees must be MECE (every SKU in exactly one node). Always validate the feed before creating campaigns.

## Why

Shopping campaigns reach shoppers at the point of product comparison with zero headline writing — Google assembles the ad from the feed. The tradeoff is that creative leverage is gone; a bad title or missing GTIN will generate no impressions regardless of bid. Feed management is the primary optimization lever, and a single policy violation can suspend the entire Merchant Center account, taking down PMax and Shopping simultaneously.

## When To Use

- E-commerce with a structured product catalog (SKUs, GTINs, brand, category, images, price)
- Direct-response retail campaigns where shoppers compare products across vendors
- Migrating legacy Smart Shopping campaigns to Standard Shopping or PMax-with-feed
- Scenarios needing per-product bid control (Standard Shopping) — PMax cannot do this
- Multi-country expansion with localized feeds (per-country language, currency, shipping)

## When NOT To Use

- Lead-gen, services, B2B, or info-products — Shopping requires a product feed and physical/digital good
- Catalogs under 50 SKUs — feed maintenance overhead exceeds value
- Items violating Google policies (supplements, weapons, certain apparel) — feed disapprovals stall everything
- Inventory turning over weekly with no ERP-driven feed — stale price/availability triggers Merchant Center suspension

## Content

| File | What's inside |
|------|---------------|
| `content/01-campaign-setup.xml` | Create Shopping campaign, ad group, product partitions via Google Ads API |
| `content/02-feed-management.xml` | Feed quality rules, Merchant Center integration, product performance reporting |
| `content/03-agent-rules.xml` | API gotchas: two-API auth, product ID format, MECE partitions, currency units, GMC suspension cascade |

## Templates

| File | Purpose |
|------|---------|
| `templates/feed-status-audit.py` | Content API helper listing disapproved and warned products by SKU |
