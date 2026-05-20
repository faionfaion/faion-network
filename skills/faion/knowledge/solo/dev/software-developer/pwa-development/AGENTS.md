---
slug: pwa-development
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for turning a web app into an installable Progressive Web App with offline capability via Workbox service workers, a compliant Web App Manifest, and a user-driven install/update prompt.
content_id: "f0d906087eec25c3"
tags: [pwa, service-worker, offline, web-app, installability]
---
# PWA Development

## Summary

**One-sentence:** Methodology for turning a web app into an installable Progressive Web App with offline capability via Workbox service workers, a compliant Web App Manifest, and a user-driven install/update prompt.

**One-paragraph:** Methodology for turning a web app into an installable Progressive Web App with offline capability via Workbox service workers, a compliant Web App Manifest, and a user-driven install/update prompt. Core rule: default to registerType: 'prompt' — never silent skipWaiting() for app shells with in-flight state; ship a working offline.html from day one.

## Applies If (ALL must hold)

- Adding installability and offline support to an existing SPA
- Mobile-first apps where skipping the App Store gate is valuable
- Content sites needing fast repeat-visit loads via precaching
- Apps needing push notifications without a native rewrite
- Internal tools that must feel native on field devices and survive flaky networks

## Skip If (ANY kills it)

- Background-heavy apps needing native features (Bluetooth LE, geofencing, CallKit)
- iOS-first products where push and install UX still lag (iOS Web Push only since 16.4)
- Static marketing sites with low return rate — SW cost outweighs benefit
- Apps requiring exact filesystem access, USB/HID, or low-level audio — use Capacitor/Tauri
- Single-session tools (one-time forms) where caching adds risk without payoff

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

- parent skill: `solo/dev/software-developer/`
