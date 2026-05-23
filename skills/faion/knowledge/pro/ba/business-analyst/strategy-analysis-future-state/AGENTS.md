---
slug: strategy-analysis-future-state
tier: pro
group: business-analyst
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defines the target to-be environment — processes, systems, capabilities, measurable outcomes, and design constraints — anchored to the business need and reachable from current state.
content_id: "e8aa99e4267a0b59"
complexity: medium
produces: spec
est_tokens: 2500
tags: [strategy-analysis, future-state, to-be, capability, outcome]
---
# Strategy Analysis — Future State

## Summary

**One-sentence:** A target to-be environment spec (processes, systems, capabilities, measurable outcomes) anchored to the business need and reachable from the current state.

**One-paragraph:** Future-state work is hand-waving without anchoring to (a) the business need, (b) reachability from current state. This methodology produces a to-be spec with: target processes, target systems, target capabilities, measurable outcomes per capability, and design constraints. Every outcome traces back to the business-need metric. Output feeds `strategy-analysis-gap-analysis` and `strategy-analysis-change-strategy`.

**Ефективно для:**

- Pre-RFP target operating model definition.
- Multi-quarter transformation programs needing a north-star artefact.
- Steering-committee approval requiring an outcome-anchored vision.
- Vendor evaluation requiring fit-against-future-state scoring.

## Applies If (ALL must hold)

- business-need spec exists and is current
- current-state spec exists (or is being produced in parallel)
- named decision-maker who can sign off the target
- outcomes are quantifiable from existing data

## Skip If (ANY kills it)

- business-need is undefined — produce it first
- purely tactical fixes — go to requirements
- future-state artefact already current (≤90 days) — refresh selectively

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| business-need spec | MD / wiki | strategy-analysis-business-need |
| current-state spec or parallel work in progress | MD / wiki | strategy-analysis-current-state |
| data source for outcome measurement | CSV / API | analytics / finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-analysis-business-need]] | Anchors every future-state outcome to a business metric. |
| [[strategy-analysis-current-state]] | Bounds reachability. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: every outcome traces to business need, measurable outcomes only, reachable from current state, named approver, no solution-vendor names | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for future-state spec: processes, systems, capabilities, outcomes, constraints | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: vendor-locked language, unmeasurable outcomes, unreachable jump, sponsor missing, drift from business need | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: anchor outcomes to need → define target capabilities → derive systems + processes → constrain → sign off | 700 |
| `content/05-examples.xml` | essential | Worked example: customer-onboarding to-be spec excerpt | 500 |
| `content/06-decision-tree.xml` | essential | Tree on need-clarity + measurability + reachability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `outcome_traceback` | sonnet | Trace each outcome to a business-need metric. |
| `capability_derivation` | sonnet | Derive capabilities supporting outcomes. |
| `reachability_check` | sonnet | Compare to current-state for reachability gaps. |
| `spec_assembly` | sonnet | Compile final spec. |

## Templates

| File | Purpose |
|------|---------|
| `templates/future-state-spec.md` | Markdown skeleton with all to-be sections. |
| `templates/outcome-traceback.csv` | Outcome → business-need metric mapping table. |
| `templates/_smoke-test.md` | Minimum viable future-state spec. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-analysis-future-state.py` | Validates future-state spec against the JSON Schema. | Before sponsor sign-off; pre-commit. |

## Related

- [[strategy-analysis-business-need]]
- [[strategy-analysis-current-state]]
- [[strategy-analysis-gap-analysis]]
- [[strategy-analysis-change-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
