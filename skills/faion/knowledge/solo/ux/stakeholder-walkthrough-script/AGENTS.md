---
slug: stakeholder-walkthrough-script
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 60-minute stakeholder design walkthrough opens with a single decision-ask, presents options not artefacts, parks off-scope, and closes with a signed decision line — short-circuits the demo-mode pretty-pictures trap.
content_id: "2c439e5f1c4b949c"
complexity: medium
produces: report
est_tokens: 4200
tags: ["stakeholder", "walkthrough", "facilitation", "design-decision", "ux"]
---
# Stakeholder Walkthrough Script

## Summary

**One-sentence:** 60-minute stakeholder design walkthrough opens with a single decision-ask, presents options not artefacts, parks off-scope, and closes with a signed decision line — short-circuits the demo-mode pretty-pictures trap.

**One-paragraph:** Walkthroughs that present artefacts collect compliments; walkthroughs that ask for a decision get a decision. This script pins a 60-min format: 5 min framing (decision-ask + parking convention), 30 min options presentation (2-3 options with trade-offs, not finished designs), 15 min decision (signed-decision line), 10 min recap + park review. Off-scope ideas are parked via scope-creep-park-list. The decision is captured in design-decision-log.

**Ефективно для:**

- Solo designer running fortnightly stakeholder reviews who needs to extract decisions.
- PM facilitating cross-functional design review where decision velocity matters.
- AI agent generating walkthrough recap notes that must surface the signed decision.
- Pre-launch design freeze where every walkthrough must yield a binding decision.

## Applies If (ALL must hold)

- A design decision is required from ≥2 stakeholders in the next 7 days.
- Designer has ≥2 options shaped to a comparable level.
- A 60-min calendar slot is available with all decision-makers present.
- Decision can be logged in design-decision-log-template.

## Skip If (ANY kills it)

- Status update with no decision required — use async writeup instead.
- Single-stakeholder review — convert to a 1-1 instead.
- Brainstorm where options are not yet shaped — run brainstorm script first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision-ask statement | string | Walkthrough invite |
| 2-3 options + trade-offs | doc / Figma | Design canvas |
| Stakeholder roster + roles | list | Team directory |
| Parking-list template | template | scope-creep-park-list-template |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/scope-creep-park-list-template` | Parking ritual used during walkthrough. |
| `solo/ux/design-decision-log-template` | Signed decision goes into the log. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-decision-ask` | sonnet | Per-walkthrough judgement on framing. |
| `recap-script-execution` | haiku | Deterministic recap of options shown + signed decision. |
| `multi-stakeholder-prep` | opus | Cross-stakeholder synthesis for high-stakes reviews. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-walkthrough-script.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/stakeholder-walkthrough-script.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-walkthrough-script.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[scope-creep-park-list-template]]
- [[design-decision-log-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
