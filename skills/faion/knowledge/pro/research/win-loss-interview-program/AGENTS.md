---
slug: win-loss-interview-program
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Quarterly win/loss interview program with 50/50 sample frame, neutral-interviewer rule, evidence-anchored script, and three-channel synthesis to PM/marketing/sales."
content_id: "9a9c478f7e7dc721"
complexity: deep
produces: report
est_tokens: 4900
tags: ["win-loss", "interviews", "b2b-sales", "research", "pro"]
---
# Win-Loss Interview Program

## Summary

**One-sentence:** Quarterly win/loss interview program with 50/50 sample frame, neutral-interviewer rule, evidence-anchored script, and three-channel synthesis to PM/marketing/sales.

**One-paragraph:** Researcher methodologies cover user-interviews and problem-validation but not the specific structure of post-deal win/loss interviews. Sales-led B2B teams without this lose deals to invisible reasons and re-win them in vibes. This methodology defines the sample frame (50% won, 50% lost), the bias controls (interviewer != the rep who sold the deal), the script (open + evidence-anchored questions), the timing rule (within 30 days of close), and the quarterly synthesis that distributes findings to product, marketing, and sales. Output is a per-deal interview record plus a quarterly synthesis report with named pattern owners.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «win-loss interview program» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- sales-led B2B with >=10 deals/quarter closing won-or-lost.
- a named PM or researcher has authority to interview customers without sales gating each call.
- sales team can hand off won/lost contacts within 14 days of close.

## Skip If (ANY kills it)

- PLG self-serve product -- use churn-cohort analysis instead.
- <5 deals/quarter -- sample too small for pattern detection.
- sales leadership refuses to hand off lost contacts -- the org gap blocks the methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Win-Loss Interview Program task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent role/operating context. |
| `pro/research/researcher/user-research-at-scale` | supplies interview infrastructure (scheduling, recording, transcription). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/win-loss-script.md` | Interview script: 7 evidence-anchored questions + neutral-interviewer notes. |
| `templates/win-loss-synthesis.md` | Quarterly synthesis skeleton: 50/50 sample table + 3-channel actions. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-win-loss-interview-program.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[thematic-analysis]]
- [[service-blueprint]]
- [[wtp-survey-questionnaire]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
