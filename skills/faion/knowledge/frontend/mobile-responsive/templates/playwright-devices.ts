// playwright.config.ts (extract) — mobile/tablet/desktop device projects
import { devices, defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'mobile-chrome', use: { ...devices['Pixel 7'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 14'] } },
    { name: 'tablet',        use: { ...devices['iPad (gen 7) landscape'] } },
    { name: 'desktop',       use: { viewport: { width: 1440, height: 900 } } },
  ],
});
