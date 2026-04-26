# PWA Advanced Features

## Summary

Advanced PWA features: Web Push (VAPID subscribe → server send via `web-push`), offline data sync (IndexedDB queue + Background Sync API + retry), and update management (skipWaiting with user-visible banner). Every async service worker handler must be wrapped in `event.waitUntil()`. Test with Playwright `context.setOffline(true)` on every PR.

## Why

Push notifications and offline sync are the two most-requested PWA capabilities beyond install + precache, and the two with the most LLM failure modes: VAPID key encoding errors, IDB transaction auto-close on non-IDB awaits, `skipWaiting()` causing silent data loss, and push permission gated behind page load instead of a user gesture.

## When To Use

- Adding Web Push notifications (subscribe flow + VAPID server send).
- Building offline-first data sync with IndexedDB queue and Background Sync API.
- Implementing Background Fetch or Periodic Background Sync for large downloads or refresh jobs.
- Hardening caching strategies (stale-while-revalidate, cache-first with network update, navigation preload).

## When NOT To Use

- iOS Safari is the primary platform: Web Push requires iOS 16.4+ installed PWA; Background Sync and Periodic Sync are unsupported.
- App runs in a native shell (Capacitor, Tauri, React Native) — use platform push (APNs/FCM) directly.
- Static marketing sites with no offline UX requirement — basic precache from `pwa-core` is enough.

## Content

| File | What's inside |
|------|---------------|
| `content/01-push-notifications.xml` | Subscribe flow, VAPID key encoding, push event handler, notificationclick handler, gotchas. |
| `content/02-offline-sync.xml` | IndexedDB schema (idb), request queue, sync replay, Background Sync registration, IDB await rule. |
| `content/03-update-strategy.xml` | skipWaiting + clients.claim banner pattern, navigation preload, update detection hook. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vapid-util.ts` | urlBase64ToUint8Array — canonical VAPID key converter with test assertion note. |

## Scripts

none
