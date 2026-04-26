# Google Display Ads

## Summary

Python patterns for creating DISPLAY_NETWORK campaigns, adding contextual (keyword/placement) and audience targeting to ad groups, building responsive display ads with required asset sets (1-5 headlines, long headline, 1-5 descriptions, 1-15 images), and querying placement-level performance reports.

## Why

Display campaigns require explicit network_settings flags to avoid search spill-over. Responsive display ads have mandatory asset minimums and optional logo slots; submitting without the required fields causes API validation errors that are not obvious from the error message alone.

## When To Use

- Creating banner ad campaigns across Google Display Network
- Adding remarketing audiences or contextual keyword targeting to display ad groups
- Uploading image assets and assembling responsive display ads
- Reporting on which placements are driving impressions and conversions

## When NOT To Use

- Search text ads — use google-search-ads methodology
- Performance Max campaigns — use google-pmax methodology
- Shopping product listing ads — use google-shopping-ads methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-campaign-setup.xml` | Display campaign creation with network_settings, targeting types overview |
| `content/02-targeting.xml` | Keyword, placement, and audience targeting code patterns |
| `content/03-responsive-ads.xml` | Responsive display ad creation, image upload, asset requirements |

## Templates

| File | Purpose |
|------|---------|
| `templates/responsive-display-assets.py` | Asset dict structure for responsive display ad creation |
