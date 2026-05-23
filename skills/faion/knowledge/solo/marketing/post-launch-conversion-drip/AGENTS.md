---
slug: post-launch-conversion-drip
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Four-email drip for post-launch traffic spikes (PH, HN, viral): T+0 / T+2 / T+7 / T+14 — produces a versioned drip spec with per-email job, KPI, and suppression rule."
content_id: "82e744968037f1fb"
complexity: deep
produces: spec
est_tokens: 4900
tags: [marketing, solo, drip, post-launch, conversion]
---
# Post Launch Conversion Drip

## Summary

**One-sentence:** Four-email drip for post-launch traffic spikes (PH, HN, viral): T+0 / T+2 / T+7 / T+14 — produces a versioned drip spec with per-email job, KPI, and suppression rule.

**One-paragraph:** Four-email drip for post-launch traffic spikes (PH, HN, viral): T+0 / T+2 / T+7 / T+14 — produces a versioned drip spec with per-email job, KPI, and suppression rule. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator ran a high-volume launch (PH, HN front-page, viral thread) within the last 7 days.
- ≥100 emails or signups were captured during/after the launch.
- Basic email automation (ConvertKit, Loops, Resend, Mailchimp) is in place with tagging support.
- A named owner can author 4 emails plus a follow-up sequence and ship within 48 hours.

## Skip If (ANY kills it)

- Spike was < 50 signups — sample too small to justify a one-off drip.
- Already have a mature onboarding sequence with launch tagging — extend it instead.
- Product has no email-relevant value (anonymous instant-use tools) — drip will under-perform regardless.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Post Launch Conversion Drip task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `solo/sdd/sdd/AGENTS.md` | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end | 700 |
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
| `templates/drip-spec.md` | Markdown drip spec: 4 emails (T+0/+2/+7/+14) with job, single-CTA, KPI block, suppression rule. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-post-launch-conversion-drip.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[ph-launch-day-runbook]]
- [[newsletter-to-paid-funnel-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
