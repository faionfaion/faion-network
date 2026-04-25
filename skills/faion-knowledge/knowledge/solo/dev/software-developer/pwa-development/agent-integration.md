# Agent Integration — PWA Development

## When to use
- Adding installability + offline support to an existing SPA (React/Vue/Svelte/Angular)
- Mobile-first apps where you want to skip the App Store / Play Store gate
- Content sites that need fast repeat-visit loads (precaching, runtime caching)
- Apps needing push notifications without native rewrite
- Internal tools that should "feel native" on field devices and survive flaky networks

## When NOT to use
- Background-heavy apps needing long-running native features (Bluetooth LE central, geofencing, CallKit) — fall back to native
- iOS-first products where push and install UX still lag (iOS supports Web Push only since 16.4 and only after install)
- Static marketing sites with low return rate — service worker cost outweighs benefit
- Apps requiring exact filesystem access, USB/HID, or low-level audio — Capacitor/Tauri/Electron fits better
- Single-session tools (e.g., one-time forms) where caching adds risk without payoff

## Where it fails / limitations
- iOS Safari trims storage aggressively after ~7 days of inactivity, evicts caches and IndexedDB
- Service workers are scoped: you can't fix a bad scope without unregistering on every client
- "Stale forever" bug: if a client gets stuck on an old SW that 404s the new asset graph, they're locked out — `clients.claim()` + skipWaiting must be planned, not bolted on
- Push notifications require backend (VAPID), TLS, and explicit permission — agents often forget the server side
- Service-worker bugs are silent in DevTools "normal" mode; need Application tab and `chrome://serviceworker-internals`
- Offline analytics and offline POSTs need queueing (Background Sync), which agents skip

## Agentic workflow
A two-pass agent works well: first an audit pass runs Lighthouse + a manifest/SW checklist and emits a gap list; second pass implements the missing pieces (manifest, Workbox config, install prompt hook, update banner). Treat the service worker as a deploy artifact — version it explicitly and gate releases on a smoke test that loads, mutates cache, then forces an update.

### Recommended subagents
- `faion-sdd-executor-agent` — design → impl → verify with Lighthouse gate
- A custom `pwa-auditor` (haiku) — runs Lighthouse + manifest validation and produces gap list
- A custom `sw-update-flow` (sonnet) — designs the skipWaiting/clients.claim handshake and the user-facing reload UX

### Prompt pattern
```
Audit <site> as a PWA: read manifest.json, registered SW path, cache strategies.
Output: gap list with severity (blocker/major/minor) referencing web.dev PWA checklist.
Then propose minimal Workbox config delta. Do not auto-apply skipWaiting.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lighthouse` | PWA audit, perf, a11y | `npm i -g lighthouse` · https://github.com/GoogleChrome/lighthouse |
| `pwa-asset-generator` | Generate icons + splash screens from one source | `npm i -g pwa-asset-generator` |
| `workbox-cli` | Generate/inject SW manifest | `npm i -g workbox-cli` · https://developer.chrome.com/docs/workbox/modules/workbox-cli |
| `vite-plugin-pwa` / `@angular/pwa` / `next-pwa` (Serwist) | Framework-side SW + manifest plumbing | https://vite-pwa-org.netlify.app · https://serwist.pages.dev |
| `web-push` | Send VAPID push from CLI/Node | `npm i web-push` |
| `pwabuilder` CLI | Build native wrappers (TWA/MSIX) from PWA | https://www.pwabuilder.com |
| `bubblewrap` | Generate Trusted Web Activity Android APKs | `npm i -g @bubblewrap/cli` |
| `unlighthouse` | Crawl-wide Lighthouse runs | `npm i -g @unlighthouse/cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Firebase Cloud Messaging | SaaS | Yes | Push backend; REST API for sending |
| OneSignal | SaaS | Yes | Higher-level push + segmentation, REST API |
| web-push (Node) + own VAPID | OSS | Yes | Self-host push; agents store keys in secret manager |
| Workbox | OSS | Yes | First-class SW abstractions; declarative config |
| Serwist | OSS | Yes | Workbox successor for Next.js; TS-first |
| PWABuilder | SaaS | Yes | Generates store packages from a PWA URL |
| Cloudflare Workers + Cache API | SaaS | Partial | Edge-side complement to client SW; not a replacement |
| Sentry / LogRocket | SaaS | Yes | Capture SW errors and offline UX regressions |

## Templates & scripts
See `templates.md` for the full Workbox config and React install hook. Inline minimal `vite.config.ts` block for Vite + PWA:

```ts
// vite.config.ts (PWA)
import { VitePWA } from 'vite-plugin-pwa';
export default {
  plugins: [
    VitePWA({
      registerType: 'prompt',          // never auto-skip; show update toast
      injectRegister: 'auto',
      includeAssets: ['favicon.svg', 'offline.html'],
      manifest: { /* see manifest.json in README */ },
      workbox: {
        navigateFallback: '/offline.html',
        runtimeCaching: [
          { urlPattern: /\/api\//, handler: 'NetworkFirst',
            options: { cacheName: 'api', networkTimeoutSeconds: 10,
              expiration: { maxEntries: 100, maxAgeSeconds: 3600 } } },
          { urlPattern: ({ request }) => request.destination === 'image',
            handler: 'CacheFirst',
            options: { cacheName: 'img',
              expiration: { maxEntries: 60, maxAgeSeconds: 60*60*24*30 } } },
        ],
      },
    }),
  ],
};
```

## Best practices
- Default to `registerType: 'prompt'` and explicit user-driven reload — never silent `skipWaiting()` for app shells with in-flight state
- Ship a working `offline.html` from day one; without it, the SW makes failures worse
- Cache APIs with `NetworkFirst` + a short `networkTimeoutSeconds` — `CacheFirst` on data is a footgun
- Version your SW filename or use `cacheName` suffixes; old caches must be cleaned in `activate`
- Test with Chrome DevTools "Offline" and "Slow 3G" toggles in CI via `lighthouse-ci`, not just locally
- Keep manifest icons at all required sizes (192, 512) plus a `maskable` variant for Android adaptive icons
- For installability: serve over HTTPS, register SW from same origin, manifest must include `start_url`, `display`, `name`, `icons[192]`, `icons[512]`

## AI-agent gotchas
- LLMs default to `CacheFirst` everywhere; that breaks freshness for APIs and HTML — review per-route strategy
- Agents forget the offline fallback registration in the SW `install` event, leaving navigations dead offline
- Service-worker scope errors: registering at `/app/sw.js` but expecting root scope — fail at runtime, not build
- iOS gotcha: agents test on Chromium and miss Safari quirks (no Background Sync, limited Push, storage caps)
- Push: agents generate VAPID keys but skip the subscription persistence layer; require an explicit DB schema diff
- Human-in-loop checkpoint: SW deploys are sticky — promote to prod behind a kill switch and a back-out SW that unregisters cleanly
- Agents forget that DevTools "Update on reload" hides real-user upgrade flow bugs; require a manual real-device pass

## References
- https://web.dev/learn/pwa/ — official curriculum
- https://web.dev/explore/progressive-web-apps
- https://developer.chrome.com/docs/workbox/
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- https://www.w3.org/TR/appmanifest/
- https://www.pwabuilder.com — store packaging
- https://web.dev/articles/offline-cookbook — caching strategies playbook
