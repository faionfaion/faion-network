---
slug: vui-iot-integration
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a smart-home voice-control spec with cohesive intent design, multi-device synchronization, explicit feedback for partial failures, undo support, and noise-robust testing for grouped scenes and routines.
content_id: "af7ec57e9fdaa2ec"
complexity: medium
produces: config
est_tokens: 4000
tags: [voice-ui, iot, smart-home, multi-device, voice-patterns]
---
# VUI + IoT Integration

## Summary

**One-sentence:** Produces a smart-home voice-control spec with cohesive intent design, multi-device synchronization, explicit feedback for partial failures, undo support, and noise-robust testing for grouped scenes and routines.

**One-paragraph:** Smart-home voice control requires more than per-device commands. Devices must be grouped logically (rooms, zones); scenes must have intuitive names; routines must give per-device action confirmation; partial failures must be surfaced explicitly ('lights on, thermostat unreachable'); undo must reverse the last action; and noise robustness (kitchen, TV) must be tested. This methodology emits a config consumed by Matter / Home Assistant / custom voice agents.

**Ефективно для:**

- Smart-home / IoT voice control спецификація.
- Grouping logic (rooms, zones, scenes) для багатопристроєвих команд.
- Partial-failure feedback design ('lights on, thermostat unreachable').
- Undo support для невипадкових (accidental) team-wide actions.

## Applies If (ALL must hold)

- Voice controls ≥2 physical devices in a household / facility.
- Devices span multiple manufacturers or protocols (Matter / Zigbee / WiFi).
- Audience expects scene + routine vocabulary, not just per-device commands.

## Skip If (ANY kills it)

- Single-device voice command (use voice-ui).
- Voice-only entertainment app without device control.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Device inventory | JSON / Matter graph | smart-home integrator |
| Group + scene definitions | Markdown | PM |
| Routine catalogue | list | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[voice-ui]] | intent + slot vocabulary upstream |
| [[vui-conversation-design]] | state-machine for multi-turn routines |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: logical-grouping-mandatory, scene-and-routine-names, partial-failure-feedback, undo-support, noise-robust-testing | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `group-devices` | haiku | Mechanical grouping. |
| `name-scenes` | sonnet | Natural-language naming. |
| `feedback-design` | sonnet | Per-device outcome wording. |

## Templates

| File | Purpose |
|------|---------|
| `templates/iot-voice-config.json` | Skeleton config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-iot-integration.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[voice-ui]]
- [[vui-conversation-design]]
- [[vui-privacy-security]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by device count and config completeness; enforces grouping + undo + partial-failure + noise-test. Each leaf cites a rule from `01-core-rules.xml`.
