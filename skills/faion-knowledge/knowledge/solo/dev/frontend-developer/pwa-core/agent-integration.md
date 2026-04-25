# Agent Integration — PWA Core

## When to use
- Web app needs offline tolerance, install prompt, push notifications, or "add to home screen" behavior.
- You want one codebase across desktop, Android, and iOS without an app store presence.
- Caching layer must survive flaky networks (transit, kiosk, captive Wi‑Fi).
- You are shipping a content/marketing site and want LCP/INP wins from precaching critical assets.

## When NOT to use
- iOS-first product where push, background sync, and persistent storage limits would block the use case (Safari still gates aggressively).
- Hard real-time apps (live trading, video conferencing) where service worker layers add cache-coherence headaches without offline upside.
- Highly regulated UI (banking transaction screens) where stale cache served by SW is a compliance risk.
- App requires deep OS integration (Bluetooth peripherals, full camera control, contacts) that PWAs cannot reliably reach on iOS.

## Where it fails / limitations
- Service worker scope tied to the file's path; deploying `sw.js` from `/static/` silently scopes it there. Always serve from origin root.
- iOS Safari purges PWA storage after ~7 days of non-use; offline-first plans must assume eviction.
- Workbox + bundlers (Vite, webpack, Next.js) each have their own injection step; mixing manual SW with framework integrations breaks `__WB_MANIFEST`.
- `beforeinstallprompt` fires once per session, not per page; agents that re-mount components lose the deferred prompt.
- Background sync and periodic sync require user engagement signals; CI smoke tests will not exercise them.
- HTTPS-only (except localhost). Staging on plain HTTP gives misleading "PWA not installable" errors.

## Agentic workflow
Drive PWA work as a three-phase agent loop: (1) audit current site with Lighthouse CI / `pwa-asset-generator`, (2) generate manifest + Workbox config from the README templates, (3) verify install + offline behavior in headless Chrome via Playwright. Treat the service worker as untrusted output — always run a Playwright `goto offline` check before merging. Subagents should produce JSON diffs of `manifest.json` and emit a Workbox config object, never edit the SW file in place.

### Recommended subagents
- `faion-frontend-component-agent` — generate install banner, update toast, offline fallback page from manifest spec.
- `faion-sdd-executor-agent` — wire SW build step into CI, add Lighthouse PWA budget, reject on score regression.
- `password-scrubber-agent` — sweep manifest and registration glue for accidentally cached secrets (auth tokens, signed URLs in precache list).

### Prompt pattern
```
You are configuring a PWA. Inputs: existing manifest.json, build tool (Vite|Next|webpack), routes that must work offline.
Output: (1) updated manifest.json, (2) workbox config object, (3) Playwright spec proving install prompt + offline navigation.
Do not invent icons; list missing icon sizes as TODO with sharp commands to generate them.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `@lhci/cli` | Lighthouse CI for PWA score budget | `npm i -D @lhci/cli` |
| `workbox-cli` | Generate / inject SW manifest | `npm i -D workbox-cli` |
| `pwa-asset-generator` | Icons + splash from one SVG | `npx pwa-asset-generator logo.svg ./icons` |
| `web-app-manifest-validator` | Lint manifest.json | `npx web-app-manifest-validator manifest.json` |
| `chrome --headless --enable-features=PWAManifest` | Manual install dry-run | bundled with Chrome |
| `bubblewrap` | Wrap PWA into Android TWA | `npm i -g @bubblewrap/cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PWABuilder | SaaS | Yes (web API) | Scores manifest, generates Android/iOS packages |
| OneSignal | SaaS | Yes (REST + SDK) | Push notifications without VAPID key juggling |
| Firebase Cloud Messaging | SaaS | Yes (REST + admin SDK) | Push; pairs well with Workbox `BackgroundSyncPlugin` |
| Cloudflare Workers | SaaS | Yes (Wrangler CLI) | Edge cache that complements SW; can serve manifest with correct headers |
| Workbox | OSS | Yes (deterministic config) | Library, not service; agents emit config objects |

## Templates & scripts
See `templates.md` and `examples.md` for full SW + manifest. Smoke check below validates install + offline in CI:

```ts
// scripts/pwa-smoke.ts
import { chromium } from 'playwright';

const url = process.env.URL ?? 'http://localhost:4173';
const browser = await chromium.launch();
const ctx = await browser.newContext({ serviceWorkers: 'allow' });
const page = await ctx.newPage();

await page.goto(url, { waitUntil: 'networkidle' });
const swReady = await page.evaluate(() => navigator.serviceWorker.ready.then(() => true));
if (!swReady) throw new Error('SW failed to register');

await ctx.setOffline(true);
const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
if (!resp || resp.status() >= 400) throw new Error('Offline navigation failed');

const manifestOk = await page.evaluate(async () => {
  const link = document.querySelector('link[rel=manifest]') as HTMLLinkElement | null;
  if (!link) return false;
  const r = await fetch(link.href);
  return r.ok;
});
if (!manifestOk) throw new Error('Manifest unreachable');

await browser.close();
console.log('PWA smoke OK');
```

## Best practices
- Serve `sw.js` and `manifest.json` from origin root with `Cache-Control: no-cache` so updates propagate.
- Precache the app shell only; never precache user-personalized HTML or API responses.
- Use `NetworkFirst` with `networkTimeoutSeconds: 3` for `/api/*`; fall back to cache to avoid spinner-of-death.
- Show update prompt on `controllerchange`, never auto-reload mid-form.
- Version caches with build hash; on activate, `caches.keys()` and delete stale ones.
- Always ship `purpose: "maskable any"` icons; Android crops non-maskable to weird circles.
- Keep manifest `id` field stable across deploys — changing it forces re-installation and breaks shortcuts.

## AI-agent gotchas
- LLMs hallucinate `workbox-strategies` import names across versions (`NetworkFirst` vs `networkFirst`); pin Workbox major and feed agent the exact import surface.
- Agents tend to register SW inside React effects; that double-registers in StrictMode dev. Register from `index.html` or a single bootstrap module instead.
- Service worker code runs in a different scope — agents that reach for `window` or `document` will silently break. Lint with `eslint-plugin-workbox` or a SW-specific tsconfig.
- Cache invalidation is the load-bearing decision; require human-in-loop sign-off whenever an agent changes precache list or routing strategies on production traffic.
- iOS-only failures rarely reproduce in agent test environments. Add a manual checklist gate before any "PWA-ready" claim.

## References
- https://web.dev/learn/pwa/
- https://developer.chrome.com/docs/workbox/
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- https://www.pwabuilder.com/
- https://github.com/GoogleChromeLabs/squoosh — image pipeline for icon assets
