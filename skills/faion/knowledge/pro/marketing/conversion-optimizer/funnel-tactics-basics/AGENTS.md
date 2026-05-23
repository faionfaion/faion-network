---
slug: funnel-tactics-basics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Stage-indexed tactic catalog with quantified lift bands per stage (Top / Middle / Bottom / Onboarding), plus four stage-specific pre-launch checklists (landing page, signup form, checkout, onboarding)."
content_id: "f8e47b7f8e11f20c"
complexity: deep
produces: spec
est_tokens: 5000
tags: [funnel, tactics, landing-page, checkout, onboarding, marketing]
---
# Funnel Tactics Basics

## Summary

**One-sentence:** Stage-indexed tactic catalog with quantified lift bands per stage (Top / Middle / Bottom / Onboarding), plus four stage-specific pre-launch checklists (landing page, signup form, checkout, onboarding).

**One-paragraph:** Stage-indexed tactic catalog with quantified lift bands per stage (Top / Middle / Bottom / Onboarding), plus four stage-specific pre-launch checklists (landing page, signup form, checkout, onboarding). The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team has measurable funnel + named CRO owner.
- Team is planning pre-launch audit of one of: landing page, signup form, checkout, onboarding.
- Team has ≥ 100 weekly users / step (minimum for tactic measurement).

## Skip If (ANY kills it)

- No measurable funnel yet — funnel-basics-framework first.
- Team applying advanced personalization — use funnel-tactics-advanced instead.
- Pre-PMF — focus on retention, not stage tactics.

**Ефективно для:**

- Growth-marketers що пишуть першу спробу tactic-prioritization за stage.
- Команди що готують pre-launch audit перед website / checkout / onboarding ship.
- CRO managers що калібрують expectations: 'що очікувати від цього класу tactic?'
- Аудит-ready середовища з вимогою evidence-anchored lift expectations.

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
| `scripts/validate-funnel-tactics-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[funnel-basics-framework]]
- [[funnel-tactics-basics]]
- [[growth-conversion-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
