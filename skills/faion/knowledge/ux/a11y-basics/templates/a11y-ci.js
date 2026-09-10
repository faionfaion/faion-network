// purpose: axe-core CI wiring snippet.
// consumes: see content/02-output-contract.xml inputs for a11y-basics
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-600 tokens when loaded as context

// Playwright test spec. Deps: npm i -D @playwright/test @axe-core/playwright
// Run in CI: A11Y_OWNER=@<handle> npx playwright test a11y-ci.js
// Emits one quick-check report per URL (content/02-output-contract.xml shape) into a11y-reports/.
// This is the automated ~30% only; the verdict is capped at "partial" until the manual
// 5-step check is attached (rule automated-only-catches-30pct).
const fs = require("node:fs");
const path = require("node:path");
const { test, expect } = require("@playwright/test");
const { AxeBuilder } = require("@axe-core/playwright");

const WCAG_VERSION = "2.2"; // rule pin-wcag-version-and-level: change only via team policy
const WCAG_LEVEL = "AA";
const AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]; // cumulative set for 2.2 AA
const PAGES = (process.env.A11Y_URLS || "http://localhost:3000/<page>").split(",");
const OWNER = process.env.A11Y_OWNER || ""; // one named handle, never "team"
const OUT_DIR = "a11y-reports";
const FAIL_ON = new Set(["critical", "serious"]); // axe impact levels that fail the PR

const POUR = { 1: "Perceivable", 2: "Operable", 3: "Understandable", 4: "Robust" }; // rule pour-as-frame-not-checklist
const SEVERITY = { critical: "high", serious: "high", moderate: "medium", minor: "low" };

// axe tags look like "wcag143" -> "1.4.3"; a rule may map to several SCs, take them all.
function scsOf(violation) {
  return violation.tags
    .map((t) => /^wcag(\d)(\d)(\d+)$/.exec(t))
    .filter(Boolean)
    .map((m) => `${m[1]}.${m[2]}.${m[3]}`);
}

function toFindings(violations) {
  const out = [];
  for (const v of violations) {
    const scs = scsOf(v);
    if (scs.length === 0) scs.push("best-practice");
    for (const sc of scs) {
      out.push({
        sc,
        principle: POUR[sc[0]] || "n/a",
        severity: SEVERITY[v.impact] || "low",
        description: `${v.id}: ${v.help} (${v.nodes.length} node(s), first: ${v.nodes[0]?.target?.join(" ") || "?"})`,
        source: "scanner",
        placeholder_as_label: v.id === "label" || v.id === "select-name", // rule placeholder-is-not-a-label
      });
    }
  }
  return out;
}

test.describe("a11y quick-check (automated layer)", () => {
  for (const url of PAGES) {
    test(`axe ${WCAG_VERSION} ${WCAG_LEVEL}: ${url}`, async ({ page }, testInfo) => {
      expect(OWNER, "A11Y_OWNER must be a single @handle").toMatch(/^@[\w-]+$/);
      await page.goto(url, { waitUntil: "networkidle" });
      // Dismiss consent overlays before scanning; an overlay hides the real page from axe.
      await page.locator("<cookie-accept-selector>").click({ timeout: 2000 }).catch(() => {});

      const results = await new AxeBuilder({ page }).withTags(AXE_TAGS).analyze();
      const findings = toFindings(results.violations);
      const blocking = results.violations.filter((v) => FAIL_ON.has(v.impact));

      const report = {
        artefact_id: `a11y-bas-${new Date().toISOString().slice(0, 10)}-${testInfo.workerIndex}-${PAGES.indexOf(url)}`,
        version: "1.1.0",
        last_reviewed: new Date().toISOString().slice(0, 10),
        owner: OWNER,
        scope: { page_url: url, wcag_version: WCAG_VERSION, level: WCAG_LEVEL },
        findings,
        // axe "incomplete" entries are not passes; they are the untested part of the 30%.
        summary:
          `axe surfaced ${results.violations.length} violation(s), ${results.incomplete.length} incomplete check(s). ` +
          "Scanner catches approx. 30% of issues; manual + AT + user testing required. " +
          "Pending: 5-step manual quick-check (tab through, 200% zoom, alt-text, label, axe).",
        verdict: findings.length ? "fail" : "partial",
      };
      fs.mkdirSync(OUT_DIR, { recursive: true });
      const file = path.join(OUT_DIR, `${report.artefact_id}.json`);
      fs.writeFileSync(file, JSON.stringify(report, null, 2));
      await testInfo.attach("quick-check-report", { path: file, contentType: "application/json" });

      expect(blocking, blocking.map((v) => `${v.id}: ${v.help}`).join("\n")).toEqual([]);
    });
  }
});
