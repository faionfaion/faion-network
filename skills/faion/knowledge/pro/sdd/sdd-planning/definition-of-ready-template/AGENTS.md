---
slug: definition-of-ready-template
tier: pro
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Seven-item Definition of Ready checklist that gates whether a story enters the sprint: AC quality, design link, dependency check, capacity reality-check, named PO + owner, success metric, NFR coverage."
content_id: "427428d6138c0977"
complexity: medium
produces: checklist
est_tokens: 4200
tags: ["dor", "scrum", "sprint-planning", "checklist", "sdd", "pro"]
---
# Definition of Ready Template

## Summary

**One-sentence:** Seven-item Definition of Ready checklist that gates whether a story enters the sprint: AC quality, design link, dependency check, capacity reality-check, named PO + owner, success metric, NFR coverage.

**One-paragraph:** Backlog grooming exists in most teams; the DoR GATE -- the explicit checkpoint a story MUST pass before being pulled into the sprint -- usually does not. Without it, planning pulls half-baked tickets and the team burns 20-40% of sprint capacity on clarification rounds and rework. This methodology defines the seven binary gates: AC pass against a rubric, design link if UI-touching, dependency check (no upstream blockers), capacity reality-check (effort estimate fits remaining sprint room), named PO + owner, declared success metric, NFR coverage. Output is a per-story DoR record + a sprint-level 'ready set' snapshot before planning.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «definition of ready template» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- team uses Scrum / Kanban with sprint commitments OR a similar batched-commitment model.
- team has a defined Product Owner role OR an analogous decision-maker for story scope.
- stories cross >1 role (e.g. design + dev) before being shippable.

## Skip If (ANY kills it)

- continuous-flow team with no sprint commitment (pure Kanban with no batching).
- single-person team where DoR collapses to a self-check.
- research-only team where 'story' is not the unit of work.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Definition of Ready Template task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/definition-of-done-template` | DoD is the sibling exit-gate; the two compose into a full sprint contract. |
| `pro/sdd/spike-protocol-template` | spikes use a relaxed DoR that this methodology references. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
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
| `templates/dor-checklist.md` | Seven-item DoR checklist + sprint-level ready-set snapshot. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-definition-of-ready-template.py` | Validate the checklist artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[definition-of-done-template]]
- [[spike-protocol-template]]
- [[agents-md-for-receiving-team]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
