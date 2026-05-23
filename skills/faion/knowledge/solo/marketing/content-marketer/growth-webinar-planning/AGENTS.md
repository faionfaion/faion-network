---
slug: growth-webinar-planning
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a webinar-planning artefact (format + content outline + 3-week promo plan + registration page) gated by promo-start lead time and registration page completeness."
content_id: "92b9ff50f0a6597b"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["webinar", "planning", "promo", "registration-page", "solo"]
---
# Webinar Planning

## Summary

**One-sentence:** Produces a webinar-planning artefact (format + content outline + 3-week promo plan + registration page) gated by promo-start lead time and registration page completeness.

**One-paragraph:** Solo operators decide to host a webinar 5 days out and watch attendance collapse. This methodology pins planning: ≥3-week promo window, named format chosen before content, ≥3 promo channels, registration-page checklist (outcome + bio + agenda + social proof + signup), and slide outline locked ≥2 weeks prior. Output: a webinar plan spec.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-webinar-planning» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator has ≥3 weeks of runway before target webinar date.
- Target audience size + channel mix is known.
- Operator has ≥3 promo channels available.

## Skip If (ANY kills it)

- Webinar date is <3 weeks out — accept reduced fill or delay.
- No registration platform available (Zoom / Demio / Crowdcast).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Webinar topic + outcome | doc | operator |
| Audience profile + size estimate | doc | marketing |
| Promo channel list with reach estimates | doc | marketing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/growth-webinar-delivery` | Downstream delivery runbook. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the webinar-plan artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-webinar-planning.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-webinar-planning.json` | webinar-plan JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-webinar-planning.py` | Validate the webinar-plan artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-webinar-delivery]]
- [[messaging-house-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
