---
slug: outreach-personalization-rubric
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Scoring rubric for outbound personalization — verbatim-anchor count, specificity, recency, evidence — produces a 0–10 score per message blocking AI-mass-mail-shaped sends."
content_id: "ce63f7cc1e0ea1e0"
complexity: medium
produces: rubric
est_tokens: 4900
tags: [marketing, solo, outreach, personalization, rubric]
---
# Outreach Personalization Rubric

## Summary

**One-sentence:** Scoring rubric for outbound personalization — verbatim-anchor count, specificity, recency, evidence — produces a 0–10 score per message blocking AI-mass-mail-shaped sends.

**One-paragraph:** Scoring rubric for outbound personalization — verbatim-anchor count, specificity, recency, evidence — produces a 0–10 score per message blocking AI-mass-mail-shaped sends. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator runs outbound (cold email, LinkedIn DM, X DM) at any volume above 5 messages / week.
- Each draft can be inspected before send (no auto-mass-send tool that bypasses review).
- A named owner is responsible for the campaign's reply-rate and bounce-rate metrics.
- Source-of-truth signals (LinkedIn profile, recent post, repo, podcast) for the recipient are accessible.

## Skip If (ANY kills it)

- Operator is running brand awareness blasts, not 1:1 outreach — different methodology.
- Tooling does not allow per-message inspection — fix the tool before applying the rubric.
- Recipient list is purchased / scraped without signal — personalization rubric does not save spam.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Outreach Personalization Rubric task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/personalization-rubric.md` | Markdown rubric with 5 scoring criteria, weight, evidence requirement, pass threshold. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-outreach-personalization-rubric.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[outreach-crm-minimal-schema]]
- [[reply-guy-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
