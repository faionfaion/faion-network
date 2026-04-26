# Retargeting

## Summary

Full-funnel retargeting strategy: segment past visitors by intent (all visitors → blog readers → product viewers → pricing viewers → cart abandoners), tailor ad messaging to each segment's stage, apply frequency caps to prevent fatigue, and always exclude recent converters from acquisition campaigns. Retargeting should be 20-30% of total ad spend and delivers 40-70% lower CPA versus cold prospecting.

## Why

97% of website visitors leave without converting. Retargeting recovers that spend by showing relevant ads to people who already know the brand — they convert at 2-4x the rate of cold traffic. The key is segmentation: showing a brand reminder to a cart abandoner, or a broad awareness ad to a pricing-page visitor, wastes the intent signal. Messaging must match where the person is in the funnel.

## When To Use

- Any campaign where a pixel is installed and website audience segments are large enough (1,000+).
- After launching prospecting campaigns to recover non-converters.
- Building sequential ad sequences (reminder → benefits → social proof → urgency).
- Upselling or cross-selling to past purchasers.

## When NOT To Use

- Before the pixel is installed and events are verified — audiences won't populate.
- Audience size under 1,000 — Meta/Google will throttle delivery; build up traffic first.
- When ad fatigue is already high (frequency >5 and CTR declining) — pause and refresh creative.
- For purely brand-awareness campaigns with no conversion goal — retargeting requires a defined conversion event.

## Content

| File | What's inside |
|------|---------------|
| `content/01-segmentation.xml` | Intent-based audience segments, tracking setup, pixel event requirements, budget guidelines. |
| `content/02-messaging-and-sequences.xml` | Segment-to-message mapping, sequential retargeting stages, frequency caps, exclusion windows. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retargeting-audiences.md` | Full audience setup table (website, engagement, customer, exclusions). |
| `templates/retargeting-campaign-structure.md` | Campaign/ad-set structure for 3-tier funnel retargeting. |
