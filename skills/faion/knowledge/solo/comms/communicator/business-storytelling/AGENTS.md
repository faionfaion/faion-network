---
slug: business-storytelling
tier: solo
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Pyramid / SCQA / Pixar structured narrative (exec summary, case study, or presentation outline) that puts the answer first and survives the 'so what' test.
content_id: "cf04ae9136adc11d"
complexity: medium
produces: spec
est_tokens: 4200
tags: [storytelling, pyramid, scqa, pixar, exec-summary]
---
# Business Storytelling

## Summary

**One-sentence:** Generates a Pyramid / SCQA / Pixar structured narrative (exec summary, case study, or presentation outline) that puts the answer first and survives the 'so what' test.

**One-paragraph:** Business storytelling is the discipline of structuring persuasive communication so the audience grasps the point immediately and remembers it. Three primary frameworks: Pyramid Principle (lead with answer, support with MECE arguments), SCQA (Situation-Complication-Question-Answer for narrative tension), Pixar (causal because-of-that chain for change stories). The methodology emits one of three artefacts — an executive summary, a case study, or a presentation outline — each obeying answer-first ordering and the so-what test on every claim.

**Ефективно для:**

- Executive summaries that lose readers in the second paragraph.
- Case studies that bury the outcome below 500 words of context.
- Investor decks where the story arc collapses into a feature list.
- Internal memos pitching a strategic shift.

## Applies If (ALL must hold)

- Audience is busy (executive, investor, customer in evaluation mode).
- Message must survive being read in 30 seconds.
- There is one central claim, not a status report.
- A 'so what' implication exists for every supporting fact.

## Skip If (ANY kills it)

- Status report — use Pyramid only if a decision is implied; otherwise plain bullets work.
- Technical reference doc — engineering reference is structured by API, not narrative.
- Reactive support reply — no narrative arc needed.
- Internal Slack thread of < 3 sentences.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Audience profile | role + decision they own + time budget | session owner |
| Central claim | one sentence | author |
| Evidence list | facts + sources | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[selling-ideas]] | pairs with SPIN for live pitches |
| [[storytelling]] | sister methodology focused on narrative structure |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `framework-selection` | sonnet | Judgement on audience + message-type fit. |
| `draft-supports` | sonnet | MECE structuring requires judgement. |
| `so-what-pass` | haiku | Mechanical: append implication to each fact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/executive-summary.txt` | Pyramid-structured executive summary skeleton |
| `templates/case-study.txt` | Pyramid case-study skeleton with outcome-first headline |
| `templates/presentation-outline.txt` | SCQA / Pixar presentation outline skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-business-storytelling.py` | Validate business-storytelling artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[storytelling]]
- [[selling-ideas]]
- [[stakeholder-communication]]
- [[feedback]]

## Decision tree

See `content/06-decision-tree.xml`. Routes by message type (decision / change / case-study) and the presence of a causal chain to a framework, each leaf referencing a rule from 01-core-rules.xml.
