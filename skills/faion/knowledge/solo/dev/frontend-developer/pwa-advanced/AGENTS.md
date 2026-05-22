---
slug: pwa-advanced
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced PWA features: Web Push (VAPID subscribe → server send via `web-push`), offline data sync (IndexedDB queue + Background Sync API + retry), and update management (skipWaiting with user-visible banner).
content_id: "75f6e4a5e024b73b"
tags: [pwa, web-push, vapid, service-worker, offline-sync, indexeddb]
---
# PWA Advanced Features

## Summary

**One-sentence:** Advanced PWA features: Web Push (VAPID subscribe → server send via `web-push`), offline data sync (IndexedDB queue + Background Sync API + retry), and update management (skipWaiting with user-visible banner).

**One-paragraph:** Advanced PWA features: Web Push (VAPID subscribe → server send via `web-push`), offline data sync (IndexedDB queue + Background Sync API + retry), and update management (skipWaiting with user-visible banner). Every async service worker handler must be wrapped in `event.waitUntil()`. Test with Playwright `context.setOffline(true)` on every PR.

## Applies If (ALL must hold)

- Adding Web Push notifications to a PWA (subscribe → store → server-send via VAPID).
- Building offline-first data sync with IndexedDB queue and Background Sync API + retry-with-backoff.
- Implementing Background Fetch / Periodic Background Sync for large downloads or refresh jobs.
- Hardening a PWA shell with advanced caching strategies (stale-while-revalidate, cache-first with network update, navigation preload).

## Skip If (ANY kills it)

- iOS Safari is the primary platform — Web Push works only on iOS 16.4+ from a home-screen-installed PWA; Background Sync and Periodic Sync are unsupported.
- Apps already running a native shell (Capacitor, Tauri, React Native) — use platform push (APNs / FCM) directly.
- Static marketing sites with no offline UX requirement — a basic precache from `pwa-core` is enough; advanced patterns add operational debt.

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
