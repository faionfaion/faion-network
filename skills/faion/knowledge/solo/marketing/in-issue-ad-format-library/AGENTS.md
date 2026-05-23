---
slug: in-issue-ad-format-library
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Library of 4 in-issue ad formats (top-banner, soft-PS, mid-issue-case, dedicated-send) with placement rules, CTR + CVR benchmarks, and a max-rotation cadence.
content_id: "91c13862b03a3d8b"
complexity: medium
produces: rubric
est_tokens: 4400
tags: [newsletter, in-issue-ad, conversion, founder-self-promo, ctr-cvr]
---
# In-Issue Ad Format Library

## Summary

**One-sentence:** A library of 4 in-issue ad formats — top-banner, soft P.S., mid-issue case, dedicated send — with placement rules, CTR + CVR benchmarks, and a max-rotation cadence per format.

**One-paragraph:** Self-promoting inside your own newsletter is awkward without conventions. This library codifies 4 formats with placement rules and rotation limits: top-banner (above-the-fold tile, max 1×/issue), soft P.S. (≤2 sentences at the foot, ≥3×/4 issues allowed), mid-issue case (a 1-paragraph case study tied to issue topic, max 1×/2 issues), dedicated send (full-issue promo, max 1×/6 issues). Each format ships CTR + CVR benchmarks measured against the founder's own 90-day median so format effectiveness is comparable. Output is the ad-format library + rotation plan + monthly review.

**Ефективно для:**

- Newsletter operators converting free readers into paid customers.
- Founders with 500-50000 subscribers and a paid product to push.
- Avoiding "in-bizdev" guilt: structured formats make self-promo a deliberate choice, not creep.
- Negotiating sponsor placements — the library is the rate-card structure.

## Applies If (ALL must hold)

- Operator runs a newsletter with ≥500 subscribers and ≥4 weeks of issue history.
- A paid product / waitlist / lead magnet exists to direct traffic to.
- Operator has open-rate + click-tracking enabled (Substack, ConvertKit, Beehiiv, Buttondown).
- Operator is willing to rotate formats per the cadence rules (not always banner).

## Skip If (ANY kills it)

- Newsletter is paid-only with no free tier — in-issue ads to paying readers fatigue them.
- Subscriber count &lt; 500 — sample too small for benchmark math.
- Operator already runs sponsored ads exclusively — the format library is for own-product promo.
- No product / waitlist / lead magnet to send traffic to.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 90-day issue archive with open-rate + CTR per send | CSV | newsletter platform |
| Per-format CTR + CVR baseline | scalars | computed locally |
| Active product / waitlist URL | URL | founder |
| Rotation calendar (next 8 issues) | YAML | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[hook-bank-template]] | Soft-PS copy and mid-issue case hooks feed the bank; bank patterns inform new ad copy. |
| [[icp-fit-scorecard-solo]] | Click-then-convert rates feed back into the ICP scorecard signal. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: 4 named formats, placement constraints, per-format cadence cap, baseline-relative CTR/CVR, max self-promo share 25%, monthly review | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for format library + rotation plan + benchmark block + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: banner-fatigue, dedicated-send over-use, PS-fatigue, no-baseline | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: compute baseline → pick formats → place per cadence → measure → rotate → monthly review | 800 |
| `content/05-examples.xml` | essential | Worked example: 5k-subscriber newsletter with 8-issue rotation plan + observed CTR/CVR | 700 |
| `content/06-decision-tree.xml` | essential | Tree routing observables → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `baseline_compute` | haiku | Mechanical aggregation. |
| `format_placement_decision` | sonnet | Bounded judgement on issue topic vs format fit. |
| `rotation_plan_8_issues` | sonnet | Constraint satisfaction across cadence rules. |
| `monthly_review` | sonnet | Aggregate and narrate top-performing format. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ad-format-library.yaml` | 4-format library skeleton with cadence caps |
| `templates/rotation-plan.csv` | 8-issue rotation plan ready to fill |
| `templates/_smoke-test.json` | Minimum viable library + plan + benchmarks for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-in-issue-ad-format-library.py` | Validate library + rotation plan against 02-output-contract schema | Pre-publish gate / monthly review |

## Related

- [[hook-bank-template]]
- [[icp-fit-scorecard-solo]]
- [[internal-linking-strategy-graph]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps subscriber count, baseline availability, target product, and cadence violations to a rule from `01-core-rules.xml`, telling the agent whether to publish the rotation plan, block on a missing constraint, or skip the library. Walk it on every fresh rotation plan; do not cache outcomes across plans.
