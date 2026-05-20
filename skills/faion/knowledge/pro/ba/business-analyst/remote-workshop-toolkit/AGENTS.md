---
slug: remote-workshop-toolkit
tier: pro
group: business-analyst
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d0532d73b2c7e25e"
summary: Operating manual for remote and hybrid BA workshops — pre-reads, Miro/FigJam patterns, breakout protocol, time-zone splitting, on-camera ground rules, async pulses — so requirements work survives the lack of a shared room.
tags: [remote-workshop, business-analyst, facilitation, miro, figjam, hybrid]
---

# Remote Workshop Toolkit

## Summary

**One-sentence:** Concrete remote/hybrid workshop toolkit — pre-reads, Miro/FigJam canvases, breakout protocol, time-zone splitting, async pulses — that replaces the implicit social affordances of a shared room.

**One-paragraph:** Most P4 BA engagements in 2024-2026 are remote or hybrid, yet generic facilitation methodology assumes an in-person room. This methodology pins the specific mechanics that compensate for what is missing online: structured async pre-reads (so live time is not spent on context), template Miro/FigJam canvases per workshop type (process-mapping, story-mapping, impact-mapping, event-storming), explicit breakout-room protocol with named timekeeper and read-out format, two-camera and one-camera ground rules to surface the silent participants, time-zone splitting for global stakeholder groups, and async pulse-checks between sessions. Mechanism: a workshop is treated as a series of async + sync touchpoints, not a single live event. Primary output: a facilitation run-book per workshop and a Miro/FigJam canvas instance, both reusable across engagements.

## Applies If (ALL must hold)

- workshop_format ∈ {fully_remote, hybrid (≥1 remote participant)}
- ≥5 stakeholders required for the workshop deliverable
- BA has authority to define the agenda and ground rules
- video/whiteboard tooling available (Zoom/Teams/Meet + Miro/FigJam/Mural)

## Skip If (ANY kills it)

- single-stakeholder requirements interview — use 1:1 interview methodology
- workshop is fully in-person with no remote tail — use in-person facilitation methodology
- the team has refused to use cameras AND refused to use a digital whiteboard — pre-condition fails; renegotiate before scheduling

## Prerequisites

- workshop objective stated as a deliverable (e.g. "agreed process map for order-to-cash"), not a topic
- stakeholder list with named roles, time zones, and language preferences
- pre-read draft (1-2 pages, NOT slides) circulated ≥48h before the live session
- whiteboard tool licence active for every attendee (not "viewer" only)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/stakeholder-analysis` | Stakeholder list shape and influence/interest grid feed the breakout grouping |
| `pro/ba/business-analyst/workshop-facilitation` | In-person facilitation primitives that this methodology adapts for remote |
| `pro/comms/hr-recruiter/inclusive-meeting-practices` | Quiet-participant patterns and language inclusivity |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pre-read floor, breakout protocol, camera policy, time-zone splitting, async pulse cadence | ~1000 |
| `content/02-output-contract.xml` | essential | Run-book schema, canvas template taxonomy, ground-rules block | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: lurker problem, hybrid asymmetry, canvas collapse, breakout disappearance, etc. | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pre_read_draft_from_brief` | sonnet | Bounded summarisation + framing |
| `breakout_grouping_proposal` | sonnet | Apply stakeholder grid; produce groups of 4-6 |
| `canvas_layout_for_workshop_type` | haiku | Template selection based on workshop type |
| `async_pulse_question_set` | haiku | 3-5 quick questions per pulse |
| `read_out_summary_synthesis` | sonnet | Combine breakout outputs into a single coherent read-out |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-read.md` | 1-2 page pre-read structure (context, objective, decisions needed, questions to noodle on) |
| `templates/miro-canvas-process-map.json` | Importable canvas for as-is/to-be process mapping |
| `templates/miro-canvas-story-map.json` | Story-map canvas (backbone + walking skeleton) |
| `templates/miro-canvas-event-storming.json` | Big-picture event-storming canvas |
| `templates/ground-rules.md` | Camera, mic, chat, hand-raise, breakout conventions |
| `templates/async-pulse.md` | 5-min Loom or written pulse questionnaire |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/breakout-allocator.py` | Reads stakeholder list + influence/interest grid, outputs 4-6 person breakouts with named facilitator | After agenda finalised, before invite sent |
| `scripts/time-zone-splitter.py` | Splits global cohort into 2 sessions covering ≥80% of participants in working hours | When stakeholder list spans ≥3 time zones |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodologies: `workshop-facilitation`, `stakeholder-analysis`, `requirements-elicitation`, `process-mapping`
- external: [Hyper Island toolkit](https://toolbox.hyperisland.com/) · [Liberating Structures](https://www.liberatingstructures.com/) · [Atlassian Team Playbook — Workshops](https://www.atlassian.com/team-playbook/plays)
