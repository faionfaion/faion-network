---
slug: pwa-core
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A Progressive Web App requires three components: a Web App Manifest (manifest.
content_id: "33e3d1eac5702f51"
tags: [pwa, service-worker, offline, web-app-manifest, workbox]
---
# PWA Core Architecture

## Summary

**One-sentence:** A Progressive Web App requires three components: a Web App Manifest (manifest.

**One-paragraph:** A Progressive Web App requires three components: a Web App Manifest (manifest.json with stable id, maskable icons, display: standalone), a Service Worker served from the origin root (not /static/), and a registration module that defers the install prompt and shows an update notification on controllerchange. Use Workbox for caching strategy — NetworkFirst for navigation and API routes, CacheFirst for images and fonts, StaleWhileRevalidate for JS/CSS.

## Applies If (ALL must hold)

- Web app needs offline tolerance, install prompt, push notifications, or "add to home screen."
- One codebase targeting desktop, Android, and iOS without an app store.
- Caching layer must survive flaky networks (transit, kiosk, captive Wi-Fi).
- Content/marketing site needing LCP/INP wins from precaching critical assets.

## Skip If (ANY kills it)

- iOS-first product where push, background sync, and persistent storage limits block the use case.
- Hard real-time apps (live trading, video conferencing) — SW cache-coherence headaches, no upside.
- Highly regulated UI (banking transactions) where stale cache is a compliance risk.
- App requiring deep OS integration (Bluetooth, full camera, contacts) unreachable on iOS PWA.

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

- parent skill: `solo/dev/frontend-developer/`
