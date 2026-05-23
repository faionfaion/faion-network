---
slug: ph-maker-dm-template
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pre-launch maker DM outreach template with anti-spam guardrails — produces a per-target DM spec naming hook, ask, evidence, and follow-up cadence."
content_id: "fca0d16527ce75f7"
complexity: medium
produces: spec
est_tokens: 4900
tags: [marketing, solo, product-hunt, outreach, dm]
---
# PH Maker DM Template

## Summary

**One-sentence:** Pre-launch maker DM outreach template with anti-spam guardrails — produces a per-target DM spec naming hook, ask, evidence, and follow-up cadence.

**One-paragraph:** Pre-launch maker DM outreach template with anti-spam guardrails — produces a per-target DM spec naming hook, ask, evidence, and follow-up cadence. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- A Product Hunt launch is scheduled 14–28 days out.
- A hunter target list of 20–80 makers exists with signal per target (recent launch, comments, follow).
- A named owner will personally send each DM (not a VA).
- The product has a one-line wedge claim that survives a 280-char compression test.

## Skip If (ANY kills it)

- Target list is purchased or scraped without signal — DMs become spam regardless of template.
- Operator plans to mass-send identical DMs via automation — falls outside the rubric and risks PH/X bans.
- No launch is scheduled — DMs without a launch are just noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the PH Maker DM Template task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/maker-dm.md` | Markdown DM spec: hook line, ask line, evidence line, follow-up cadence, anti-spam guardrails. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ph-maker-dm-template.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[ph-launch-day-runbook]]
- [[outreach-personalization-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
