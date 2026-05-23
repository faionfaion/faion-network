---
slug: spike-protocol-template
tier: pro
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Time-boxed investigation protocol with declared question, exit criteria, and outcome capture -- distinct from ADR (decision recorded) and design-doc (proposal)."
content_id: "98a371efe4c5cf75"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["spike", "investigation", "timebox", "sdd", "pro"]
---
# Spike Protocol Template

## Summary

**One-sentence:** Time-boxed investigation protocol with declared question, exit criteria, and outcome capture -- distinct from ADR (decision recorded) and design-doc (proposal).

**One-paragraph:** Time-boxed investigation tasks with explicit exit criteria are common in mature Scrum / Kanban teams but rarely templated. They are distinct from ADRs (which record a chosen decision) and design docs (which propose a path). This methodology defines the spike template: declared question + hypotheses + time-box + exit criteria + outcome (answer + recommended next action + ADR-or-not). Output is a 1-2 page spike record committed alongside the relevant PR or backlog story.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «spike protocol template» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- team uses Scrum / Kanban with iteration cadence OR similar batched commitment.
- the question is non-trivially unknown (>=2 hours of expected investigation).
- the answer will inform an upcoming decision (sprint, design, ADR).

## Skip If (ANY kills it)

- the question is a 30-minute look -- just answer it inline in the story.
- the team already has an ADR pending -- the investigation belongs inside that ADR's 'options considered' section.
- the question is research (academic-style open-ended) -- use research methodologies instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Spike Protocol Template task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/sdd-planning/definition-of-ready-template` | spikes use a relaxed DoR (no design link required) that the DoR methodology references. |
| `pro/sdd/definition-of-done-template` | spike DoD is 'question answered + outcome captured', not the standard story DoD. |

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
| `templates/spike.md` | Spike skeleton: question / timebox / exit criteria / outcome / next action. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spike-protocol-template.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[definition-of-ready-template]]
- [[definition-of-done-template]]
- [[decision-log-reconstruction-from-git]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
