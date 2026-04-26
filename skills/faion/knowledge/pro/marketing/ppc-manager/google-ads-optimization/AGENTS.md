# Google Ads Optimization

## Summary

Google Ads API patterns for bidding strategy management, conversion action setup, offline conversion upload, and GA4 integration: create portfolio bidding strategies (Target CPA, Target ROAS), apply them to campaigns, set device bid adjustments, define conversion actions with counting and attribution, upload offline conversions via gclid, and query imported GA4 conversion data. The core rule is: let automated bidding accumulate at least 30 conversions per campaign before switching from Maximize Conversions to Target CPA — insufficient conversion data causes erratic bidding.

## Why

Smart bidding (Target CPA, Target ROAS) outperforms manual CPC once enough conversion signal exists, but the algorithm fails without data. Conversion actions must be correctly typed, counted, and attributed before enabling smart bidding — otherwise the algorithm optimizes for the wrong signal. Offline conversion upload via gclid closes the loop between ad clicks and CRM-recorded revenue, enabling true ROAS measurement for high-consideration purchases.

## When To Use

- Configuring bidding strategies for existing Google Ads campaigns via Python client
- Creating or updating conversion actions (WEBSITE, APP, UPLOAD types)
- Uploading offline conversions from CRM data matched by gclid
- Querying per-campaign conversion volume and value split by conversion action
- Setting device-level bid adjustments on campaigns

## When NOT To Use

- Initial campaign/ad group/keyword creation — use `ads-google-campaign-setup` for structure
- Ad copy and RSA authoring — use `ads-google-creative`
- Cross-channel budget allocation — use `ads-budget-optimization`
- GA4 property administration or event schema design — this covers the Ads API side only

## Content

| File | What's inside |
|------|---------------|
| `content/01-bidding.xml` | Bidding strategy types, portfolio strategy creation, campaign assignment, device bid adjustment (Python SDK) |
| `content/02-conversions.xml` | Conversion action types, creation with counting/attribution, tag retrieval, offline upload via gclid |
| `content/03-ga4-integration.xml` | GA4 link context, importing GA4 conversions, querying conversion data by action |

## Templates

| File | Purpose |
|------|---------|
| `templates/create-target-cpa.py` | Python function: create Target CPA portfolio bidding strategy |
| `templates/upload-offline-conversions.py` | Python function: batch upload offline conversions by gclid |
