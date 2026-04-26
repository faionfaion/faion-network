# Meta Campaign Setup

## Summary

End-to-end checklist for launching a Facebook/Instagram campaign via Meta Ads Manager: install and verify the Meta Pixel, choose the correct campaign objective, configure the three-tier structure (Campaign → Ad Set → Ad), set targeting and placements, upload at least 3 creative variations per ad set, and avoid editing during the learning phase. The core rule is: select the objective that matches the actual business action — choosing Traffic when the goal is leads optimizes for clicks, not conversions, and wastes budget.

## Why

Meta's delivery system optimizes for the event you specify as your objective. Wrong objective = wrong optimization signal. The learning phase requires ~50 conversions per ad set per week; editing during learning resets the counter and extends unstable performance. Campaign Budget Optimization (CBO) distributes spend across ad sets dynamically, outperforming fixed ad-set budgets once the algorithm has enough signal. These mechanics make correct initial setup critical — retrofitting an objective after launch requires a new campaign.

## When To Use

- Launching a new Meta campaign from scratch
- Auditing an existing campaign's structure for mis-aligned objectives or missing Pixel setup
- Setting up the naming conventions and UTM parameters for a new product line
- Configuring CBO vs. ad-set budget for a new test
- Onboarding a new account that has never run Meta ads

## When NOT To Use

- Audience construction (custom, lookalike, interest targeting) — use `meta-audience-targeting`
- Creative copy and image/video spec decisions for Instagram placements — use `instagram-ads`
- Budget reallocation across live campaigns — use `ads-budget-optimization`
- Reporting and analysis of a running campaign — use the Meta reporting methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-pixel-setup.xml` | Pixel installation checklist, standard events to track, verification methods |
| `content/02-campaign-structure.xml` | Three-tier model, objective-to-goal mapping, CBO vs ad-set budget |
| `content/03-ad-set-config.xml` | Audience size guidelines, placement selection, optimization goal |
| `content/04-ads-and-launch.xml` | Ad components, minimum creative set, UTM parameters, learning phase rules |
| `content/05-antipatterns.xml` | Common mistakes: no pixel, wrong objective, too-narrow audience, editing during learning |

## Templates

| File | Purpose |
|------|---------|
| `templates/campaign-naming.txt` | Naming convention for campaigns, ad sets, and ads |
| `templates/launch-checklist.md` | Pre-launch checklist: pixel, objective, budget, targeting, creatives, tracking |
