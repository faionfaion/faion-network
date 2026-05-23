---
slug: brainstorming-techniques
tier: solo
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a facilitated brainstorm session plan (Classic, 6-3-5, Round Robin, or Reverse) with Osborn's 4 rules enforced and a scored idea shortlist.
content_id: "3ec5dd38eb03f9d3"
complexity: medium
produces: spec
est_tokens: 4200
tags: [brainstorming, facilitation, ideation, 6-3-5, osborn]
---
# Brainstorming Techniques

## Summary

**One-sentence:** Generates a facilitated brainstorm session plan (Classic, 6-3-5, Round Robin, or Reverse) with Osborn's 4 rules enforced and a scored idea shortlist.

**One-paragraph:** Brainstorming techniques structure group ideation to maximize quantity and diversity of ideas while preventing dominant voices and premature evaluation. Four core techniques — Classic (open verbal, 4-8 people), Brainwriting 6-3-5 (written rotation, 6 people, 108 ideas in 30 min), Round Robin (enforced equal turns, 4-10 people), Reverse Brainstorming (invert the problem) — all follow Osborn's 4 rules: defer judgment, go for quantity, encourage wild ideas, build on others'. The methodology emits a session plan, a generation prompt, and a clustering/scoring sheet.

**Ефективно для:**

- Facilitated group ideation where dominant voices kill diversity.
- Time-boxed product-team workshops needing >50 ideas in 30 min.
- Surfacing risks via Reverse Brainstorming before a launch.
- Mixed-seniority groups where rank-anchoring kills junior input.

## Applies If (ALL must hold)

- Group of 4-10 participants available for a synchronous session.
- Problem statement is open-ended enough for >20 candidate ideas.
- Facilitator has 30-60 min uninterrupted to run the session.
- Output is meant to be clustered and shortlisted, not selected live.

## Skip If (ANY kills it)

- Solo ideation — use `ideation-methods` (SCAMPER, Mind Mapping) instead.
- Group already has 2+ candidate options and needs evaluation, not generation.
- Single decision-maker present who will override the group — pointless theatre.
- Async-only context — use brainwriting-by-doc instead of synchronous brainstorm.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement | single sentence, open-ended | facilitator / PM |
| Participant list | 4-10 names + roles | session owner |
| Tool | whiteboard / Miro / FigJam / paper | logistics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-communication]] | mode-selection — Brainstorm is one of the 5 dialogue modes |
| [[ideation-methods]] | fallback for solo or follow-up structured ideation |

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
| `technique-selection` | sonnet | Light judgement on group + problem fit. |
| `session-plan-generation` | sonnet | Phase planning + time-boxing. |
| `dedup-cluster` | haiku | Mechanical similarity grouping. |
| `score-impact-effort` | sonnet | Calibration judgement, bounded inputs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-generate.txt` | Prompt to run the generation phase for a chosen technique |
| `templates/prompt-cluster.txt` | Prompt to dedup + cluster a raw idea list into 3-7 themes |
| `templates/session-plan.md` | Markdown session plan skeleton with Osborn's 4 rules pre-printed |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-brainstorming-techniques.py` | Validate brainstorming-techniques artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[ideation-methods]]
- [[brainstorming-ideation]]
- [[stakeholder-communication]]
- [[feedback]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts with problem shape (generate vs risk-surface), then routes by group profile (dominance risk, written comfort) to one of the four techniques.
