---
slug: solo-saas-legal-docs-pack
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Minimum five legal documents (ToS, Privacy, Cookie, Refund, DPA) sourced from Stripe / Iubenda / Termly / Vanta with billing-activation gates that block ship until live.
content_id: "c3de9d8937b69245"
complexity: light
produces: checklist
est_tokens: 2900
tags: [legal, solo-saas, pre-launch, tos-privacy]
---
# Solo Saas Legal Docs Pack

## Summary

**One-sentence:** Minimum five legal documents (ToS, Privacy, Cookie, Refund, DPA) sourced from Stripe / Iubenda / Termly / Vanta with billing-activation gates that block ship until live.

**One-paragraph:** Minimum five legal documents (ToS, Privacy, Cookie, Refund, DPA) sourced from Stripe / Iubenda / Termly / Vanta with billing-activation gates that block ship until live. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Solo Saas Legal Docs Pack on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Solo SaaS preparing to activate billing.
- Operates in EU / US (GDPR / CCPA scope).
- Owner accepts 'good enough to bill' standard (not enterprise legal).
- Budget for a lawyer review later, not now.

## Skip If (ANY kills it)

- Enterprise tier — bespoke MSA required.
- Regulated industry (health / finance) — defer to specialist counsel.
- Pre-billing prototype with no payments.
- Single-customer paid pilot — direct contract suffices.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product positioning + business model | doc | Self |
| Payment processor chosen | config | Stripe |
| Hosting region + data location | config | Hetzner / AWS |
| Cookie + analytics inventory | list | Self |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/product-launch` | Sequenced with launch; legal must precede billing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-solo-saas-legal-docs-pack` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-solo-saas-legal-docs-pack` | haiku | Schema check + threshold checks; deterministic. |
| `review-solo-saas-legal-docs-pack` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-saas-legal-docs-pack.json` | JSON skeleton conforming to the output contract schema. |
| `templates/solo-saas-legal-docs-pack.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-saas-legal-docs-pack.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-launch]]
- [[subscription-lifecycle-edge-cases]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
