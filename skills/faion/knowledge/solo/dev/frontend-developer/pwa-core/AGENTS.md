# PWA Core

## Summary

A Progressive Web App requires three components: a Web App Manifest (`manifest.json` with stable
`id`, maskable icons, `display: standalone`), a Service Worker served from the origin root (not
`/static/`), and a registration module that defers the install prompt and shows an update
notification on `controllerchange`. Use Workbox for caching strategy — `NetworkFirst` for
navigation and API routes, `CacheFirst` for images and fonts, `StaleWhileRevalidate` for JS/CSS.

## Why

PWAs close the gap between web and native: offline tolerance, installability, push notifications,
and LCP gains from precaching the app shell — without an app store. `NetworkFirst` with a 3-second
timeout prevents the spinner-of-death on flaky networks while keeping data fresh. Workbox handles
service worker lifecycle (install, activate, update) so manual cache management is not needed.

## When To Use

- Web app needs offline tolerance, install prompt, push notifications, or "add to home screen."
- One codebase targeting desktop, Android, and iOS without an app store.
- Caching layer must survive flaky networks (transit, kiosk, captive Wi-Fi).
- Content/marketing site needing LCP/INP wins from precaching critical assets.

## When NOT To Use

- iOS-first product where push, background sync, and persistent storage limits block the use case.
- Hard real-time apps (live trading, video conferencing) — SW cache-coherence headaches, no upside.
- Highly regulated UI (banking transactions) where stale cache is a compliance risk.
- App requiring deep OS integration (Bluetooth, full camera, contacts) unreachable on iOS PWA.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Rules: serve SW from origin root, no-cache headers, maskable icons, stable manifest id, update flow. |
| `content/02-patterns.xml` | Manifest JSON, Workbox service worker, registration hook, install prompt hook. |

## Templates

| File | Purpose |
|------|---------|
| `templates/manifest.json` | Full manifest with icons (all sizes), shortcuts, screenshots, stable id. |
| `templates/service-worker.ts` | Workbox SW: precache, NavigationRoute, API/image/font/static strategies, offline fallback. |
| `templates/pwa-smoke.ts` | Playwright smoke test: SW registration + offline navigation + manifest reachability. |
