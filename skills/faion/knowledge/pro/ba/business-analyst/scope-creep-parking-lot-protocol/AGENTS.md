---
slug: scope-creep-parking-lot-protocol
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Live-meeting protocol absorbing client asks (verbatim capture, visible canvas, no-live-judgement) with 24h triage SLA + 48h response SLA producing a triaged parking-lot artefact and response log.
content_id: "8e6bee9a28f9052f"
complexity: medium
produces: config
est_tokens: 4500
tags: [scope-creep, business-analyst, demo, parking-lot, facilitation, requirements-review]
---
# Scope Creep Parking Lot Protocol

## Summary

**One-sentence:** Live-meeting protocol absorbing client asks (verbatim capture, visible canvas, no-live-judgement) with 24h triage SLA + 48h response SLA producing a triaged parking-lot artefact and response log.

**One-paragraph:** Live-meeting protocol for absorbing client asks during demos and requirements reviews without litigating scope on the spot — capture in a structured parking lot, classify after the session, route per pre-agreed triage rules. Mechanism: verbatim quotes, visible canvas, the BA never judges in the room, 24h triage SLA via scope-change-vs-scope-creep-detection, 48h response SLA per item.

**Ефективно для:**

- Client demo з невпинним потоком ad-hoc asks.
- Distributed / hybrid sessions з visible canvas.
- Outsourced delivery — кожне ask може стати change.
- Регульований domain з conversation logs у change control.

## Applies If (ALL must hold)

- Client demo or requirements review where ad-hoc asks regularly fly.
- Distributed / hybrid sessions where capture must be visible.
- Programme with frequent client steering meetings.
- Outsourced delivery where every ask is a potential contract change.
- Regulated domain where conversation logs feed change control.

## Skip If (ANY kills it)

- Internal-only retros / planning where formal protocol overhead is unjustified.
- Tactical bug-triage standups.
- 1:1 conversations.
- Pre-existing parking-lot venue authoritative and integrated.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Meeting recording / transcript | MP3 / VTT | facilitator |
| Parking-lot canvas template | Markdown | templates/ |
| Triage rules | YAML | scope-change-vs-scope-creep-detection |
| Response template | Markdown | templates/ |
| Daily age-report scheduler | cron | engineering |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/requirements-lifecycle` | Triage outcomes flow into change-control. |
| `pro/ba/business-analyst/remote-workshop-toolkit` | Workshop integration with parking-lot canvas. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `live_capture_transcription` | sonnet | Transcribe meeting audio into canvas in real time. |
| `post_meeting_triage_handoff` | sonnet | Package parking-lot items for the classifier. |
| `requester_response_draft` | sonnet | Draft the 48h response from triage verdict. |
| `weekly_parking_lot_rollup` | haiku | Aggregate counts and ageing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/parking-lot-canvas.md` | Markdown canvas with verbatim quote + requester + meeting context columns. |
| `templates/requester-response.md` | 48h response template. |
| `templates/triage-handoff.yaml` | Schema bridge between parking lot and the classifier. |
| `templates/_smoke-test.md` | Minimum filled-in parking lot. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scope-creep-parking-lot-protocol.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[remote-workshop-toolkit]]
- [[requirements-lifecycle]]
- [[decision-analysis]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
