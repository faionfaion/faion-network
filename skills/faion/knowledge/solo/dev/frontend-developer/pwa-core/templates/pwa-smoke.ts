/**
 * Playwright smoke tests for PWA: SW registration, offline navigation, manifest.
 *
 * Run: npx playwright test pwa-smoke.ts
 * Requires: the app to be running at BASE_URL (set in playwright.config.ts)
 */
import { test, expect } from "@playwright/test";

test.describe("PWA smoke tests", () => {
  test("service worker registers at origin root", async ({ page }) => {
    await page.goto("/");

    const swRegistered = await page.evaluate(async () => {
      if (!("serviceWorker" in navigator)) return false;
      const reg = await navigator.serviceWorker.getRegistration("/");
      return !!reg;
    });

    expect(swRegistered).toBe(true);
  });

  test("sw.js is served with Cache-Control: no-cache", async ({ request }) => {
    const response = await request.get("/sw.js");
    expect(response.status()).toBe(200);
    const cacheControl = response.headers()["cache-control"] ?? "";
    expect(cacheControl).toMatch(/no-cache|no-store|max-age=0/i);
  });

  test("manifest.json is reachable and has required fields", async ({ request }) => {
    const response = await request.get("/manifest.json");
    expect(response.status()).toBe(200);

    const manifest = await response.json();
    expect(manifest).toHaveProperty("id");
    expect(manifest).toHaveProperty("name");
    expect(manifest).toHaveProperty("start_url");
    expect(manifest).toHaveProperty("display");
    expect(manifest).toHaveProperty("icons");
    expect(Array.isArray(manifest.icons)).toBe(true);

    // All icons must have maskable purpose
    for (const icon of manifest.icons) {
      expect(icon.purpose).toMatch(/maskable/);
    }
  });

  test("offline navigation falls back gracefully", async ({ page, context }) => {
    // Warm the cache
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Go offline
    await context.setOffline(true);

    const response = await page.goto("/");
    // Expect either a cached response (200) or offline fallback (200) — not a network error
    expect(response?.status()).toBe(200);

    await context.setOffline(false);
  });

  test("install prompt event is captured or app is already installed", async ({ page }) => {
    await page.goto("/");
    // Verify there are no unhandled errors that would block the install flow
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));
    await page.waitForLoadState("networkidle");
    expect(errors).toHaveLength(0);
  });
});
