// a11y-ci.js — Playwright + axe-core CI gate for WCAG 2.2 AA
// Usage: npx playwright test tests/a11y-ci.js
// Requires: npm install -D @playwright/test @axe-core/playwright
// Set BASE_URL env var or defaults to http://localhost:3000

const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

const BASE_URL = process.env.BASE_URL || "http://localhost:3000";

// Define routes to check — extend as your app grows
const ROUTES = [
  "/",
  "/pricing",
  "/login",
  "/signup",
  "/dashboard",
];

for (const route of ROUTES) {
  test(`a11y WCAG 2.2 AA: ${route}`, async ({ page }) => {
    await page.goto(`${BASE_URL}${route}`, { waitUntil: "networkidle" });

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
      .analyze();

    // Fail on critical and serious violations only
    // Moderate and minor violations are reported but do not block CI
    const blocking = results.violations.filter(
      (v) => v.impact === "critical" || v.impact === "serious"
    );

    if (blocking.length > 0) {
      const summary = blocking
        .map(
          (v) =>
            `[${v.impact.toUpperCase()}] ${v.id}: ${v.description}\n` +
            `  Nodes: ${v.nodes.map((n) => n.html).join(", ")}`
        )
        .join("\n\n");
      expect(blocking, `Blocking a11y violations on ${route}:\n\n${summary}`).toEqual([]);
    }

    // Log non-blocking violations for awareness (do not fail)
    const nonBlocking = results.violations.filter(
      (v) => v.impact !== "critical" && v.impact !== "serious"
    );
    if (nonBlocking.length > 0) {
      console.warn(`[a11y warn] ${nonBlocking.length} non-blocking violation(s) on ${route}`);
    }
  });
}
