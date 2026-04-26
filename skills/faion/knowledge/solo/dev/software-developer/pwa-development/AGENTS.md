# PWA Development

## Summary

Methodology for turning a web app into an installable Progressive Web App with offline
capability via Workbox service workers, a compliant Web App Manifest, and a user-driven
install/update prompt. Core rule: default to `registerType: 'prompt'` — never silent
`skipWaiting()` for app shells with in-flight state; ship a working `offline.html` from day one.

## Why

PWAs combine the reach of the web with near-native install and offline UX. Service-worker bugs
are sticky — clients can be locked on a broken SW for weeks — so the update handshake must be
explicit and tested. Workbox's per-resource caching strategies (NetworkFirst for APIs,
CacheFirst for images) prevent stale data from killing freshness.

## When To Use

- Adding installability and offline support to an existing SPA
- Mobile-first apps where skipping the App Store gate is valuable
- Content sites needing fast repeat-visit loads via precaching
- Apps needing push notifications without a native rewrite
- Internal tools that must feel native on field devices and survive flaky networks

## When NOT To Use

- Background-heavy apps needing native features (Bluetooth LE, geofencing, CallKit)
- iOS-first products where push and install UX still lag (iOS Web Push only since 16.4)
- Static marketing sites with low return rate — SW cost outweighs benefit
- Apps requiring exact filesystem access, USB/HID, or low-level audio — use Capacitor/Tauri
- Single-session tools (one-time forms) where caching adds risk without payoff

## Content

| File | What's inside |
|------|---------------|
| `content/01-manifest-sw.xml` | Web App Manifest fields, Workbox caching strategies, SW registration |
| `content/02-install-update.xml` | Install prompt hook, update notification, vite-plugin-pwa config |

## Templates

| File | Purpose |
|------|---------|
| `templates/manifest.json` | Complete Web App Manifest with required fields and icon sizes |
| `templates/vite-pwa-config.ts` | Minimal Vite PWA plugin config with NetworkFirst API caching |
