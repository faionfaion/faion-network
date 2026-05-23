---
slug: white-label-partnership-design
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Evaluating, pricing, and contracting white-label work — distinct from partnership-strategy because the buyer is an agency, the brand is hidden, and the legal shape differs.
content_id: "e8dfbcc5d82703e2"
complexity: deep
produces: spec
est_tokens: 4400
tags: [white-label-partnership-design, marketing, pro]
---
# White-Label Partnership Design

## Summary

**One-sentence:** Evaluating, pricing, and contracting white-label work — distinct from partnership-strategy because the buyer is an agency, the brand is hidden, and the legal shape differs.

**One-paragraph:** A common micro-agency growth lever is white-labeling delivery for a larger agency. The corpus has no methodology for evaluating, pricing, or contracting white-label work — including the trap of becoming captive. Output: white-label decision + pricing + contract clauses + captivity guardrails.

**Ефективно для:**

- Micro-agency, що пропонують white-label larger agency.
- Pricing ≥1.5-2× direct rate; нижче — net loss.
- Captivity cap: жоден primary agency &gt; 30% revenue.
- Anti-circumvent clause + brand-attribution policy + quarterly review.

## Applies If (ALL must hold)

- micro-agency offered white-label delivery role
- primary agency would otherwise have to refuse work due to capacity OR niche mismatch
- founder has authority to accept or refuse

## Skip If (ANY kills it)

- direct client work (no white-label layer)
- agency with no spare capacity (white-label adds risk)
- primary agency with hostile terms (no negotiation room)

## Prerequisites

- current rate card
- list of services offered
- contract template editable for white-label clauses

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/agency-to-agency-referral` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/agency-niche-positioning` | peer methodology — produces inputs or consumes outputs |

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
| `templates/white-label-partnership-design.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/white-label-partnership-design.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-white-label-partnership-design.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/agency-to-agency-referral`
- peer methodology: `pro/marketing/agency-niche-positioning`
- peer methodology: `pro/marketing/scope-creep-prevention-on-hourly`
- external: https://philipmorganconsulting.com/white-label/; https://blog.hubspot.com/agency/white-labeling

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

