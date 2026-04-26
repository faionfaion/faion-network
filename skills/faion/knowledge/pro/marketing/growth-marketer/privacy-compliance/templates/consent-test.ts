// consent-test.ts — Playwright regression tests for analytics consent compliance
// Run in CI to catch analytics cookies firing before consent

import { test, expect } from "@playwright/test";

const ALLOWED_PRE_CONSENT = ["__cf_bm", "csrftoken", "session"]; // strictly necessary only
const BASE_URL = process.env.TEST_URL || "https://example.com";

test("no analytics cookies set before consent", async ({ page, context }) => {
  await page.goto(BASE_URL);
  await page.waitForLoadState("networkidle");
  const cookies = await context.cookies();
  const violations = cookies.filter(
    (c) => !ALLOWED_PRE_CONSENT.some((ok) => c.name.startsWith(ok))
  );
  expect(violations, `Non-essential cookies set pre-consent:\n${JSON.stringify(violations, null, 2)}`).toEqual([]);
});

test("GA4 fires only after explicit consent", async ({ page }) => {
  const analyticsRequests: string[] = [];
  page.on("request", (r) => {
    if (r.url().includes("google-analytics.com")) analyticsRequests.push(r.url());
  });

  await page.goto(BASE_URL);
  await page.waitForLoadState("networkidle");
  expect(
    analyticsRequests.find((u) => u.includes("/g/collect")),
    "GA4 collect fired before consent"
  ).toBeUndefined();

  await page.getByRole("button", { name: /accept all/i }).click();
  await page.waitForRequest((r) => r.url().includes("google-analytics.com"));
  expect(analyticsRequests.length).toBeGreaterThan(0);
});

test("reject all is one click and does not fire analytics", async ({ page }) => {
  const analyticsRequests: string[] = [];
  page.on("request", (r) => {
    if (r.url().includes("google-analytics.com")) analyticsRequests.push(r.url());
  });

  await page.goto(BASE_URL);
  await page.getByRole("button", { name: /reject all/i }).click();
  await page.waitForLoadState("networkidle");
  expect(
    analyticsRequests.find((u) => u.includes("/g/collect")),
    "GA4 collect fired after reject"
  ).toBeUndefined();
});
