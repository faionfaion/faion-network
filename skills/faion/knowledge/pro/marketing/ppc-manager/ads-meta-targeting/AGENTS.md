# Meta Targeting & Audiences

## Summary

Three-tier audience strategy for Meta Ads: Core (interest/demographic/behavior) for cold traffic, Custom (pixel + email + engagement) for warm traffic, and Lookalike (1%, 2-3%, 5-10% of a quality source) for scaling. Build exclusion audiences (purchasers, subscribers) before launching any campaign. Use Advantage+ only for large budgets with broad-appeal products; manual targeting for niche or small budgets.

## Why

Audience quality is a direct multiplier on CPA — showing ads to the wrong people converts at 0.2% instead of 2%, a 10x cost difference. Lookalike audiences built from purchasers (not visitors) produce the highest-quality cold traffic. Excluding converters prevents wasted spend and audience pollution in prospecting campaigns.

## When To Use

- Setting up audiences before launching any Meta campaign.
- Scaling a campaign by expanding from Core/Interest to Lookalike.
- Building retargeting audiences by pixel behavior (pricing page, cart, checkout).
- Testing which audience type produces the lowest CPA (Core vs LAL vs retarget).

## When NOT To Use

- Audience size below 500K for Core/Interest — ad delivery is constrained and CPM spikes.
- Lookalike with a source smaller than 1,000 people — match quality is poor; build up the source first.
- Advantage+ when the product is niche or the budget is small — Meta's AI needs scale to work.
- When pixel is not installed and verified — Custom and Lookalike audiences won't populate correctly.

## Content

| File | What's inside |
|------|---------------|
| `content/01-audience-types.xml` | Core/Custom/Lookalike definitions, setup steps, best-source ranking, size guidelines. |
| `content/02-testing-and-exclusions.xml` | Testing structure, exclusion strategy, audience layering, Advantage+ decision criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/custom-audience-library.md` | Checklist of website, engagement, customer, and exclusion audiences to create. |
| `templates/audience-testing-log.md` | Audience test tracking table with spend, conversions, CPA, and winner decision. |
