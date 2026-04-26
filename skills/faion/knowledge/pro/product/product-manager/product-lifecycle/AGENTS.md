# Product Lifecycle Management

## Summary

A four-stage framework (Introduction → Growth → Maturity → Decline) for diagnosing which lifecycle stage a product is in and applying the matching investment strategy. Each stage has distinct focus areas, key metrics, and transition triggers. The process runs in four steps: assess stage from metrics, validate with multi-quarter trends, apply stage-appropriate strategy, and plan the next-stage transition.

## Why

Products managed with the same tactics regardless of maturity stage waste investment. Growth acquisition tactics applied to a Maturity product over-spend on CAC; optimization investments applied to an Introduction product starve PMF discovery. Stage-aware allocation is the lever: right strategy, right metrics, right expectations per stage.

## When To Use

- Quarterly portfolio review — decide investment level for each shipped product and stop applying growth budget to maturity or decline assets.
- A product hits a metrics inflection (growth slows from 30% to 8%, churn jumps) — need a structured stage reassessment, not a gut call.
- Pre-roadmap step: tag every product with its stage before sequencing the year.
- End-of-life decision: product declining for 3+ quarters, need a sunset plan with migration timeline.
- Investor or board update: defending why a Maturity product gets retention budget instead of new features.
- Stage transition checkpoint: Introduction product hits PMF and must shift from "learn fast" to "scale" tooling.

## When NOT To Use

- Pre-PMF startup with one product still hunting for fit — there is no lifecycle yet, only a discovery loop.
- Sub-feature decisions inside one product (which feature to build next) — RICE / MoSCoW are sharper at that grain.
- Pure B2B services / agency revenue with no productized asset — lifecycle math is undefined.
- Internal tools / platforms with no external customers — they have a usefulness curve, not a revenue curve.
- Crisis weeks (P0 outage, security incident) — survival first, restore lifecycle planning after.

## Content

| File | What's inside |
|------|---------------|
| `content/01-stages.xml` | Stage characteristics, focus areas, metrics, and stage-appropriate strategies table. |
| `content/02-process.xml` | Four-step assessment process; transition planning; common mistakes. |
| `content/03-examples.xml` | SaaS product in Growth and legacy product in Decline worked examples. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lifecycle-assessment.md` | Metrics table, stage indicator matrix, assessed stage block, transition plan. |
| `templates/stage-strategy-guide.md` | Focus areas, key metrics, investment priorities, risks, success criteria per stage. |
| `templates/stage-suggest.sh` | Bash + Python: rule-based first-pass stage classification from MRR CSV. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/stage-suggest.sh` | Classifies products by lifecycle stage from quarterly MRR CSV; emits ambiguous rows for LLM review. |
