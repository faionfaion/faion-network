# VUI + IoT Integration

## Summary

Methodology for designing coherent voice control of smart home and IoT device ecosystems: command pattern taxonomy (direct control, scene activation, status query, conditional, scheduled), multi-device coordination flows, partial failure handling, and undo support. The core rule: always confirm multi-device actions verbally after execution, and handle partial failures gracefully rather than silently.

## Why

Smart home voice control fails most often at the seam between user intent and multi-device coordination: an "I'm leaving" command that locks doors but fails to arm security silently leaves the home insecure. Explicit confirmation after multi-device actions and graceful partial failure handling are the two most impactful design decisions.

## When To Use

- Designing VUI flows for smart home or IoT control applications
- Specifying voice command grammars for device ecosystems
- Auditing an existing smart home VUI for failure handling gaps
- Designing scene/routine naming and grouping for voice discoverability

## When NOT To Use

- IoT device firmware or protocol design (Matter, Zigbee) — hardware/protocol concerns, not VUI UX
- Enterprise IoT control systems — different use case and constraint set
- Single-device voice control with no multi-device coordination

## Content

| File | What's inside |
|------|---------------|
| `content/01-iot-vui-patterns.xml` | Command pattern taxonomy, multi-device coordination example, best practice rules, failure handling |

## Templates

none
