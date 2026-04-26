# PLG Optimization Tactics

## Summary

A tactics catalog for improving activation, free-tier-to-paid, and expansion conversion in an existing PLG product. Core rules: pair every tactic with the metric it moves and a current baseline; show upgrade prompts at 80% of limit (not 100%); cap prompts to one per session and zero during the first session; name a comparable customer and quantify value in all upgrade copy; reject "Upgrade Now" and "Premium Plan" as CTA text.

## Why

Post-PMF PLG products plateau because teams lack a structured tactic backlog tied to measurable funnel steps. This methodology provides an ICE-scored tactic index covering activation friction reduction, free-tier balance, self-serve checkout design, and expansion signal detection. ICE scoring ensures the backlog is ordered by impact × confidence × ease rather than team preference.

## When To Use

- Existing PLG product where activation, free-tier-to-paid, or expansion conversion has plateaued.
- Designing a free tier or self-serve checkout and wanting a curated friction checklist to instrument before launch.
- Generating in-product upgrade copy, feature-gate messaging, and pricing-page variants.
- Producing a quarterly A/B test backlog scored against the tactic idea bank.

## When NOT To Use

- Pre-PMF teams without measurable activation data — generic tactics distract from PMF discovery.
- Pure sales-led products with ACV above ~$50K where self-serve patterns do not survive procurement.
- Single-event transactions (one-shot ecommerce, ticketing) with no expansion or seat-growth surface.
- Hard-regulated products (healthcare, banking) where "instant access, no approval" recommendations conflict with compliance.

## Content

| File | What's inside |
|------|---------------|
| `content/01-activation-tactics.xml` | Friction reduction, progressive onboarding, template-first patterns, free-tier balance (too-generous / balanced / too-restrictive), onboarding checklist. |
| `content/02-conversion-and-expansion.xml` | Self-serve checkout design, upgrade prompt rules (timing, copy, frequency), expansion signal detection, A/B test idea bank. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ice-scorer.py` | Dataclass for ICE-scoring tactic backlog; bucket() returns test_now / this_quarter / if_capacity / backlog. |
