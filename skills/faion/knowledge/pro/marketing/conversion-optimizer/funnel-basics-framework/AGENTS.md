---
slug: funnel-basics-framework
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "7-phase systematic funnel optimization process \u2014 map / measure / find biggest drop / diagnose / hypothesize / test / repeat \u2014 with the discipline rule: always fix the biggest absolute user loss first, not the easiest step."
content_id: "967f14dab2d73d0b"
complexity: deep
produces: spec
est_tokens: 5000
tags: [funnel, conversion, framework, process, marketing]
---
# Funnel Basics Framework

## Summary

**One-sentence:** 7-phase systematic funnel optimization process — map / measure / find biggest drop / diagnose / hypothesize / test / repeat — with the discipline rule: always fix the biggest absolute user loss first, not the easiest step.

**One-paragraph:** 7-phase systematic funnel optimization process — map / measure / find biggest drop / diagnose / hypothesize / test / repeat — with the discipline rule: always fix the biggest absolute user loss first, not the easiest step. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Funnel has measurable steps from entry to goal (signup / purchase / activation).
- Conversion is below industry benchmark OR plateaued.
- Team has ≥ 7 days of tracking data per step and ≥ 100 users per step (minimum for diagnosis).

## Skip If (ANY kills it)

- Fewer than 100 users / step — sample too small for meaningful diagnosis.
- No analytics instrumentation — map + measure steps first.
- Pre-PMF — fix retention before acquisition funnel.

**Ефективно для:**

- CRO-команди що тільки впроваджують funnel-discipline (вперше structured підхід).
- Marketing leads що приймають prioritization decisions під hypothesis pressure.
- Команди де optimization дрейфує до 'що легше зробити' замість 'що дасть більше lift'.
- Аудит-ready середовища з вимогою repeatable optimization process.

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
| `scripts/validate-funnel-basics-framework.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[funnel-basics-framework]]
- [[funnel-tactics-basics]]
- [[growth-conversion-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
