---
slug: solo-lead-qualification-rubric
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces an ICE-style qualification score per lead (budget + authority + timeline + history) replacing BANT for one-person services."
content_id: "fc5c4fc1c0c6b35b"
complexity: medium
produces: rubric
est_tokens: 4900
tags: ["lead-qualification", "freelance", "discovery-call", "ice-score", "pipeline", "solo"]
---
# Solo Lead Qualification Rubric

## Summary

**One-sentence:** Produces an ICE-style qualification score per lead (budget + authority + timeline + history) replacing BANT for one-person services.

**One-paragraph:** Solo freelancers waste discovery time on no-budget leads or get scarred by serial contractor-churn clients. This methodology pins an ICE-style rubric tuned to solo signals: 4 axes (budget clarity / decision authority on call / sane timeline / no scarring contractor history), each scored 0-3, no-budget auto-decline, authority confirmed on call (not assumed from title), and an explicit scar flag for triage. Output: a lead qualification score artefact per lead.

**Ефективно для:**

- готова основа для повторюваної задачі «solo-lead-qualification-rubric» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator runs ≥1 discovery call per week.
- Operator can decline leads (not desperate for every closeable deal).
- Pipeline tracking surface exists (CRM / spreadsheet / Notion).

## Skip If (ANY kills it)

- Operator is in launch mode and cannot afford to decline any lead.
- Operator runs only fixed-fee productised services with no discovery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Lead intake fields | form / spreadsheet | intake |
| Discovery-call notes template | doc | operator |
| Pipeline tracking surface | Notion / sheet | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/conversion-optimizer/` | Parent role / operating context. |
| `solo/marketing/conversion-optimizer/testimonial-harvest-sop` | Post-engagement methodology for qualified-and-closed leads. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the lead-qualification-score artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/solo-lead-qualification-rubric.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/solo-lead-qualification-rubric.json` | lead-qualification-score JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-lead-qualification-rubric.py` | Validate the lead-qualification-score artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[testimonial-harvest-sop]]
- [[indie-mini-crm-notion]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
