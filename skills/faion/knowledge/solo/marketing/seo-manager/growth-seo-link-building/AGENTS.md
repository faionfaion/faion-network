---
slug: growth-seo-link-building
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Off-page link-building methodology covering target qualification, outreach cadence, anchor-text diversity, and toxic-link audit — produces a link-building campaign checklist."
content_id: "faaef1247d7e9e4a"
complexity: medium
produces: checklist
est_tokens: 4900
tags: [marketing, solo, seo, link-building, off-page]
---
# Growth SEO Link Building

## Summary

**One-sentence:** Off-page link-building methodology covering target qualification, outreach cadence, anchor-text diversity, and toxic-link audit — produces a link-building campaign checklist.

**One-paragraph:** Off-page link-building methodology covering target qualification, outreach cadence, anchor-text diversity, and toxic-link audit — produces a link-building campaign checklist. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- On-page SEO is already passing baseline (`growth-seo-fundamentals` checklist green).
- Target list of 50–200 candidate sites exists with relevance + authority signal.
- A named owner will run outreach and log every reply / placement.
- Backlink monitoring tool (Ahrefs / SEMrush / GSC) is connected and authoritative.

## Skip If (ANY kills it)

- On-page issues unresolved — links do not save a broken on-page foundation.
- Operator wants to buy links — out of scope; the methodology refuses paid-link patterns.
- Site is in a sandboxed / penalised state — fix penalty first, then build links.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Growth SEO Link Building task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/link-building-checklist.md` | Markdown checklist: target qualification, outreach drafts, anchor-text mix, toxic-link audit cadence. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-seo-link-building.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[seo-manager/growth-seo-fundamentals]]
- [[outreach-personalization-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
