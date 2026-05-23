---
slug: funnel-basics-examples
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Concrete before/after funnel case studies across SaaS, e-commerce, mobile app, B2B lead-gen, and subscription \u2014 paired with industry benchmark tables by step \u2014 so teams can ground hypotheses in real patterns, not vibes."
content_id: "4613a5432c18b03b"
complexity: medium
produces: spec
est_tokens: 5000
tags: [funnel, conversion, case-studies, benchmarks, marketing]
---
# Funnel Basics Examples

## Summary

**One-sentence:** Concrete before/after funnel case studies across SaaS, e-commerce, mobile app, B2B lead-gen, and subscription — paired with industry benchmark tables by step — so teams can ground hypotheses in real patterns, not vibes.

**One-paragraph:** Concrete before/after funnel case studies across SaaS, e-commerce, mobile app, B2B lead-gen, and subscription — paired with industry benchmark tables by step — so teams can ground hypotheses in real patterns, not vibes. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team has a defined funnel and wants reference benchmarks to anchor hypothesis prioritisation.
- Team vertical maps to one of: SaaS, e-commerce, mobile app, B2B lead-gen, subscription.
- Named CRO owner can read + apply the examples within 5 business days.

## Skip If (ANY kills it)

- Pre-PMF startup with < 100 users / step — examples don't transfer at low volume.
- Highly bespoke funnel (deep enterprise, hardware) — reference cases will mislead more than help.
- Team is in execution mode on one specific hypothesis — examples are for prioritisation phase only.

**Ефективно для:**

- Growth-команди що шукають reference benchmarks для свого funnel шару (SaaS / DTC / mobile).
- Marketers що пишуть першу funnel hypothesis і потребують 'як це робили інші'.
- Команди у вертикалях що цитують industry-specific drop-off norms.
- CRO трейнінги / onboarding: показати реальні before/after як teaching aid.

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
| `scripts/validate-funnel-basics-examples.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[funnel-basics-framework]]
- [[funnel-tactics-basics]]
- [[growth-conversion-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
