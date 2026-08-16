# Remote Workshop Toolkit

## Summary

**One-sentence:** Run-book for remote/hybrid BA workshops (pre-read floor, four-role breakouts, camera policy, time-zone split, async pulses) producing the workshop run-book + canvas templates + ground rules block.

**One-paragraph:** Operating manual for remote and hybrid BA workshops — pre-reads, Miro/FigJam patterns, breakout protocol, time-zone splitting, on-camera ground rules, async pulses — so requirements work survives the lack of a shared room. Each workshop produces a typed run-book object satisfying the output contract.

**Ефективно для:**

- Remote / hybrid workshops з лезом проти lurker problem.
- Cross-time-zone cohort з ≥3 zones — split або async relay.
- Canvas-collaboration workshops (process map, story map, event storming).
- Series workshops, де треба переносити pre-read floor + ground rules.

## Applies If (ALL must hold)

- Remote-only or hybrid BA workshop with ≥4 attendees.
- Distributed team across ≥3 time zones (need split or async relay).
- Process / requirements work where canvas collaboration is the deliverable.
- Workshop with mixed stakeholder groups (sponsor + operator + engineering).
- Series of workshops sharing pre-read floor and ground rules.

## Skip If (ANY kills it)

- Single-room workshop where everyone is co-located.
- 1:1 interview — use elicitation-techniques instead.
- Decision meeting — use decision-analysis.
- Ad-hoc 30-min sync — overhead unjustified.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Workshop objective | Markdown | BA / facilitator |
| Stakeholder grid | JSON | stakeholder-analysis |
| Canvas tool credentials | env | infra |
| Pre-read draft | Markdown | BA |
| Calendar slots | ics | scheduling |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/elicitation-techniques` | Workshop technique uses this toolkit. |
| `pro/ba/business-analyst/scope-creep-parking-lot-protocol` | Parking-lot canvas integrated for ad-hoc asks. |

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
| `pre_read_draft_from_brief` | sonnet | Bounded summarisation + framing. |
| `breakout_grouping_proposal` | sonnet | Apply stakeholder grid; produce groups of 4–6. |
| `canvas_layout_for_workshop_type` | haiku | Template selection by workshop type. |
| `async_pulse_question_set` | haiku | 3–5 quick questions per pulse. |
| `read_out_summary_synthesis` | sonnet | Combine breakout outputs into a coherent read-out. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-read.md.j2` | 1–2 page pre-read structure. |
| `templates/pre-read.md` | 1–2 page pre-read structure. Generated from `templates/pre-read.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/miro-canvas-process-map.json` | Importable canvas for as-is/to-be process mapping. |
| `templates/miro-canvas-story-map.json` | Story-map canvas (backbone + walking skeleton). |
| `templates/miro-canvas-event-storming.json` | Big-picture event-storming canvas. |
| `templates/ground-rules.md.j2` | Camera, mic, chat, hand-raise, breakout conventions. |
| `templates/ground-rules.md` | Camera, mic, chat, hand-raise, breakout conventions. Generated from `templates/ground-rules.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/async-pulse.md.j2` | 5-min Loom or written pulse questionnaire. |
| `templates/async-pulse.md` | 5-min Loom or written pulse questionnaire. Generated from `templates/async-pulse.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum filled-in run-book. |
| `templates/_smoke-test.md` | Minimum filled-in run-book. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-remote-workshop-toolkit.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[elicitation-techniques]]
- [[scope-creep-parking-lot-protocol]]
- [[decision-analysis]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/miro-canvas-process-map.json`

```json
{
  "example": {
    "workshop_id": "ws-2026-05-23-process-map",
    "objective": "Build to-be process map for invoice exception handling with sign-off-ready BPMN draft",
    "agenda": [
      {
        "block": "Opening",
        "duration_min": 10,
        "mode": "plenary",
        "deliverable": "ground-rules ack"
      }
    ],
    "pre_read": {
      "url": "https://wiki/ws/pre-read",
      "sent_at": "2026-05-21T09:00:00Z",
      "acknowledgement_threshold": 0.7,
      "acknowledgement_rate": 0.82
    },
    "ground_rules": {
      "camera_policy": "on for plenary",
      "mic_policy": "on in breakouts \u22646",
      "chat_use": "questions + side-notes",
      "hand_raise": "tool-native"
    },
    "breakouts": [
      {
        "facilitator": "BA",
        "timekeeper": "PM",
        "scribe": "Ops lead",
        "canvas_frame": "frame-1",
        "deliverable_definition": "exception path bpmn draft",
        "read_out_template": "3-bullet summary"
      }
    ],
    "canvas_links": [
      {
        "tool": "miro",
        "url": "https://miro/abc",
        "template_id": "process-map"
      }
    ],
    "time_zones": {
      "zones": [
        "UTC+1",
        "UTC-5"
      ],
      "working_hours_coverage_pct": 0.85,
      "split_decision": "single session"
    },
    "async_pulses": [
      {
        "window": "T-24h",
        "questions": [
          "What is the worst exception you saw last month?"
        ],
        "response_rate_threshold": 0.6
      }
    ],
    "decision_log": []
  }
}
```

### `templates/miro-canvas-story-map.json`

```json
{
  "example": {
    "workshop_id": "ws-2026-05-23-process-map",
    "objective": "Build to-be process map for invoice exception handling with sign-off-ready BPMN draft",
    "agenda": [
      {
        "block": "Opening",
        "duration_min": 10,
        "mode": "plenary",
        "deliverable": "ground-rules ack"
      }
    ],
    "pre_read": {
      "url": "https://wiki/ws/pre-read",
      "sent_at": "2026-05-21T09:00:00Z",
      "acknowledgement_threshold": 0.7,
      "acknowledgement_rate": 0.82
    },
    "ground_rules": {
      "camera_policy": "on for plenary",
      "mic_policy": "on in breakouts \u22646",
      "chat_use": "questions + side-notes",
      "hand_raise": "tool-native"
    },
    "breakouts": [
      {
        "facilitator": "BA",
        "timekeeper": "PM",
        "scribe": "Ops lead",
        "canvas_frame": "frame-1",
        "deliverable_definition": "exception path bpmn draft",
        "read_out_template": "3-bullet summary"
      }
    ],
    "canvas_links": [
      {
        "tool": "miro",
        "url": "https://miro/abc",
        "template_id": "process-map"
      }
    ],
    "time_zones": {
      "zones": [
        "UTC+1",
        "UTC-5"
      ],
      "working_hours_coverage_pct": 0.85,
      "split_decision": "single session"
    },
    "async_pulses": [
      {
        "window": "T-24h",
        "questions": [
          "What is the worst exception you saw last month?"
        ],
        "response_rate_threshold": 0.6
      }
    ],
    "decision_log": []
  }
}
```

### `templates/miro-canvas-event-storming.json`

```json
{
  "example": {
    "workshop_id": "ws-2026-05-23-process-map",
    "objective": "Build to-be process map for invoice exception handling with sign-off-ready BPMN draft",
    "agenda": [
      {
        "block": "Opening",
        "duration_min": 10,
        "mode": "plenary",
        "deliverable": "ground-rules ack"
      }
    ],
    "pre_read": {
      "url": "https://wiki/ws/pre-read",
      "sent_at": "2026-05-21T09:00:00Z",
      "acknowledgement_threshold": 0.7,
      "acknowledgement_rate": 0.82
    },
    "ground_rules": {
      "camera_policy": "on for plenary",
      "mic_policy": "on in breakouts \u22646",
      "chat_use": "questions + side-notes",
      "hand_raise": "tool-native"
    },
    "breakouts": [
      {
        "facilitator": "BA",
        "timekeeper": "PM",
        "scribe": "Ops lead",
        "canvas_frame": "frame-1",
        "deliverable_definition": "exception path bpmn draft",
        "read_out_template": "3-bullet summary"
      }
    ],
    "canvas_links": [
      {
        "tool": "miro",
        "url": "https://miro/abc",
        "template_id": "process-map"
      }
    ],
    "time_zones": {
      "zones": [
        "UTC+1",
        "UTC-5"
      ],
      "working_hours_coverage_pct": 0.85,
      "split_decision": "single session"
    },
    "async_pulses": [
      {
        "window": "T-24h",
        "questions": [
          "What is the worst exception you saw last month?"
        ],
        "response_rate_threshold": 0.6
      }
    ],
    "decision_log": []
  }
}
```
