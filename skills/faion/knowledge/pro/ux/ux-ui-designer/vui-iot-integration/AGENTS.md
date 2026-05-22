---
slug: vui-iot-integration
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Smart home voice control requires cohesive intent design, multi-device synchronization, and explicit feedback for partial failures.
content_id: "af7ec57e9fdaa2ec"
tags: [voice-ui, iot, smart-home, multi-device, voice-patterns]
---
# VUI + IoT Integration

## Summary

**One-sentence:** Smart home voice control requires cohesive intent design, multi-device synchronization, and explicit feedback for partial failures.

**One-paragraph:** Smart home voice control requires cohesive intent design, multi-device synchronization, and explicit feedback for partial failures. Group devices logically, create intuitive scene names, provide action confirmation per routine, handle undo, and test under noisy conditions.

## Applies If (ALL must hold)

- Designing voice control flows for smart home, commercial IoT, or industrial automation.
- Authoring multi-device routines like "Goodnight", "Leaving", "Movie Mode" that fan out commands.
- Mapping natural language intents and utterances to device APIs (Matter, Home Assistant, SmartThings, Alexa, Google Home).
- Designing failure, partial-success, and undo behavior across heterogeneous device fleets.

## Skip If (ANY kills it)

- Pure visual app UI work where voice is not a channel — use core VUI design principles instead.
- Single-device, single-vendor remote control with no scene logic — manufacturer SDK is sufficient.
- Safety-critical automation (medical, alarm dispatch) — requires regulatory layer and domain expertise beyond VUI patterns.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ux/ux-ui-designer/`
