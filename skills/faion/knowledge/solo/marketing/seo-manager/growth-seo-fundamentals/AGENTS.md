---
slug: growth-seo-fundamentals
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Three-pillar SEO baseline (Technical / On-Page / Off-Page) covering audit checklist, content optimisation by intent, and metric baseline — produces an audit checklist artefact."
content_id: "71330b73df757013"
complexity: medium
produces: checklist
est_tokens: 4900
tags: [marketing, solo, seo, growth, fundamentals]
---
# Growth SEO Fundamentals

## Summary

**One-sentence:** Three-pillar SEO baseline (Technical / On-Page / Off-Page) covering audit checklist, content optimisation by intent, and metric baseline — produces an audit checklist artefact.

**One-paragraph:** Three-pillar SEO baseline (Technical / On-Page / Off-Page) covering audit checklist, content optimisation by intent, and metric baseline — produces an audit checklist artefact. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Starting SEO from scratch on a new project OR diagnosing zero-organic-traffic on an existing one.
- Operator can run a Technical / On-Page / Off-Page audit with the URLs and analytics in hand.
- A named owner will fix each failed item before next audit cycle.
- Monthly reporting cadence is established (or being established this cycle).

## Skip If (ANY kills it)

- Deep schema / AEO work is the need — use `seo-techniques` instead.
- Link-building is the bottleneck — use `growth-seo-link-building` instead.
- PPC is the channel — `ppc-manager` instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Growth SEO Fundamentals task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/seo-content-brief.md` | Markdown SEO content brief: keyword data, SERP analysis, requirements, on-page details, internal links. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-seo-fundamentals.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[seo-manager/seo-basics]]
- [[seo-manager/growth-seo-link-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
