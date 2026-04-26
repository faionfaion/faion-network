/**
 * validate_events.js — Playwright script to verify GA4 event firing on staging
 *
 * Intercepts window.dataLayer.push calls to capture all events fired during
 * a test flow, then compares against an expected event list.
 *
 * Input: expected event names array, staging URL to test
 * Output: PASS or FAIL with list of missing events
 *
 * Usage:
 *   node validate_events.js
 *   # Edit STAGING_URL and EXPECTED_EVENTS below before running
 *
 * Requirements:
 *   npm install playwright
 */

const { chromium } = require("playwright");

const STAGING_URL = "https://staging.example.com/signup";
const EXPECTED_EVENTS = ["page_view", "sign_up", "trial_started"];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const seen = new Set();

  // Intercept dataLayer.push before any scripts run
  await page.addInitScript(() => {
    window.dataLayer = window.dataLayer || [];
    const originalPush = window.dataLayer.push.bind(window.dataLayer);
    window.dataLayer.push = (event) => {
      if (event && event.event) {
        // captureEvent is exposed via page.exposeFunction below
        if (typeof window.captureEvent === "function") {
          window.captureEvent(event.event);
        }
      }
      return originalPush(event);
    };
  });

  await page.exposeFunction("captureEvent", (name) => {
    seen.add(name);
  });

  await page.goto(STAGING_URL, { waitUntil: "networkidle" });

  // Simulate sign-up flow — adapt selectors to the actual form
  try {
    await page.fill('input[type="email"]', "test-validate@example.com");
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
  } catch {
    console.warn("Form interaction failed — check selectors for this staging URL");
  }

  const missing = EXPECTED_EVENTS.filter((e) => !seen.has(e));
  const extra = [...seen].filter((e) => !EXPECTED_EVENTS.includes(e));

  if (missing.length === 0) {
    console.log("PASS: all expected events fired");
    console.log("  Seen:", [...seen].join(", "));
  } else {
    console.error("FAIL: missing events:", missing.join(", "));
    console.log("  Seen:", [...seen].join(", "));
    console.log("  Extra (not in expected list):", extra.join(", "));
    process.exitCode = 1;
  }

  await browser.close();
})();
