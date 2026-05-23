---
slug: newsletter-issue-template-indie
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Weekly indie newsletter template: hook → story → lesson → CTA, ≤900 words, evidence-anchored — produces a single-issue spec a drafter can fill without re-deriving the structure."
content_id: "fdc9e3c8e89fbd1d"
complexity: medium
produces: spec
est_tokens: 4900
tags: [marketing, solo, newsletter, indie, weekly]
---
# Newsletter Issue Template Indie

## Summary

**One-sentence:** Weekly indie newsletter template: hook → story → lesson → CTA, ≤900 words, evidence-anchored — produces a single-issue spec a drafter can fill without re-deriving the structure.

**One-paragraph:** Weekly indie newsletter template: hook → story → lesson → CTA, ≤900 words, evidence-anchored — produces a single-issue spec a drafter can fill without re-deriving the structure. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Indie operator publishes (or wants to publish) a weekly newsletter on a paid platform (Substack, beehiiv, ConvertKit, Ghost).
- A named owner exists who will draft and ship the issue this cycle.
- Source-of-truth artefacts for the week (build-log, customer thread, metric snapshot) are available before drafting starts.
- Downstream consumer is a subscriber audience or a re-publisher (not a private notes file).

## Skip If (ANY kills it)

- No audience yet — write zero-to-100-subscribers content engine first (`build-in-public-cadence`).
- Topic is a one-off announcement — use `feature-launch-checklist` instead.
- Issue is paid-only and the product has no clear wedge — paid newsletters without a tested wedge churn within 2 issues.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Newsletter Issue Template Indie task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/newsletter-issue.md` | Markdown skeleton: hook-story-lesson-CTA blocks with word-budget and evidence-anchor slots. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-newsletter-issue-template-indie.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[newsletter-to-paid-funnel-template]]
- [[build-in-public-cadence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
