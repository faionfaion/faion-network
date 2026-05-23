---
slug: plg-basics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Product-Led Growth go-to-market spec: product as primary acquisition / activation / retention vehicle; freemium vs free-trial vs reverse-trial model selection; self-serve checkout; sales-assist threshold \u2014 with named owner and ARR-tier triggers."
content_id: "2a1e09a995910e91"
complexity: medium
produces: spec
est_tokens: 5000
tags: [plg, go-to-market, self-serve, freemium, marketing]
---
# PLG Basics

## Summary

**One-sentence:** Product-Led Growth go-to-market spec: product as primary acquisition / activation / retention vehicle; freemium vs free-trial vs reverse-trial model selection; self-serve checkout; sales-assist threshold — with named owner and ARR-tier triggers.

**One-paragraph:** Product-Led Growth go-to-market spec: product as primary acquisition / activation / retention vehicle; freemium vs free-trial vs reverse-trial model selection; self-serve checkout; sales-assist threshold — with named owner and ARR-tier triggers. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Product can deliver standalone value without sales hand-holding (single-user TTV < 30 min).
- Pricing supports < $1K/mo self-serve tier (no enterprise-only customer).
- Named owner can ship the spec within 60 days.

## Skip If (ANY kills it)

- Product requires deep integration / configuration (no self-serve TTV possible).
- Average contract > $50K/year — PLG overhead doesn't pay back; stay sales-led.
- Pre-PMF — model selection without product-fit data misleads.

**Ефективно для:**

- SaaS founders що вибирають perfect-fit PLG model під product-shape.
- Marketing leads що пишуть першу PLG spec при переході зі sales-led.
- Команди з self-serve checkout але без disciplined PQL scoring.
- Аудит-ready середовища з вимогою explicit PLG model decision rationale.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/conversion-optimizer` | Parent CRO context — funnel + activation discipline. |
| `pro/marketing/growth-marketer` | Adjacent metric / experimentation context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-plg-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[plg-basics]]
- [[plg-implementation-guide]]
- [[plg-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
