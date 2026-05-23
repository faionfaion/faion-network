---
slug: growth-app-store-optimization
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an ASO spec for one app: target keywords, title/subtitle/description fields, screenshot order, review-prompt timing, and 30-day re-baseline — for Apple App Store and Google Play.
content_id: "4555bc6b96a94d10"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["aso", "app-store", "keywords", "mobile", "solo"]
---
# App Store Optimization (ASO)

## Summary

**One-sentence:** Generates an ASO spec for one app: target keywords, title/subtitle/description fields, screenshot order, review-prompt timing, and 30-day re-baseline — for Apple App Store and Google Play.

**One-paragraph:** App Store Optimization (ASO) produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo mobile founder with ≥1 published app who needs an ASO spec with keyword targets, asset order, and review-prompt timing — before competing apps eat impressions.

## Applies If (ALL must hold)

- App is published or queued to publish on App Store and/or Google Play
- Keyword research data available (App Annie / Sensor Tower / AppFollow)
- Founder controls title, subtitle, screenshots, description fields

## Skip If (ANY kills it)

- Web app only — ASO does not apply (use SEO instead)
- Enterprise distribution outside public stores
- Pre-publish app missing screenshots / icon — fix asset gap first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current app metadata snapshot | table | App Store Connect / Play Console |
| Keyword research data | CSV | App Annie / Sensor Tower |
| Competitor benchmark (≥3 apps) | list | store search |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `growth-product-hunt-launch` | Adjacent launch channel. |
| `ops-dashboard-setup` | Dashboard tracks ASO KPIs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-one-app-per-spec, r2-keyword-set-5-to-10, r3-title-keyword-first, r4-screenshots-first-three-load-bearing, r5-review-prompt-after-success, r6-30-day-rebaseline | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-growth-app-store-optimization` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-growth-app-store-optimization` | haiku | Schema check + threshold checks; deterministic. |
| `review-growth-app-store-optimization` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-app-store-optimization.json` | JSON skeleton conforming to the output contract schema. |
| `templates/growth-app-store-optimization.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-app-store-optimization.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[growth-product-hunt-launch]]
- [[ops-dashboard-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
