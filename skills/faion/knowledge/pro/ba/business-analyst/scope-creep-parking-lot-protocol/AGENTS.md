---
slug: scope-creep-parking-lot-protocol
tier: pro
group: business-analyst
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d4a6826adc4f86af"
summary: Live-meeting protocol for absorbing client asks during demos and requirements reviews without litigating scope on the spot — capture in a structured parking lot, classify after the session, route per pre-agreed triage rules.
tags: [scope-creep, business-analyst, demo, parking-lot, facilitation, requirements-review]
---

# Scope Creep Parking Lot Protocol

## Summary

**One-sentence:** Live-meeting protocol that absorbs client asks during demos and requirements reviews — capture in a visible parking lot, classify and route after the meeting, never debate scope in front of stakeholders.

**One-paragraph:** Demos and requirements reviews are high-trust moments where clients raise new asks ("oh, while we are here, could it also do X?"). Litigating scope live damages the demo. Accepting silently invites creep. This protocol pins a live capture move (the BA writes the ask verbatim on a visible parking-lot canvas in front of the client), a post-meeting triage (within 24h, classify each item using the four-outcome routing from `scope-change-vs-scope-creep-detection`), and a closed-loop response (the requester receives a written reply per item within 48h). Mechanism: capture-not-judge in the moment; triage on schedule; respond explicitly. Primary output: a parking-lot artefact per session + a per-item response log. The protocol works in BA-led contexts (demos, requirements walks, sprint reviews) where the BA is the front-of-house but does not unilaterally accept scope.

## Applies If (ALL must hold)

- BA leads or co-facilitates live client sessions (demos, requirements reviews, sprint reviews, workshops)
- a signed scope baseline exists
- the team has authority to defer scope decisions to a triage process (not commit in the room)
- clients are typically engaged enough to raise asks during sessions

## Skip If (ANY kills it)

- meetings are async-only — use ticket-based intake instead
- BA has full authority to accept scope changes on the spot and the team accepts that — direct change-control is faster
- client culture is fully transactional (T&M, fixed-bid with frequent change-orders) — every ask becomes a change-order anyway

## Prerequisites

- signed scope baseline accessible during the meeting
- parking-lot canvas (physical flipchart, Miro frame, Notion page, or shared doc) prepared per session
- triage process exists (`pro/pm/project-manager/scope-change-vs-scope-creep-detection`)
- 24h SLA on triage and 48h SLA on requester response

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/scope-change-vs-scope-creep-detection` | Triage logic the parking lot feeds into |
| `pro/ba/business-analyst/client-demo-prep-and-run` | Demo facilitation context |
| `pro/ba/business-analyst/requirements-review-meeting-facilitation` | Review-meeting context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: verbatim capture, visible canvas, no-live-judgement, 24h triage SLA, 48h response SLA | ~1000 |
| `content/02-output-contract.xml` | essential | Parking-lot artefact schema, per-item response log, hand-off to triage | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: silent acceptance, BA-judges-in-room, parking-lot orphans, response drift, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `live_capture_transcription` | sonnet | Transcribe meeting audio into the parking-lot canvas in real time |
| `post_meeting_triage_handoff` | sonnet | Package parking-lot items for the classifier |
| `requester_response_draft` | sonnet | Draft the 48h response per item from the triage verdict |
| `weekly_parking_lot_rollup` | haiku | Aggregate counts and ageing |

## Templates

| File | Purpose |
|------|---------|
| `templates/parking-lot-canvas.md` | Markdown canvas with verbatim quote + requester + meeting context columns |
| `templates/requester-response.md` | 48h response template (acknowledge, classify, route, next step) |
| `templates/triage-handoff.yaml` | Schema bridge between parking lot and the classifier |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/parking-lot-to-triage.py` | Convert parking-lot canvas into triage-ready records | After meeting closes |
| `scripts/age-report.py` | Surface parking-lot items that exceed SLA | Daily |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodologies: `scope-change-vs-scope-creep-detection`, `client-demo-prep-and-run`, `requirements-review-meeting-facilitation`, `scope-drift-early-warning-metrics`
- external: [Atlassian Team Playbook — Parking Lot](https://www.atlassian.com/team-playbook/plays) · [BABOK v3 — requirements elicitation](https://www.iiba.org/standards-and-resources/babok/)
