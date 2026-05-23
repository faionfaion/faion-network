---
slug: newsletter-to-paid-funnel-template
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "End-to-end indie funnel: free newsletter → wedge product → paid offer with measurable conversion gates — produces a spec naming each stage's metric, gate, and owner."
content_id: "0d3cbc5c649bd2c6"
complexity: deep
produces: spec
est_tokens: 4900
tags: [marketing, solo, newsletter, funnel, conversion]
---
# Newsletter To Paid Funnel Template

## Summary

**One-sentence:** End-to-end indie funnel: free newsletter → wedge product → paid offer with measurable conversion gates — produces a spec naming each stage's metric, gate, and owner.

**One-paragraph:** End-to-end indie funnel: free newsletter → wedge product → paid offer with measurable conversion gates — produces a spec naming each stage's metric, gate, and owner. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Indie operator has ≥500 newsletter subscribers AND ≥3 issues of historical open/click data.
- A paid product (or wedge SKU) exists or is in build state within 60 days.
- A named owner exists who will publish the funnel spec and own conversion per stage.
- Email automation tooling (ConvertKit, Loops, Substack, beehiiv) can attribute conversions to issues.

## Skip If (ANY kills it)

- No paid product or wedge in sight — defer until offer exists, otherwise the spec rots.
- Audience < 500 — audience-development methodology applies first.
- Funnel is B2B enterprise (multi-touch, sales-assisted) — different methodology required.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Newsletter To Paid Funnel Template task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/newsletter-funnel-spec.md` | Markdown skeleton: stage table (free → wedge → paid) with conversion gates, owners, weekly KPIs. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-newsletter-to-paid-funnel-template.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[newsletter-issue-template-indie]]
- [[post-launch-conversion-drip]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
