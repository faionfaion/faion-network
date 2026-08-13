# Browser Automation

## Summary

**One-sentence:** Designs a resilient Playwright (or Puppeteer) automation with explicit waits keyed on assertions, Page Object Model isolation, anti-flake retry policy, and a kill-switch on selector-churn.

**One-paragraph:** Browser automation breaks for three reasons: timing assumptions, brittle selectors, and mixed concerns in page logic. This methodology emits an automation-spec: assertion-based explicit waits (no sleep), Page Object Model per screen, selector-strategy policy (data-test-id &gt; role &gt; text &gt; CSS), a flake budget that fails CI if breached, and an extract-data primitive separated from interaction. Output: automation-spec + page-object scaffold + extract primitive + flake budget.

**Ефективно для:**

- Solo dev whose e2e suite went from green to 60% flaky in a quarter.
- Adding scraping + extraction for a product that needs offline data sync.
- Wiring data-test-id everywhere so the design team can refactor without breaking tests.
- Setting a flake budget that gates merges instead of letting flakes accumulate.

## Applies If (ALL must hold)

- Browser automation runs in CI (not just locally).
- Target site has DOM stability OR data-test-id can be added.
- Author has authority to fail the suite on flake budget breach.

## Skip If (ANY kills it)

- API-only testing (use api-contract-first).
- Visual regression only (use a screenshot-diff methodology).
- Unit-tested code that doesn't need browser.
- Third-party site where data-test-id is impossible AND the surface churns weekly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target URL or app | URL | running app or third party |
| Playwright / Puppeteer | npm dependency | package.json |
| CI runner | GitHub Actions / GitLab CI | platform |
| Flake budget | rate (% per 100 runs) | team-agreed default ≤2% |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[flaky-test-elimination]] | Same anti-flake discipline applies. |
| [[deterministic-test-data-pattern]] | Data fixtures used by automation must be deterministic. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `browser_automation_draft` | sonnet | Bounded synthesis. |
| `browser_automation_validate` | haiku | Mechanical schema check. |
| `browser_automation_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/page-object.js` | Generic Page Object base class with data-test-id helpers |
| `templates/extract.js` | Extraction primitive separated from interaction |
| `templates/output-schema.json` | JSON Schema (draft-07) for the browser-automation artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in browser-automation artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-browser-automation.py` | Validate browser-automation artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[performance-testing]]
- [[security-testing]]
- [[ai-pair-coding-prompt-patterns]]
- [[ai-generated-test-validation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/page-object.js`

```javascript
 */
// page-object.js — Page Object Model scaffold for Playwright.
// Each page gets its own POM file; selectors never appear inline in tests.

class LoginPage {
  constructor(page) {
    this.page = page;
    // Prefer role/text locators over CSS
    this.usernameInput = page.locator('role=textbox[name="Username"]');
    this.passwordInput = page.locator('role=textbox[name="Password"]');
    this.submitButton = page.locator('role=button[name="Sign in"]');
    this.errorMessage = page.locator('[data-testid="auth-error"]');
  }

  async navigate() {
    await this.page.goto('/login');
  }

  async login(username, password) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return this.errorMessage.textContent();
  }

  async isLoggedIn() {
    return this.page.locator('[data-testid="dashboard"]').isVisible();
  }
}

module.exports = { LoginPage };
```

### `templates/extract.js`

```javascript
 */
// extract.js — Playwright extractor with Zod schema validation.
// Usage: URL=https://example.com/products npx playwright install chromium && node extract.js
const { chromium } = require('playwright');
const { z } = require('zod');

const Item = z.object({
  title: z.string().min(1),
  price: z.number().positive(),
  url: z.string().url(),
});

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (compatible; bot/1.0)',
  });
  const page = await context.newPage();

  // Block non-essential resources for speed
  await page.route('**/*.{png,jpg,svg,woff2,gif,css}', (r) => r.abort());

  await page.goto(process.env.URL, { waitUntil: 'networkidle' });

  const raw = await page.locator('article.product').evaluateAll((els) =>
    els.map((e) => ({
      title: e.querySelector('h2')?.textContent?.trim(),
      price: parseFloat(e.querySelector('.price')?.textContent?.replace(/[^0-9.]/g, '')),
      url: e.querySelector('a')?.href,
    })),
  );

  const items = raw
    .map((r, i) => {
      const result = Item.safeParse(r);
      if (!result.success) console.error(`row ${i} skipped:`, result.error.flatten());
      return result.success ? result.data : null;
    })
    .filter(Boolean);

  console.log(JSON.stringify(items, null, 2));
  await browser.close();
})();
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/browser-automation.json",
  "type": "object",
  "required": [
    "spec_id",
    "target_url",
    "framework",
    "page_objects",
    "selector_strategy",
    "flake_budget_pct"
  ],
  "properties": {
    "spec_id": {
      "type": "string",
      "pattern": "^BA-[A-Z0-9-]{2,40}$"
    },
    "target_url": {
      "type": "string",
      "minLength": 4
    },
    "framework": {
      "type": "string",
      "enum": [
        "playwright",
        "puppeteer",
        "selenium"
      ]
    },
    "page_objects": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "selector_strategy": {
      "type": "object",
      "required": [
        "primary",
        "fallback_order"
      ]
    },
    "flake_budget_pct": {
      "type": "number",
      "minimum": 0,
      "maximum": 10
    },
    "sleep_calls": {
      "type": "integer",
      "minimum": 0
    },
    "extract_module": {
      "type": "string"
    },
    "interact_module": {
      "type": "string"
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "spec_id": "BA-ONBOARDING-E2E",
  "target_url": "https://staging.example.com",
  "framework": "playwright",
  "page_objects": [
    "pages/SignUpPage.ts",
    "pages/CheckoutPage.ts",
    "pages/AccountPage.ts"
  ],
  "selector_strategy": {
    "primary": "data-test-id",
    "fallback_order": [
      "role",
      "text",
      "css"
    ]
  },
  "flake_budget_pct": 1.5,
  "sleep_calls": 0,
  "extract_module": "lib/extract.ts",
  "interact_module": "lib/page-object.ts"
}
```
