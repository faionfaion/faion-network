# Gumroad Ops Playbook

## Summary

**One-sentence:** Operate a Gumroad product end-to-end — listing fields, A/B copy, affiliate program, EU VAT (Gumroad acts as Merchant of Record), license key delivery, post-purchase upsell.

**One-paragraph:** Gumroad is the default distribution channel for indie digital products (templates, ebooks, mini-tools, prompt packs). This playbook closes the gap: listing-page optimisation (cover, subtitle, social proof slot), A/B copy via Gumroad's experiments, affiliate program setup (commission %, payout cadence), EU VAT handled by Gumroad as Merchant of Record (you do NOT collect VAT yourself), license key delivery for paid software via Gumroad's license API, and post-purchase upsell to a follow-on product. Output is a Gumroad listing config + ops checklist + monthly review cadence.

**Ефективно для:**

- Selling digital files / templates / mini-tools where you want zero billing/tax burden.
- Cross-border buyers (EU especially) — Gumroad as MoR handles VAT automatically.
- License-keyed software where validation needs Gumroad's license API.
- Affiliate-driven micro-launches (Product Hunt + HN + IH same week).

## Applies If (ALL must hold)

- The product is a digital good distributable via Gumroad (file download, license key, link drop).
- Founder is comfortable letting Gumroad take the 10% + payment fees in exchange for MoR + tax handling.
- The product has at least one strong cover image + a 280-char subtitle drafted.
- A follow-on or upsell product exists or is planned within 90 days.

## Skip If (ANY kills it)

- Product is a SaaS subscription with high ARPU — Stripe-direct is cheaper at scale.
- Founder must keep all tax/legal responsibility (Gumroad MoR clause unacceptable).
- File too large or licensing rules incompatible with Gumroad's terms (e.g. NSFW thresholds).
- Product is enterprise-procured with NET-30 invoicing — Gumroad does not support invoicing.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product cover image (1280×720+) | PNG / JPG | designer |
| Subtitle ≤280 chars | string | founder |
| Pricing decision (fixed, pwyw, tiers) | scalar | founder |
| Affiliate commission % decision (0-90) | scalar | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lemon-squeezy-ops-playbook]] | Sibling MoR — used when Gumroad's terms or fees do not fit. |
| [[pricing-experiment-runbook]] | Pricing-change discipline carries over to Gumroad's A/B copy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: 6-field listing, MoR not collecting VAT yourself, license API for software, affiliate 30-50% range, A/B copy 2-week min, monthly review | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for listing config + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix): cover blur, missing license, affiliate broken, double-tax | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: build cover → fill fields → wire license/affiliate → A/B copy → launch → monthly review | 800 |
| `content/05-examples.xml` | essential | Worked example: $19 prompt-pack listing with affiliate at 50% | 700 |
| `content/06-decision-tree.xml` | essential | Tree routing observables → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `listing_field_fill` | haiku | Template fill once decisions are made. |
| `subtitle_copywriting` | sonnet | 280-char hook with tone control. |
| `affiliate_program_setup` | sonnet | Commission + payout + recruitment mechanics. |
| `monthly_review` | sonnet | Aggregate metrics + narrate top sellers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gumroad-listing.yaml` | Listing field skeleton ready to fill |
| `templates/affiliate-invite.md` | Affiliate recruitment email template |
| `templates/_smoke-test.json` | Minimum viable listing config for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gumroad-ops-playbook.py` | Validate listing config against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[lemon-squeezy-ops-playbook]]
- [[pricing-experiment-runbook]]
- [[ih-build-update-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps product type (file/license/saas), MoR acceptance, cover quality, and affiliate intent to a rule from `01-core-rules.xml`, telling the agent whether to publish, block on a missing field, or skip Gumroad for a better-fit channel. Walk it on every fresh listing; do not cache outcomes across products.
