---
slug: 30-60-90-day-plan
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Three-phase new-hire ramp (Learn / Contribute / Execute) with observable milestones anchored to real team work, co-authored on Day 1.
content_id: "3bf3d9ed7359780b"
complexity: medium
produces: spec
est_tokens: 5000
tags: [onboarding, 30-60-90, ramp, performance-management, hr]
---
# 30-60-90 Day Plan

## Summary

**One-sentence:** Three-phase new-hire ramp (Learn / Contribute / Execute) with observable milestones anchored to real team work, co-authored on Day 1.

**One-paragraph:** Three-phase new-hire ramp (Learn / Contribute / Execute) with observable milestones anchored to real team work, co-authored on Day 1. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- новий найм у роль з measurable project deliverables.
- internal transfer чи promotion з суттєвою зміною scope.
- ramp анкорований на observable artifacts (PR, doc, deal), не на «understand».
- co-authoring з hiring manager + hire на Day 1, не HR-only.
- day-25 / 55 / 85 reviews → 5-day correction window перед формальним gate.

## Applies If (ALL must hold)

- new hire onboarding for any role with measurable project deliverables (engineer, sales rep, PM, marketer).
- internal transfers and promotions where role scope changes substantially.
- re-orgs where leaders need a structured first quarter against new mandates.
- drafting role-specific milestones during offer close to set explicit expectations.

## Skip If (ANY kills it)

- hourly or shift roles where competency comes from training scripts.
- sub-30-day contracts where the three-phase cadence does not fit.
- roles where outcomes depend wholly on team output — use team-level OKRs instead.
- externally mandated apprenticeship curricula (medical residency, regulated trades).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/30-60-90-day-plan.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-30-60-90-day-plan.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[onboarding]]
- [[onboarding-30-day]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
