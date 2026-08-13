# PWA Development

## Summary

**One-sentence:** PWA spec covering manifest fields, service-worker lifecycle, install prompt, update flow, and offline strategy; rejects manifests missing icons or service workers that swallow updates.

**One-paragraph:** PWAs fail in three predictable ways: manifest missing the icon set required for install, service worker that caches index.html with cache-first and never updates, and update flow that leaves users on a stale shell forever. This methodology produces a spec naming manifest fields (name, short_name, icons 192+512, start_url, display, theme_color), service-worker scope, caching strategy per route (stale-while-revalidate / network-first / cache-first with TTL), update strategy (skipWaiting + clients.claim + user-visible reload prompt), and offline page contract.

**Ефективно для:**

- Mobile web app переходить в installable PWA - треба manifest + SW spec.
- SW кешує index.html і нові деплої не доходять до користувачів - оновити стратегію.
- Lighthouse PWA audit fail - зафіксувати manifest fields.
- Offline mode потрібен для core flow - визначити що кешується.
- Push notifications wired - перевірити що SW lifecycle не блокує оновлень.

## Applies If (ALL must hold)

- Web app is intended to be installable on mobile or desktop.
- Offline support is a product requirement (not just nice-to-have).
- Build pipeline can output a service worker (Workbox, vite-plugin-pwa, etc.).
- Team can ship a user-visible update prompt and reload flow.

## Skip If (ANY kills it)

- Site is purely static marketing with no app behaviour.
- App lives only inside an iframe of a host app (PWA install blocked).
- Compliance forbids client-side caching of user data.
- Push notifications and install are explicitly out of scope.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Icon set | PNG 192/512 + maskable variant | design |
| Route map | list of routes + freshness budget | engineering |
| Offline UX brief | what works offline / what is read-only | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[seo-for-spas]] | shared SPA shell concerns; offline page must be indexable when online. |
| [[caching-strategy]] | server-side cache headers complement SW cache strategy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: manifest fields, SW scope explicit, shell not cache-first, update prompt, offline page, TTL per route, HTTPS-only | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: manifest, SW scope, cache plan, update flow, offline page | ~900 |
| `content/05-examples.xml` | essential | Worked example for an installable note-taking PWA | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-manifest` | haiku | Boilerplate JSON with fixed fields. |
| `design-cache-plan` | sonnet | Per-route judgement on freshness vs offline. |
| `wire-update-flow` | sonnet | UX detail; user-visible prompt copy. |
| `audit-with-lighthouse` | haiku | Mechanical run + delta against rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/manifest.webmanifest` | manifest.webmanifest skeleton with required fields and maskable icon. |
| `templates/manifest.json` | manifest.json variant with shortcuts, categories, and prefer_related_applications. |
| `templates/sw.js` | Service worker skeleton: precache + navigation fallback + skipWaiting + clients.claim. |
| `templates/vite-pwa-config.ts` | Minimal Vite PWA plugin config with prompt registerType. |
| `templates/_smoke-test.json` | Minimum viable PWA spec artefact for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pwa-development.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[seo-for-spas]]
- [[caching-strategy]]
- [[react-component-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - manifest completeness, SW lifecycle, shell strategy, offline support - onto a rule from `content/01-core-rules.xml`. Use it before drafting the SW + manifest: it catches cache-first-on-shell and silent-update failure modes upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/manifest.webmanifest`

```json
{
  "__faion_header__": {
    "purpose": "manifest.webmanifest skeleton with required fields and maskable icon.",
    "consumes": "see content/02-output-contract.xml inputs for pwa-development",
    "produces": "artefact conforming to content/02-output-contract.xml",
    "depends_on": "content/01-core-rules.xml + content/04-procedure.xml",
    "token_budget_impact": "~200-700 tokens when loaded as context"
  },
  "name": "REPLACE",
  "short_name": "REPLACE",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/icons/192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "/icons/512-maskable.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

### `templates/manifest.json`

```json
{
  "name": "Example App",
  "short_name": "ExampleApp",
  "description": "A progressive web application",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0066cc",
  "orientation": "portrait-primary",
  "scope": "/",
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable any"
    }
  ],
  "shortcuts": [
    {
      "name": "New Item",
      "short_name": "New",
      "url": "/new",
      "icons": [
        {
          "src": "/icons/new-item.png",
          "sizes": "192x192"
        }
      ]
    }
  ],
  "categories": [
    "productivity"
  ],
  "prefer_related_applications": false
}
```

### `templates/sw.js`

```javascript
import { precacheAndRoute } from 'workbox-precaching';
import { NavigationRoute, registerRoute } from 'workbox-routing';
import { NetworkFirst, StaleWhileRevalidate, CacheFirst } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

self.skipWaiting();
clients.claim();

precacheAndRoute(self.__WB_MANIFEST || []);

registerRoute(new NavigationRoute(new NetworkFirst({ cacheName: 'shell', networkTimeoutSeconds: 3 })));

registerRoute(/\\/api\\/static\\//, new CacheFirst({ cacheName: 'api-static', plugins: [new ExpirationPlugin({ maxAgeSeconds: 86400, maxEntries: 100 })] }));
registerRoute(/\\/api\\/notes\\//, new StaleWhileRevalidate({ cacheName: 'api-notes', plugins: [new ExpirationPlugin({ maxAgeSeconds: 300, maxEntries: 200 })] }));
```

### `templates/vite-pwa-config.ts`

```typescript
import { VitePWA } from 'vite-plugin-pwa';

export default {
  plugins: [
    VitePWA({
      registerType: 'prompt',        // user controls when new SW activates
      injectRegister: 'auto',
      includeAssets: ['favicon.svg', 'offline.html'],
      manifest: {
        // see templates/manifest.json for full manifest
        name: 'Example App',
        short_name: 'ExampleApp',
        start_url: '/',
        display: 'standalone',
        theme_color: '#0066cc',
        icons: [
          { src: '/icons/icon-192x192.png', sizes: '192x192', type: 'image/png', purpose: 'maskable any' },
          { src: '/icons/icon-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable any' },
        ],
      },
      workbox: {
        navigateFallback: '/offline.html',
        runtimeCaching: [
          {
            urlPattern: /\/api\//,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api',
              networkTimeoutSeconds: 10,
              expiration: { maxEntries: 100, maxAgeSeconds: 3600 },
            },
          },
          {
            urlPattern: ({ request }) => request.destination === 'image',
            handler: 'CacheFirst',
            options: {
              cacheName: 'images',
              expiration: { maxEntries: 60, maxAgeSeconds: 60 * 60 * 24 * 30 },
            },
          },
        ],
      },
    }),
  ],
};
```

### `templates/_smoke-test.json`

```json
{
  "manifest": {
    "name": "X",
    "short_name": "X",
    "start_url": "/",
    "display": "standalone",
    "icons": [
      {
        "src": "/192.png",
        "sizes": "192x192"
      }
    ]
  },
  "service_worker": {
    "scope": "/",
    "skip_waiting": true,
    "clients_claim": true
  },
  "cache_plan": [
    {
      "route": "/",
      "strategy": "network-first",
      "ttl_seconds": 60,
      "max_entries": 1
    }
  ],
  "update_strategy": {
    "user_prompt": true,
    "auto_reload": false
  }
}
```
