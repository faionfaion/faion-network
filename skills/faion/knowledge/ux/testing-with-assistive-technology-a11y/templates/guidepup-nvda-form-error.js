// purpose: Guidepup script template for NVDA form-error flow.
// consumes: see content/02-output-contract.xml inputs for testing-with-assistive-technology
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-600 tokens when loaded as context

// Windows only (NVDA). Deps: npm i -D @guidepup/guidepup playwright
// Setup once: npx @guidepup/setup   (installs a pinned NVDA into the rig; do not auto-update it)
// Run: AT_VERSION=2024.2 RIG_ID=rig-win11-01 node guidepup-nvda-form-error.js
// Guidepup API used here has been stable since v0.20 (2023).
const fs = require("node:fs");
const path = require("node:path");
const { nvda } = require("@guidepup/guidepup");
const { chromium } = require("playwright");

const PAGE_URL = process.env.PAGE_URL || "https://<staging-host>/<form-path>";
const FIELD_LABEL = process.env.FIELD_LABEL || "<Email>";       // visible label of the required field left empty
const ERROR_TEXT = process.env.ERROR_TEXT || "<Enter your email>"; // exact error copy the page renders
const SUBMIT_LABEL = process.env.SUBMIT_LABEL || "<Place order>";
const OUT_DIR = process.env.OUT_DIR || "artifacts";
const AT_ID = `NVDA-${process.env.AT_VERSION || "<version>"}`;   // rule at-and-version-pinned: version is mandatory
const RIG_ID = process.env.RIG_ID || "<rig-baseline-id>";          // rule no-shared-rig: frozen rig baseline

const has = (log, text) => log.some((p) => p.toLowerCase().includes(text.toLowerCase()));

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  // Guidepup drives the real NVDA, so the browser must be headed and focused.
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto(PAGE_URL, { waitUntil: "networkidle" });

  await nvda.start();
  await nvda.clearSpokenPhraseLog();
  try {
    // Step 1: land on the required field, leave it empty.
    await nvda.perform(nvda.keyboardCommands.moveToNextFormField);
    const fieldPhrase = await nvda.lastSpokenPhrase();

    // Step 2: move to submit and activate it with the field still empty.
    let guard = 0;
    while (!(await nvda.lastSpokenPhrase()).toLowerCase().includes(SUBMIT_LABEL.toLowerCase()) && guard++ < 20) {
      await nvda.press("Tab");
    }
    await nvda.act();
    await page.waitForTimeout(1500); // let aria-live / focus move settle before reading the log

    // Step 3: what did NVDA actually say after submit?
    const log = await nvda.spokenPhraseLog();
    const afterSubmit = log.slice(log.findIndex((p) => p.toLowerCase().includes(SUBMIT_LABEL.toLowerCase())) + 1);
    const transcriptPath = path.join(OUT_DIR, "nvda-form-error.log");
    fs.writeFileSync(transcriptPath, log.join("\n"), "utf8"); // rule recording-required

    // Each check maps to one WCAG SC (rule finding-mapped-to-sc). Severity uses the a11y-testing enum.
    const checks = [
      { sc: "3.3.1", severity: "blocker", ok: has(afterSubmit, ERROR_TEXT), what: "error text announced after submit" },
      { sc: "4.1.2", severity: "major", ok: has(afterSubmit, "invalid") || has(afterSubmit, FIELD_LABEL), what: "invalid state or field name in announcement (aria-invalid / focus moved to field)" },
      { sc: "3.3.3", severity: "minor", ok: has(afterSubmit, "<suggestion-keyword>"), what: "correction suggestion announced" },
      { sc: "3.3.2", severity: "major", ok: fieldPhrase.toLowerCase().includes("required"), what: "required state announced on the field itself" },
    ];
    const findings = checks
      .filter((c) => !c.ok)
      .map((c) => ({ at: AT_ID, sc: c.sc, severity: c.severity, observation: `missing: ${c.what}`, recording_url: transcriptPath }));

    const record = {
      artefact_id: `at-${new Date().toISOString().slice(0, 10)}-form-error`,
      version: "1.1.0",
      last_reviewed: new Date().toISOString().slice(0, 10),
      owner: process.env.AT_OWNER || "<@qa-lead>",
      scope: { flows: [new URL(PAGE_URL).pathname], ats: [AT_ID, "<paired-at-for-this-flow>"], rig: RIG_ID },
      findings,
      summary: findings.length ? `${findings.length} SC failure(s) on ${AT_ID}; paired AT cell still required (rule matrix-coverage).` : `Form error flow passes on ${AT_ID}; run the paired AT cell before closing the flow.`,
      verdict: findings.some((f) => f.severity === "blocker") ? "fail" : findings.length ? "partial" : "pass",
    };
    fs.writeFileSync(path.join(OUT_DIR, "at-finding-record.json"), JSON.stringify(record, null, 2));
    console.log(JSON.stringify(record, null, 2));
    process.exitCode = record.verdict === "fail" ? 1 : 0;
  } finally {
    await nvda.stop();
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(2);
});
