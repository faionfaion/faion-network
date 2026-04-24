---
id: pwa-advanced
name: "PWA Development - Advanced Features"
domain: DEV
skill: faion-software-developer
category: "development"
---

# PWA Development - Advanced Features

## Push Notifications

```typescript
// lib/notifications.ts
const VAPID_PUBLIC_KEY = process.env.NEXT_PUBLIC_VAPID_KEY!;

export async function subscribeToPush(): Promise<PushSubscription | null> {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    console.log('Push notifications not supported');
    return null;
  }

  try {
    const registration = await navigator.serviceWorker.ready;

    // Check permission
    const permission = await Notification.requestPermission();
    if (permission !== 'granted') {
      console.log('Notification permission denied');
      return null;
    }

    // Subscribe to push
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
    });

    // Send subscription to backend
    await fetch('/api/push/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(subscription),
    });

    return subscription;
  } catch (error) {
    console.error('Failed to subscribe to push:', error);
    return null;
  }
}

function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

// Service worker push handler
// In service-worker.ts
self.addEventListener('push', (event) => {
  const data = event.data?.json() ?? {
    title: 'New Notification',
    body: 'You have a new notification',
  };

  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icons/icon-192x192.png',
      badge: '/icons/badge-72x72.png',
      tag: data.tag,
      data: data.url,
      actions: data.actions,
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  const url = event.notification.data || '/';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // Focus existing window if available
        for (const client of clientList) {
          if (client.url === url && 'focus' in client) {
            return client.focus();
          }
        }
        // Open new window
        return clients.openWindow(url);
      })
  );
});
```

## Offline Data Sync

```typescript
// lib/offline-sync.ts
import { openDB, DBSchema, IDBPDatabase } from 'idb';

interface OfflineDB extends DBSchema {
  'pending-requests': {
    key: string;
    value: {
      id: string;
      url: string;
      method: string;
      body: string;
      timestamp: number;
    };
  };
  'cached-data': {
    key: string;
    value: {
      key: string;
      data: unknown;
      timestamp: number;
    };
  };
}

let db: IDBPDatabase<OfflineDB>;

async function getDB() {
  if (!db) {
    db = await openDB<OfflineDB>('offline-db', 1, {
      upgrade(db) {
        db.createObjectStore('pending-requests', { keyPath: 'id' });
        db.createObjectStore('cached-data', { keyPath: 'key' });
      },
    });
  }
  return db;
}

// Queue request for later sync
export async function queueRequest(
  url: string,
  method: string,
  body: unknown
) {
  const db = await getDB();
  await db.add('pending-requests', {
    id: crypto.randomUUID(),
    url,
    method,
    body: JSON.stringify(body),
    timestamp: Date.now(),
  });
}

// Sync pending requests
export async function syncPendingRequests() {
  const db = await getDB();
  const pendingRequests = await db.getAll('pending-requests');

  for (const request of pendingRequests) {
    try {
      await fetch(request.url, {
        method: request.method,
        headers: { 'Content-Type': 'application/json' },
        body: request.body,
      });

      // Remove from queue on success
      await db.delete('pending-requests', request.id);
    } catch (error) {
      console.error('Failed to sync request:', error);
      // Keep in queue for retry
    }
  }
}

// Background sync registration
if ('serviceWorker' in navigator && 'sync' in (ServiceWorkerRegistration.prototype)) {
  navigator.serviceWorker.ready.then((registration) => {
    // @ts-ignore - Background Sync API types
    registration.sync.register('sync-pending-requests');
  });
}

// In service-worker.ts
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-pending-requests') {
    event.waitUntil(syncPendingRequests());
  }
});
```

## Network Status Hook

```typescript
// hooks/useOnlineStatus.ts
import { useState, useEffect } from 'react';

export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}

// Component
function OfflineIndicator() {
  const isOnline = useOnlineStatus();

  if (isOnline) return null;

  return (
    <div className="offline-banner" role="alert">
      You are offline. Some features may be unavailable.
    </div>
  );
}
```

## Best Practices

### Offline-First Strategy

- Cache critical resources during service worker installation
- Use Network First for dynamic content
- Use Cache First for static assets
- Implement fallback pages for offline scenarios

### Update Management

- Notify users when new version is available
- Provide manual refresh option
- Check for updates periodically
- Handle version conflicts gracefully

### Data Synchronization

- Queue failed requests in IndexedDB
- Retry on network reconnection
- Use Background Sync API when available
- Show sync status to users

### Performance Optimization

- Minimize service worker size
- Use selective caching strategies
- Implement cache expiration policies
- Monitor cache storage usage

## Testing

```typescript
// Test service worker registration
describe('Service Worker', () => {
  it('registers successfully', async () => {
    const registration = await registerServiceWorker();
    expect(registration).toBeDefined();
  });

  it('handles offline scenario', async () => {
    // Simulate offline
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);

    const response = await fetch('/api/data');
    // Should return cached data
    expect(response.status).toBe(200);
  });
});
```

## Debugging

- Use Chrome DevTools > Application > Service Workers
- Check Cache Storage in DevTools
- Monitor Network tab for offline behavior
- Use Lighthouse for PWA audit
- Test on real devices with throttled network

## Related Methodologies

- [mobile-responsive.md](mobile-responsive.md) - Responsive design patterns
- [testing-e2e.md](testing-e2e.md) - E2E testing with network conditions
- [api-rest-design.md](api-rest-design.md) - API design for offline support

## References

- [Background Sync API](https://developer.mozilla.org/en-US/docs/Web/API/Background_Sync_API)
- [Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
- [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Lighthouse PWA Audit](https://developer.chrome.com/docs/lighthouse/pwa/)

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
