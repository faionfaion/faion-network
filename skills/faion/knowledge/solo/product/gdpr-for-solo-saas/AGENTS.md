---
slug: gdpr-for-solo-saas
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pragmatic GDPR posture for a one-person SaaS: scope the obligations that actually apply, ship the minimal data-protection set, name when to lawyer up \u2014 not the same content as enterprise GDPR."
content_id: "13932318b81002c1"
complexity: medium
produces: checklist
est_tokens: 4100
tags: [gdpr-for-solo-saas, product, solo, gdpr, compliance]
---
# Gdpr For Solo Saas

## Summary

**One-sentence:** Pragmatic GDPR posture for a one-person SaaS: scope the obligations that actually apply, ship the minimal data-protection set, name when to lawyer up — not the same content as enterprise GDPR.

**One-paragraph:** Solo SaaS operators are told to 'be GDPR-compliant' and freeze, or to ignore GDPR entirely. Both fail. This methodology pins the minimum viable posture for one-person operations: (1) data-inventory worksheet, (2) lawful-basis declaration per data category, (3) data-processor list (Stripe, Postmark, Plausible, etc.), (4) privacy policy template tuned for solo SaaS, (5) DPA / SCC checklist, (6) breach-response one-pager, (7) explicit 'when to lawyer up' triggers (EU revenue >€10k, sensitive categories, B2B-with-DPA-required).

**Ефективно для:**

- Solo SaaS operator serving any EU traffic.
- Indie tool maker with EU subscribers via newsletter.
- Operator panicking after first 'where is your DPA?' request.
- Founder choosing between freeze, ignore, or pragmatic posture.

## Applies If (ALL must hold)

- Product processes data of EU residents (any traffic counts).
- Operator is solo (no in-house counsel).
- Revenue from EU is under €100k/year (above this, switch to enterprise GDPR).
- Data categories are limited to standard SaaS (account info, usage events, billing).

## Skip If (ANY kills it)

- Product processes special-category data (health, biometrics, children) — lawyer up immediately.
- Operator is in a regulated B2B vertical (HIPAA, PCI) — use that methodology.
- EU revenue >€100k — switch to enterprise GDPR + named DPO.
- Operator has corporate counsel — let them run it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Data inventory (auto or manual) | md / spreadsheet | operator audit |
| Data-processor list | csv | billing / infra inventory |
| Privacy policy reference | current published URL | website |
| Subscriber + revenue counts by region | csv / dashboard | analytics + billing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent operating context |
| `solo/product/maintain-mode-sops-solo` | ops-doc pattern for breach response |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gdpr-for-solo-saas` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gdpr-for-solo-saas.md` | Markdown skeleton for the checklist artefact, matching content/02-output-contract.xml |
| `templates/gdpr-for-solo-saas.schema.json` | JSON Schema seed + filled fixture for the checklist artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gdpr-for-solo-saas.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[maintain-mode-sops-solo]]`
- `[[feedback-loop-customer-reply-templates]]`
- `[[indie-portfolio-scorecard]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
