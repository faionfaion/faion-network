---
slug: rate-raise-conversation-script
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: When to raise (utilization, market signals), how much (10-25%), the conversation script, the bluff-call response — for annual rate raises on retainer/hourly clients.
content_id: "6d90a2802d139b94"
complexity: medium
produces: playbook-step
est_tokens: 4400
tags: [rate-raise-conversation-script, marketing, pro]
---
# Rate-Raise Conversation Script

## Summary

**One-sentence:** When to raise (utilization, market signals), how much (10-25%), the conversation script, the bluff-call response — for annual rate raises on retainer/hourly clients.

**One-paragraph:** Annual rate raise for existing retainer/hourly clients is the single highest-ROI freelancer move and the most-avoided. Output: decision criteria + script + counter-response playbook.

**Ефективно для:**

- Розмови про підвищення ставки на існуючому ретейнері/годинній моделі.
- Підготовки трьох counter-response сценаріїв перед розмовою.
- Pre-committed walk-away threshold (не каже "так" нижче N%).
- Команди фрілансерів, які раз на рік оновлюють ставки.

## Applies If (ALL must hold)

- freelancer with ≥3 months retainer/hourly client
- current utilization >70% OR market rate >15% above current
- founder has authority to walk if rejected

## Skip If (ANY kills it)

- rate locked in contract for ≥6 more months — wait
- client just expanded scope (give 60-90 days first)
- freelancer in onboarding phase (no leverage)

## Prerequisites

- current rate + market rate data (≥2 sources)
- utilization % over last 90 days
- list of value delivered in current engagement

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/late-invoice-dunning-sequence` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/scope-creep-prevention-on-hourly` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-raise-conversation-script.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/rate-raise-conversation-script.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rate-raise-conversation-script.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/late-invoice-dunning-sequence`
- peer methodology: `pro/marketing/scope-creep-prevention-on-hourly`
- peer methodology: `solo/marketing/freelance-pilot-pricing`
- external: https://philipmorganconsulting.com/raising-rates/; https://www.danmall.com/posts/how-to-raise-your-rates/

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

