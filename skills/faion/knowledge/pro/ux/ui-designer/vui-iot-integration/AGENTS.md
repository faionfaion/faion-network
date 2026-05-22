---
slug: vui-iot-integration
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for designing coherent voice control of smart home and IoT device ecosystems: command pattern taxonomy (direct control, scene activation, status query, conditional, scheduled), multi-device coordination flows, partial failure handling, and undo support.
content_id: "af7ec57e9fdaa2ec"
tags: [voice-iot, smart-home, voice-control, iot-design]
---
# VUI + IoT Integration

## Summary

**One-sentence:** Methodology for designing coherent voice control of smart home and IoT device ecosystems: command pattern taxonomy (direct control, scene activation, status query, conditional, scheduled), multi-device coordination flows, partial failure handling, and undo support.

**One-paragraph:** Methodology for designing coherent voice control of smart home and IoT device ecosystems: command pattern taxonomy (direct control, scene activation, status query, conditional, scheduled), multi-device coordination flows, partial failure handling, and undo support. The core rule: always confirm multi-device actions verbally after execution, and handle partial failures gracefully rather than silently.

## Applies If (ALL must hold)

- Designing VUI flows for smart home or IoT control applications
- Specifying voice command grammars for device ecosystems
- Auditing an existing smart home VUI for failure handling gaps
- Designing scene/routine naming and grouping for voice discoverability

## Skip If (ANY kills it)

- IoT device firmware or protocol design (Matter, Zigbee) — hardware/protocol concerns, not VUI UX
- Enterprise IoT control systems — different use case and constraint set
- Single-device voice control with no multi-device coordination

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

- parent skill: `pro/ux/ui-designer/`
