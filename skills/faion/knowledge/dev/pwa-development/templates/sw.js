// purpose: Service worker skeleton: precache + navigation fallback + skipWaiting + clients.claim.
// consumes: see content/02-output-contract.xml inputs for pwa-development
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
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
