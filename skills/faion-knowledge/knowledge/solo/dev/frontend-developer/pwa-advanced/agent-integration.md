# Agent Integration — PWA Advanced

## When to use
- Adding Web Push notifications to a PWA (subscribe → store → server-send via VAPID).
- Building offline-first data sync (IndexedDB queue + Background Sync API + retry-with-backoff).
- Implementing Background Fetch / Periodic Background Sync for large downloads or refresh jobs.
- Hardening a PWA shell with advanced caching strategies (stale-while-revalidate, cache-first with network update, navigation preload).

## When NOT to use
- iOS Safari is the primary platform — Web Push works only on iOS 16.4+ from a home-screen-installed PWA; Background Sync and Periodic Sync are unsupported.
- Apps already running a native shell (Capacitor, Tauri, React Native) — use platform push (APNs / FCM) directly.
- Static marketing sites with no offline UX requirement — a basic precache from `pwa-core` is enough; advanced patterns add operational debt.

## Where it fails / limitations
- VAPID key encoding: `urlBase64ToUint8Array` is the #1 source of "applicationServerKey is not a valid base64-encoded string" errors when keys contain `+`/`/`.
- Background Sync only fires when the browser deems network "reliable" — there is no guaranteed timing; tests must use `chrome://serviceworker-internals` or simulated triggers.
- Service worker updates: `skipWaiting()` + `clients.claim()` without a refresh banner causes data loss for users mid-edit.
- IndexedDB transactions auto-close on the first `await` of a non-IDB promise; agents routinely break this.
- Push payload encryption (`aes128gcm`) requires a server library (`web-push` for Node, `pywebpush` for Python) — rolling your own is a security footgun.

## Agentic workflow
Treat PWA-advanced work as three separable tracks: push (subscribe + send), offline sync (queue + replay), and update strategy (skipWaiting + UX). Run a subagent per track with a Playwright + `@playwright/test` PWA harness as the oracle. The agent must register the SW, force `update()`, simulate offline (`context.setOffline(true)`), and assert behavior — otherwise the human cannot tell if the change worked. Keep production VAPID keys human-controlled; let agents generate scratch keys for dev only.

### Recommended subagents
- `faion-feature-executor` — push notifications and offline sync are well-scoped tasks; sequential gates (build, lint, Playwright PWA tests) catch regressions.
- `faion-sdd-executor-agent` — when the work spans backend (push send service) + SW + UI, the SDD spec/design loop keeps it coherent.

### Prompt pattern
- "Implement Web Push subscription flow per `pwa-advanced/README.md`. Server side: Node Express handler that stores subscriptions and exposes `POST /api/push/send`. Use the `web-push` library with VAPID keys from env. Write a Playwright test that asserts the SW receives a push event."
- "Audit `service-worker.ts` against three failure modes: (1) IDB transaction await across non-IDB promise, (2) `skipWaiting` without update banner, (3) push handler missing `event.waitUntil`."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx web-push generate-vapid-keys` | Generate VAPID public/private pair | https://github.com/web-push-libs/web-push |
| `pnpm add idb` | Typed IndexedDB wrapper used in the README | https://github.com/jakearchibald/idb |
| `pnpm add -D workbox-cli` | Pre-built strategies + manifest gen + SW build | https://developer.chrome.com/docs/workbox/ |
| `npx lighthouse --preset=desktop --only-categories=pwa <url>` | Audit PWA install + offline + manifest | https://developer.chrome.com/docs/lighthouse/ |
| `npx pwa-asset-generator <logo> public/icons` | Generate maskable icons + splash screens | https://github.com/elegantapp/pwa-asset-generator |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OneSignal | SaaS | Yes (REST + SDK) | Push as a service; agents wire SDK + send via API token. Skip if you want zero vendor lock-in. |
| Pushwoosh / Knock | SaaS | Yes (REST) | Multi-channel (push + email + SMS) — useful when push extends to native apps later. |
| Firebase Cloud Messaging | SaaS | Yes (REST/SDK) | Most widely used; same VAPID-keyed Web Push under the hood for browsers. |
| `web-push` (Node), `pywebpush` (Py), `web_push` (Rust) | OSS | Yes | Self-host send infrastructure. |
| Workbox | OSS | Yes | Google's SW strategies library; `injectManifest` mode for custom logic. |

## Templates & scripts
See `templates.md` for SW push handler, offline-sync queue, and Background Sync registration. Minimal VAPID-key conversion utility (the breakpoint LLMs miss):

```ts
// lib/vapid.ts
export function urlBase64ToUint8Array(b64: string): Uint8Array {
  const pad = '='.repeat((4 - (b64.length % 4)) % 4);
  const norm = (b64 + pad).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(norm);
  const arr = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) arr[i] = raw.charCodeAt(i);
  return arr;
}
// Test: assert Uint8Array length is 65 for a P-256 public key.
```

## Best practices
- Always wrap async work in service worker handlers with `event.waitUntil(...)` — without it the browser may kill the SW before the work finishes.
- Store push subscriptions with a `userId` foreign key and a `createdAt`; expire stale ones on 410 Gone responses from the push service.
- For SW updates, ship a "new version available, reload" banner; never call `skipWaiting()` silently.
- Use `navigation preload` (`registration.navigationPreload.enable()`) for navigation requests to avoid the "wait for SW boot" latency hit.
- Test offline mode with Playwright (`context.setOffline(true)`) on every PR — manual DevTools checks regress within a sprint.
- Keep VAPID private key in a secrets manager; never commit it. Rotate on team changes.

## AI-agent gotchas
- Agents call `Notification.requestPermission()` on page load — Chrome and Safari heuristics will silently deny. Gate it behind a user gesture.
- LLMs commonly write `pushManager.subscribe({ userVisibleOnly: false })` for "silent push" — Chrome rejects this; only `true` is allowed for web.
- IDB code generated from memory uses `db.transaction(...).complete` (deprecated) instead of `tx.done` from `idb`.
- Agents forget to call `event.notification.close()` in `notificationclick`, leaving the notification visible after the user clicks.
- When asked to "register sync", agents use the wrong API (`SyncManager` vs `PeriodicSyncManager`); only Background Sync is one-shot, Periodic requires installed PWA + permission.
- HTTPS-only: agents test against `http://localhost` (works) and miss that staging on plain HTTP silently fails SW registration.

## References
- Web Push Protocol (RFC 8030) — https://datatracker.ietf.org/doc/html/rfc8030
- MDN Service Worker API — https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- `web-push` library — https://github.com/web-push-libs/web-push
- Workbox — https://developer.chrome.com/docs/workbox/
- Apple PWA Push (iOS 16.4+) — https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
