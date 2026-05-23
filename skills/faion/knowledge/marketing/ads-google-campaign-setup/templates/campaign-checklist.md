<!-- purpose: legacy template for ads-google-campaign-setup — campaign-checklist -->
<!-- consumes: per AGENTS.md Prerequisites -->
<!-- produces: artefact per content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml, content/06-decision-tree.xml -->
<!-- token-budget-impact: ~400-1200 tokens when loaded as context -->

# Campaign Launch Checklist: [Campaign Name]

## Pre-Launch

- [ ] Conversion action created in Google Ads
- [ ] Google Tag installed and verified firing in last 24 hours
- [ ] GA4 linked to Google Ads account
- [ ] Remarketing audience created

## Campaign Settings

- [ ] Campaign type: Search
- [ ] Networks: Search only (Display and Partners disabled)
- [ ] Locations: geoTargetConstants/[id] format
- [ ] Languages: [list]
- [ ] Budget: $[X]/day ([X * 1,000,000] micros)
- [ ] Bidding: Maximize Conversions (no Target CPA)
- [ ] Status: PAUSED
- [ ] start_date set: [date]
- [ ] end_date set: [date or never]
- [ ] Naming: [Product]_[Type]_[Goal]_[Date] format

## Ad Groups

- [ ] AG1: [Theme] — [N] keywords
- [ ] AG2: [Theme] — [N] keywords
- [ ] AG3: [Theme] — [N] keywords

## Ads

- [ ] 1 RSA minimum per ad group
- [ ] 15 headlines per RSA (30 chars each, validated)
- [ ] 4 descriptions per RSA (90 chars each, validated)
- [ ] Primary keyword in at least one headline

## Extensions (Assets)

- [ ] Sitelinks: 4-6 (using Asset resources, not Extension service)
- [ ] Callouts: 4-6
- [ ] Structured snippets: at least one category
- [ ] Images: logo and/or product

## Go-Live Gate

- [ ] Launch gate script passed (all ok)
- [ ] Human approval received
- [ ] Status flipped to ENABLED
