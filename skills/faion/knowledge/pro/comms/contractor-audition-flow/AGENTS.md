---
slug: contractor-audition-flow
tier: pro
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Paid-trial spec + scoring rubric + ramp-onto-real-client criteria + kill-criteria — a contractor-specific audition flow that does NOT run a 6-week W-2 interview funnel.
content_id: "0657efa9e59a3327"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: [contractor, audition, hiring, micro-agency, comms]
---
# Contractor Audition Flow

## Summary

**One-sentence:** Paid-trial spec + scoring rubric + ramp-onto-real-client criteria + kill-criteria — a contractor-specific audition flow that does NOT run a 6-week W-2 interview funnel.

**One-paragraph:** Paid-trial spec + scoring rubric + ramp-onto-real-client criteria + kill-criteria — a contractor-specific audition flow that does NOT run a 6-week W-2 interview funnel. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned playbook-step artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- micro-agency будує bench без перетворення на agency-of-agencies.
- paid trial task з типовими input/output, не «design exercise».
- scoring rubric з вагами, не «vibe».
- ramp criteria для real-client onboarding (не theatre).
- kill criteria за day-30 → охороняє margin замість sunk cost.

## Applies If (ALL must hold)

- task is 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' or close variant.
- operator has the artefacts named in Prerequisites available before starting.
- output will be consumed by a downstream agent or human reviewer (not discarded).
- tier == pro or higher (gating enforced by tier-manifest).

## Skip If (ANY kills it)

- team already maintains a working artefact for this gap — replace, do not duplicate.
- single-use throwaway hire — overhead of the contract is not justified.
- regulatory / compliance context overrides any in-methodology guidance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the playbook-step artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
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
| `templates/contractor-audition-flow.md` | Working playbook-step skeleton with 5-line header |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contractor-audition-flow.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[contractor-onboarding-runbook]]
- [[graceful-offboard-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
