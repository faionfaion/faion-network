---
slug: social-proof-harvest
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "6d3b3e486aa876bc"
summary: Proactive pipeline that scrapes tweets, DMs, and comments mentioning the product, asks for permission, and routes approved quotes onto a testimonial wall — without manual hunting.
---
# Social Proof Harvest

## Summary

**One-sentence:** A repeatable pipeline that turns spontaneous tweets, DMs, and comments mentioning your product into permissioned testimonials on a wall page — without the founder doing manual screenshotting.

**One-paragraph:** Existing methodologies like `growth-customer-testimonials` cover the ASK pattern (DM the customer, get the quote). They do not cover the HARVEST pattern: detect when someone mentions you in public, capture the quote with author identity, run a permission flow, and publish to the wall. Solo founders leak 80% of organic social proof because the moments fly past. This methodology defines the four-stage loop: detect → capture → consent → publish, plus the storage schema that lets you re-use a single quote across the site, landing page, and outbound. Anchored to "Audience-to-customer conversion sprint" for the indie hacker.

## Applies If (ALL must hold)

- The product has at least one public mention channel (Twitter/X, LinkedIn, Reddit, Hacker News, Discord, Product Hunt) and ≥1 mention per week organically.
- You own the website / landing pages where the wall will live.
- You can run a lightweight detection workflow (search alerts, Brand24, or a Make/n8n scrape).
- You can store the source-of-truth quote DB (Notion, Airtable, or a flat JSON in the repo).

## Skip If (ANY kills it)

- Zero organic mentions yet — fix distribution first, this harvests existing signal.
- Pre-launch with no public product — there is nothing to mention.
- Product handles sensitive data where surfacing customer names creates risk (health, finance, dating without consent infrastructure) — needs a harder review.

## Prerequisites

- A consent template (one paragraph + one-click reply) in the founder's email / DM canned-responses.
- A quote DB with fields specified in the core rules.
- A wall page or section on the site to publish approved quotes.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context |
| `solo/marketing/testimonial-capture-microsurvey/` if present | Sibling ASK-pattern methodology — harvest fills the inbound side. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every harvest cycle enforces | ~900 |

## Related

- parent skill: `solo/marketing/`
- triggering activity: `p2-indie-hacker/Audience-to-customer conversion sprint`
- adjacent: `solo/marketing/growth-customer-testimonials` (ASK pattern, distinct from this HARVEST pattern)
