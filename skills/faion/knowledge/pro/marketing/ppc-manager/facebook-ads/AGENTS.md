# Facebook Ads API

## Summary

Meta Marketing API v20+ patterns for campaign management (objectives, CBO), ad set creation with targeting and bid strategies, creative upload (image, video, dynamic), and ad assembly. Budget values are in cents (10000 = $100). Always create campaigns with status PAUSED; activate only after review.

## Why

The Meta API has a 4-level hierarchy (Campaign → Ad Set → Creative → Ad) where each level has its own budget/bidding knobs. Misplacing budget at the wrong level or using a mismatched optimization_goal/billing_event combination causes delivery failure or overspend.

## When To Use

- Creating or managing Facebook/Instagram ad campaigns via the Meta Marketing API
- Implementing CBO (Campaign Budget Optimization) or ad set-level budgets
- Building image, video, or dynamic creative programmatically
- Setting up retargeting funnels with audience-based targeting

## When NOT To Use

- Instagram-specific placement optimization — refer to instagram-ads methodology
- Audience research and lookalike creation — use meta-audience-targeting methodology
- Attribution modeling — use ads-attribution-models methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-campaign-management.xml` | Campaign objectives, CBO, status values, update patterns |
| `content/02-ad-set-targeting.xml` | Ad set creation, bid strategies, optimization goals, placement options |
| `content/03-creative-and-ads.xml` | Image/video upload, CTA types, dynamic creative, naming conventions |

## Templates

| File | Purpose |
|------|---------|
| `templates/create-campaign.sh` | cURL command to create a campaign with objective and budget |
| `templates/create-adset.sh` | cURL command to create an ad set with targeting and optimization |
