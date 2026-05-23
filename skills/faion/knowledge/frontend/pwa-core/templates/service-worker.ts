/**
 * Workbox service worker.
 * Build with: workbox-build (generateSW or injectManifest) or vite-plugin-pwa.
 *
 * Rules:
 * - SW must live at /sw.js (origin root) with Cache-Control: no-cache
 * - No window/document access — runs in ServiceWorkerGlobalScope
 * - Strategies: NetworkFirst for nav+API, CacheFirst for images/fonts, SWR for JS/CSS
 */
/// <reference lib="webworker" />
declare const self: ServiceWorkerGlobalScope;

import { clientsClaim } from "workbox-core";
import { cleanupOutdatedCaches, precacheAndRoute } from "workbox-precaching";
import { registerRoute, NavigationRoute } from "workbox-routing";
import { NetworkFirst, CacheFirst, StaleWhileRevalidate } from "workbox-strategies";
import { ExpirationPlugin } from "workbox-expiration";
import { CacheableResponsePlugin } from "workbox-cacheable-response";

// Take control immediately after activation
clientsClaim();

// Precache the app shell (populated by build tool)
precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches();

// Navigation: NetworkFirst with 3s timeout → cache fallback
registerRoute(
  new NavigationRoute(
    new NetworkFirst({
      cacheName: "pages",
      networkTimeoutSeconds: 3,
      plugins: [
        new CacheableResponsePlugin({ statuses: [0, 200] }),
        new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 86400 }),
      ],
    })
  )
);

// API: NetworkFirst, cache as offline fallback (1h max)
registerRoute(
  ({ url }) => url.pathname.startsWith("/api/"),
  new NetworkFirst({
    cacheName: "api",
    networkTimeoutSeconds: 3,
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 3600 }),
    ],
  })
);

// Images: CacheFirst, 30-day expiry
registerRoute(
  ({ request }) => request.destination === "image",
  new CacheFirst({
    cacheName: "images",
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxEntries: 60, maxAgeSeconds: 2592000 }),
    ],
  })
);

// Fonts: CacheFirst, 1-year expiry
registerRoute(
  ({ request }) => request.destination === "font",
  new CacheFirst({
    cacheName: "fonts",
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxEntries: 20, maxAgeSeconds: 31536000 }),
    ],
  })
);

// JS/CSS static assets: StaleWhileRevalidate
registerRoute(
  ({ request }) =>
    request.destination === "script" || request.destination === "style",
  new StaleWhileRevalidate({
    cacheName: "static-assets",
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
    ],
  })
);

// Offline fallback for navigation
self.addEventListener("fetch", (event) => {
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request).catch(() =>
        caches.match("/offline.html") as Promise<Response>
      )
    );
  }
});
