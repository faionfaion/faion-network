---
slug: scope-creep-park-list-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: One-page format used live in stakeholder design walkthroughs to capture 'wouldn't it be cool if' ideas without committing to them, with explicit owner, date, and revisit gate.
content_id: "315932eacb4ece49"
complexity: medium
produces: report
est_tokens: 4200
tags: ["scope-creep", "parking-lot", "walkthrough", "facilitation", "ux"]
---
# Scope-Creep Park List Template

## Summary

**One-sentence:** One-page format used live in stakeholder design walkthroughs to capture 'wouldn't it be cool if' ideas without committing to them, with explicit owner, date, and revisit gate.

**One-paragraph:** Stakeholder walkthroughs derail when off-scope ideas land mid-meeting. This template gives the facilitator a one-page format to acknowledge each idea, capture it as a parked row (owner + date + revisit-gate), and keep the meeting on the decision-ask. Park rows are reviewed at the next sprint planning; never silently ignored. The artefact prevents both demo-mode derailment and rude shutdown of stakeholders.

**Ефективно для:**

- Solo designer running stakeholder walkthroughs that keep getting derailed.
- PM facilitating a design review where senior stakeholders bring big ideas.
- AI agent generating walkthrough recap notes that must surface parked ideas.
- Pre-launch demo where scope must be frozen but stakeholder input is welcome.

## Applies If (ALL must hold)

- A stakeholder walkthrough is scheduled with ≥2 non-design participants.
- Scope for the current sprint is decided and must not expand mid-meeting.
- A backlog tool exists where parked rows can be revisited.
- Facilitator is willing to enforce parking instead of debating each idea.

## Skip If (ANY kills it)

- Brainstorm session — divergence is the goal, parking is counterproductive.
- Hard deadline + frozen scope + stakeholders briefed — parking ritual unnecessary.
- Single-stakeholder review with no derailment risk.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Walkthrough agenda + decision ask | doc | Walkthrough invite |
| Sprint scope statement | string | Roadmap / current sprint board |
| Backlog tool URL | URL | Sprint board |
| Facilitator handle | string | Designer / PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/stakeholder-walkthrough-script` | Script that calls out parking ritual. |
| `solo/ux/design-decision-log-template` | Parked-then-decided ideas graduate to the log. |

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
| `record-parked-idea` | sonnet | Per-idea judgement on capture and acknowledgement wording. |
| `weekly-park-review` | haiku | Deterministic age check + revisit-gate evaluation. |
| `scope-impact-audit` | opus | Cross-row pattern detection (e.g. 5 ideas pointing at one omission). |

## Templates

| File | Purpose |
|------|---------|
| `templates/scope-creep-park-list-template.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/scope-creep-park-list-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scope-creep-park-list-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[stakeholder-walkthrough-script]]
- [[design-decision-log-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
