---
slug: onboarding
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: End-to-end repeatable onboarding program: preboarding, Day 1 orientation, buddy pairing, 30-60-90 progression, feedback loops, manager guides, remote adaptations.
content_id: "760dc853263a24c3"
complexity: medium
produces: spec
est_tokens: 5000
tags: [onboarding, new-hire, employee-experience, retention, hr]
---
# Onboarding Program Design

## Summary

**One-sentence:** End-to-end repeatable onboarding program: preboarding, Day 1 orientation, buddy pairing, 30-60-90 progression, feedback loops, manager guides, remote adaptations.

**One-paragraph:** End-to-end repeatable onboarding program: preboarding, Day 1 orientation, buddy pairing, 30-60-90 progression, feedback loops, manager guides, remote adaptations. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- standing up repeatable onboarding program replacing tribal knowledge.
- hiring velocity ≥1 hire/week — ad-hoc diverges.
- rolling out remote-first onboarding де in-office Day-1 не translate.
- after 90-day retention drop or new-hire eNPS decline.
- M&A integration — два onboarding cultures convergence.

## Applies If (ALL must hold)

- standing up a repeatable onboarding program for the first time (replacing tribal knowledge).
- hiring velocity of one or more hires per week where ad-hoc approaches diverge.
- rolling out remote-first onboarding where in-office Day-1 rituals do not translate.
- after a 90-day-retention drop or new-hire eNPS decline.

## Skip If (ANY kills it)

- one or two hires per year — a checklist suffices; a full program is not worth the maintenance.
- C-suite or executive onboarding — bespoke, board-driven; this framework does not apply.
- contractor or agency placements under 90 days — limit to access provisioning and safety.
- crisis backfills replacing a critical departure — collapse into knowledge transfer.

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
| `templates/onboarding.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-onboarding.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[onboarding-30-day]]
- [[30-60-90-day-plan]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
