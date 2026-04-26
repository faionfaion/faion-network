# Playwright Automation

## Summary

Cross-browser automation library (Chromium/Firefox/WebKit) for E2E testing, agentic web tasks, and headless scraping with auth reuse via `storageState`. The concrete rule: always prefer `getByRole` > `getByLabel` > `getByText` > CSS selectors — role-based locators survive UI tweaks; CSS selectors die on the next sprint. Never use `page.waitForTimeout`; use locator auto-wait or `expect(locator).toBeVisible({timeout})`.

## Why

Playwright's auto-wait model and trace viewer (screenshots + network + DOM snapshots per action) dramatically reduce flaky test debugging. `storageState` lets an agent authenticate once and reuse the session across hundreds of headless runs without re-login overhead. For agentic web tasks, Microsoft's `playwright-mcp` exposes the accessibility tree to LLMs — more reliable than raw DOM dumps.

## When To Use

- Cross-browser E2E tests (Chromium/Firefox/WebKit) with auto-waiting and trace viewer
- Agentic web tasks: login flows, form filling, scraping requiring JS execution
- Visual regression testing via `toHaveScreenshot()` snapshots
- API testing alongside UI in one session (`page.request`)
- Replacing legacy Selenium/Cypress suites for speed and reliability

## When NOT To Use

- Pure HTTP scraping where the target renders server-side (use httpx/fetch, 100x cheaper)
- Mobile-app E2E testing (use Appium, Detox, Maestro)
- Sub-millisecond unit tests of UI components (use Vitest + Testing Library)
- Targets with hard bot-detection (Cloudflare Turnstile aggressive mode)
- Long-lived stateful sessions (hours): better suited to a real browser profile

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-api.xml` | Auto-wait, locators, selectors, form handling, network interception, browser contexts |
| `content/02-testing-patterns.xml` | Test structure, fixtures, assertions, Page Object Model, advanced patterns |
| `content/03-agent-workflow.xml` | Agentic usage, storageState reuse, playwright-mcp, gotchas, services table |

## Templates

| File | Purpose |
|------|---------|
| `templates/scrape.mjs` | Headless scrape script with auth reuse via storageState |
| `templates/playwright-prompt.txt` | Prompt for generating Playwright TypeScript tests with role-locator rules |
