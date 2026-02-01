---
id: pwa-core
name: "PWA Development - Core Concepts"
domain: DEV
skill: faion-software-developer
category: "development"
---

# PWA Development - Core Concepts

## Overview

Progressive Web Apps (PWAs) combine the best of web and native apps, offering offline capability, push notifications, and app-like experiences through web technologies. PWAs work on any platform with a standards-compliant browser.

## When to Use

- Mobile-first web applications
- Apps requiring offline functionality
- Applications needing push notifications
- Installable web experiences
- Reducing app store dependency

## Key Principles

- **Progressive enhancement**: Works for every user regardless of browser
- **Responsive**: Fits any form factor
- **Connectivity independent**: Works offline or on slow networks
- **App-like**: Feels like a native app
- **Installable**: Can be added to home screen

## Best Practices

### Web App Manifest

```json
// public/manifest.json
{
  "name": "Example App",
  "short_name": "ExampleApp",
  "description": "A progressive web application example",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0066cc",
  "orientation": "portrait-primary",
  "scope": "/",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "maskable any"
    },
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
      "name": "New Order",
      "short_name": "Order",
      "description": "Create a new order",
      "url": "/orders/new",
      "icons": [{ "src": "/icons/new-order.png", "sizes": "192x192" }]
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    },
    {
      "src": "/screenshots/mobile.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ],
  "categories": ["shopping", "productivity"],
  "related_applications": [],
  "prefer_related_applications": false
}
```

### Service Worker (Workbox)

```typescript
// service-worker.ts
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute, NavigationRoute } from 'workbox-routing';
import {
  NetworkFirst,
  CacheFirst,
  StaleWhileRevalidate,
} from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

declare const self: ServiceWorkerGlobalScope;

// Precache static assets (injected by build tool)
precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches();

// Cache page navigations (HTML) with Network First
registerRoute(
  new NavigationRoute(
    new NetworkFirst({
      cacheName: 'pages-cache',
      plugins: [
        new CacheableResponsePlugin({
          statuses: [0, 200],
        }),
      ],
    })
  )
);

// Cache API responses with Network First
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 10,
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 60 * 60, // 1 hour
      }),
    ],
  })
);

// Cache images with Cache First
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
    ],
  })
);

// Cache fonts with Cache First
registerRoute(
  ({ request }) => request.destination === 'font',
  new CacheFirst({
    cacheName: 'fonts-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxEntries: 10,
        maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
      }),
    ],
  })
);

// Cache static assets with Stale While Revalidate
registerRoute(
  ({ request }) =>
    request.destination === 'style' ||
    request.destination === 'script',
  new StaleWhileRevalidate({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// Handle offline fallback
const FALLBACK_HTML = '/offline.html';
const FALLBACK_IMAGE = '/images/offline.png';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('offline-fallbacks').then((cache) => {
      return cache.addAll([FALLBACK_HTML, FALLBACK_IMAGE]);
    })
  );
});

// Serve fallback for failed navigations
registerRoute(
  ({ request }) => request.mode === 'navigate',
  async ({ event }) => {
    try {
      return await new NetworkFirst({
        cacheName: 'pages-cache',
      }).handle({ event, request: event.request });
    } catch (error) {
      return caches.match(FALLBACK_HTML);
    }
  }
);
```

### Service Worker Registration

```typescript
// lib/pwa.ts
export async function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/',
      });

      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New content available, notify user
              showUpdateNotification();
            }
          });
        }
      });

      console.log('Service Worker registered successfully');
      return registration;
    } catch (error) {
      console.error('Service Worker registration failed:', error);
    }
  }
}

export function showUpdateNotification() {
  // Show a toast or banner
  if (confirm('New version available! Reload to update?')) {
    window.location.reload();
  }
}

// Check for updates periodically
export function checkForUpdates(registration: ServiceWorkerRegistration) {
  setInterval(() => {
    registration.update();
  }, 60 * 60 * 1000); // Check every hour
}
```

### Install Prompt

```typescript
// hooks/useInstallPrompt.ts
import { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export function useInstallPrompt() {
  const [installPrompt, setInstallPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
      return;
    }

    const handler = (e: Event) => {
      e.preventDefault();
      setInstallPrompt(e as BeforeInstallPromptEvent);
    };

    window.addEventListener('beforeinstallprompt', handler);

    // Listen for successful installation
    window.addEventListener('appinstalled', () => {
      setIsInstalled(true);
      setInstallPrompt(null);
    });

    return () => {
      window.removeEventListener('beforeinstallprompt', handler);
    };
  }, []);

  const promptInstall = async () => {
    if (!installPrompt) return;

    await installPrompt.prompt();
    const { outcome } = await installPrompt.userChoice;

    if (outcome === 'accepted') {
      setInstallPrompt(null);
    }
  };

  return {
    canInstall: !!installPrompt && !isInstalled,
    isInstalled,
    promptInstall,
  };
}

// Component
function InstallBanner() {
  const { canInstall, promptInstall } = useInstallPrompt();

  if (!canInstall) return null;

  return (
    <div className="install-banner">
      <p>Install our app for a better experience!</p>
      <button onClick={promptInstall}>Install</button>
      <button onClick={() => {}}>Maybe Later</button>
    </div>
  );
}
```

## Anti-patterns

- **No offline fallback**: App completely broken when offline
- **Cache everything**: Caching sensitive or frequently changing data
- **Ignoring updates**: Not notifying users of new versions
- **Blocking install**: Showing install prompt immediately
- **No sync strategy**: Losing user data when offline
- **Missing manifest fields**: Incomplete PWA configuration

## References

- [web.dev PWA Guide](https://web.dev/progressive-web-apps/)
- [Workbox Documentation](https://developer.chrome.com/docs/workbox/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [PWA Builder](https://www.pwabuilder.com/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Fix CSS typo, update Tailwind class, run prettier | haiku | Direct text replacement and formatting |
| Code review component accessibility compliance | sonnet | WCAG standards evaluation |
| Debug responsive layout issues across breakpoints | sonnet | Testing and debugging |
| Design system architecture and token structure | opus | Complex organization and scaling |
| Refactor React component for performance | sonnet | Optimization and code quality |
| Plan design token migration across 50+ components | opus | Large-scale coordination |
| Build storybook automation and interactions | sonnet | Testing and documentation setup |
