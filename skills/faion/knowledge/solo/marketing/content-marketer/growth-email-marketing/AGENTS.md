---
slug: growth-email-marketing
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a value-first email program artefact (list-building + welcome + segmentation + sales sequences) gated by deliverability and consent."
content_id: "12b9ff50f0a6597b"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["email-marketing", "list-building", "welcome-sequence", "segmentation", "solo"]
---
# Email Marketing for Solo Operators

## Summary

**One-sentence:** Produces a value-first email program artefact (list-building + welcome + segmentation + sales sequences) gated by deliverability and consent.

**One-paragraph:** Solo operators broadcast to a single list with multi-CTA newsletters and watch open rates collapse. This methodology pins a value-first email program: organic list growth via lead magnet, double opt-in, sub-5-minute welcome trigger, segmented sends with one CTA each, and quarterly hygiene. Output: an email-program spec wired to deliverability gates (<2% bounce, <0.1% complaint).

**Ефективно для:**

- готова основа для повторюваної задачі «growth-email-marketing» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator runs ≥1 email channel OR is launching one.
- ESP supports behavior triggers + segmentation (Buttondown / Mailchimp / ConvertKit class).
- Sender domain is configured with SPF + DKIM + DMARC.

## Skip If (ANY kills it)

- Operator owns no email list and refuses to build one organically.
- Sender domain has unresolved deliverability issues (DMARC fail / blacklist).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subscriber list with source per signup | CSV | ESP export |
| Lead magnet asset | PDF / Notion / template | marketing drive |
| Welcome email draft | markdown / ESP draft | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/growth-newsletter-growth` | Upstream list-growth methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the email-program artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/growth-email-marketing.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-email-marketing.json` | email-program JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-email-marketing.py` | Validate the email-program artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-newsletter-growth]]
- [[growth-onboarding-emails]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
