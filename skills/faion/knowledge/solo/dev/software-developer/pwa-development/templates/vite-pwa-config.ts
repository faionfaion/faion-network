// vite.config.ts — minimal Vite PWA plugin config
// Requires: vite-plugin-pwa
// Install: npm i -D vite-plugin-pwa

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
