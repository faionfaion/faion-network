# Business Model Research

## Summary

Systematic analysis of how a business will create, deliver, and capture value, structured as a Business Model Canvas (9 blocks) plus P10/P50/P90 unit economics (CAC, LTV, LTV:CAC, payback period) and 5 stress tests. Every assumption is tagged Hard (sourced) or Soft (founder estimate); LTV must never use a lifetime of more than 60 months.

## Why

Entrepreneurs build products without viable business models — "we'll figure out monetization later" is the #1 cause of post-PMF collapse. A Canvas alone is theater without unit economics; unit economics at a single point hide the P10 scenario that actually determines runway. The P10 verdict is the only one that matters for fundraising and hiring decisions.

## When To Use

- Pre-spec phase: founder has a product idea but no defended monetization story.
- Pricing decision under uncertainty: ARPU/margin/churn assumptions must be modeled before a price page ships.
- Pivot review: existing product is missing LTV:CAC >= 3:1 and the model itself may be broken.
- Investor memo/seed deck requiring "How we make money" section with stress tests.
- Multi-revenue-stream design: subscription + usage + marketplace fee blends.

## When NOT To Use

- Internal tools, OSS side-projects, hobby apps with no intent to monetize.
- Already-shipping products with 12+ months of real ARR data — use `aarrr-pirate-metrics` instead.
- Pure infrastructure libraries where revenue is a downstream consequence.
- Government/grant-funded work where the "customer" is a budget line.
- Two-sided marketplace pre-launch with zero supply — do `network-effects` first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-canvas-and-revenue-models.xml` | 9-block Canvas, 5 revenue archetypes (subscription, one-time, transaction, advertising, marketplace), variant table per archetype. |
| `content/02-unit-economics.xml` | CAC/LTV/payback formulas, P10/P50/P90 scenario model, 5 stress tests, churn floor rules. |
| `content/03-agentic-pipeline.xml` | 8-step workflow, subagents, prompt patterns (build + validate), gotchas, SDD integration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/business-model-canvas.md` | Fillable 9-block canvas with Hard/Soft cell tagging. |
| `templates/unit-econ-scenarios.sh` | P10/P50/P90 LTV:CAC and payback from arpu/margin/churn/cac args. |

## Scripts

none
