// purpose: Playwright project matrix covering mobile / tablet / desktop device profiles
// consumes: playwright.config.ts of the target repo
// produces: per-device test projects for the verification gate
// depends-on: content/01-core-rules.xml#multi-viewport-verification-gate
// token-budget-impact: ~0 tokens at runtime — config only
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
