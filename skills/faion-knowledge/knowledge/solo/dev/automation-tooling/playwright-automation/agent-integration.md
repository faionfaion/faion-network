# Agent Integration — Playwright Automation

## When to use
- Cross-browser E2E tests (Chromium/Firefox/WebKit) with auto-waiting and trace viewer.
- Agentic web tasks: scraping, login flows, form filling that require JS execution.
- Visual regression testing via `toHaveScreenshot()` snapshots.
- API testing alongside UI in one session (`page.request`).
- Replacing legacy Selenium/Cypress suites for speed and reliability.
- Authenticating once, reusing `storageState` across many headless agent runs.

## When NOT to use
- Pure HTTP scraping where the target renders server-side — use `httpx`/`fetch`, 100x cheaper.
- Mobile-app E2E (use Appium, Detox, Maestro).
- Sub-millisecond unit tests of UI components (use Vitest + Testing Library).
- Targets with hard bot-detection (Cloudflare Turnstile aggressive mode); Playwright's signature is detectable.
- Long-lived stateful sessions (hours) — better suited to a real browser profile, not Playwright contexts.

## Where it fails / limitations
- WebKit headless on Linux still has minor parity gaps with macOS Safari.
- Playwright auto-waits for "actionable", but `page.evaluate` returns immediately — agents hit race conditions.
- Trace viewer huge: a 5-min run can produce 200MB; CI artifacts blow up.
- Codegen produces brittle CSS selectors; agents copy them and tests break next sprint. Prefer role/text locators.
- `page.waitForTimeout` is an antipattern but agents reach for it; use locator auto-wait or `expect(...).toBeVisible({ timeout })`.
- Worker isolation: shared `storageState` across workers causes flakes if not read-only.

## Agentic workflow
A browser agent gets a task ("scrape product table from URL X" or "verify checkout flow"), reads the methodology README, generates a Playwright script using locators (role-based first, CSS as fallback), runs headless with `--trace=on-first-retry`, and on failure attaches the trace + screenshot to the task report. For E2E, use Playwright's test runner; for one-off scrapes, a plain `node script.mjs`. `faion-sdd-executor-agent` can gate the run as a quality check.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps E2E run as a task, fails build on red.
- A composed `browser-agent` (per `automation-tooling/CLAUDE.md` "Used by: faion-browser-agent") for general scraping/automation.

### Prompt pattern
```
Generate a Playwright test in TypeScript for: <user flow description>.
Rules:
- Use page.getByRole / getByLabel / getByText. NO CSS selectors unless no role exists.
- No page.waitForTimeout. Use auto-wait or expect(locator).toBeVisible.
- Save auth via storageState in tests/setup.ts; reuse across tests.
- Headless = true. Trace = 'on-first-retry'. Screenshot = 'only-on-failure'.
- One assertion per behavior. Output: tests/<flow>.spec.ts.
```

```
Login + scrape: navigate <URL>, login with env creds (PW_USER/PW_PASS),
extract the table at selector 'role=table[name="Orders"]', return JSON array.
Save storageState to ./auth.json on success so subsequent runs skip login.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx playwright test` | Test runner with parallel workers | `npm i -D @playwright/test` |
| `npx playwright codegen <url>` | Record actions → script | bundled |
| `npx playwright show-trace trace.zip` | Trace viewer | bundled |
| `npx playwright install --with-deps` | Browsers + system deps | bundled |
| `playwright-mcp` (Microsoft) | MCP server exposing Playwright to LLMs | https://github.com/microsoft/playwright-mcp |
| `npx playwright show-report` | HTML report viewer | bundled |
| `pwdebug` env | Step-through with inspector | `PWDEBUG=1 npx playwright test` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Browserbase | SaaS | Yes — Playwright CDP API | Hosted browsers for agentic workflows; stealth modes. |
| Browserless.io | SaaS + OSS | Yes — Playwright via WS | Self-hostable; ideal for headless-at-scale. |
| Microsoft Playwright Testing | SaaS | Yes — cloud workers | Parallel cross-browser runs from CI. |
| BrowserStack Automate | SaaS | Yes | Real-device cross-browser. |
| Sauce Labs | SaaS | Yes | Enterprise grid. |
| Argos | SaaS + OSS | Yes — CI integration | Visual diffs for Playwright screenshots. |
| Chromatic | SaaS | Partial | Storybook-focused; Playwright support via plugin. |

## Templates & scripts
See `templates.md` and the methodology README for full setups. Headless scrape with auth reuse (≤50 lines):

```javascript
// scrape.mjs — `node scrape.mjs https://target.example/orders`
import { chromium } from 'playwright';
import fs from 'node:fs';

const URL = process.argv[2];
const AUTH = './auth.json';

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  storageState: fs.existsSync(AUTH) ? AUTH : undefined,
  viewport: { width: 1280, height: 720 },
});
const page = await ctx.newPage();

await page.goto(URL, { waitUntil: 'domcontentloaded' });

if (await page.getByRole('button', { name: /sign in/i }).isVisible()) {
  await page.getByLabel('Email').fill(process.env.PW_USER);
  await page.getByLabel('Password').fill(process.env.PW_PASS);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL('**/orders');
  await ctx.storageState({ path: AUTH });
}

const rows = await page.getByRole('row').all();
const data = [];
for (const r of rows.slice(1)) data.push(await r.allInnerTexts());
console.log(JSON.stringify(data, null, 2));
await browser.close();
```

## Best practices
- Always prefer `getByRole` > `getByLabel` > `getByText` > `getByTestId` > CSS. Tests survive UI tweaks.
- Save auth state once via global setup; never login per-test (5x slowdown).
- Configure `expect.toHaveScreenshot.maxDiffPixelRatio` >= 0.01 to absorb font rendering noise.
- Use `--shard=1/4` in CI matrix for fan-out parallelism.
- Run `npx playwright install --with-deps` in CI; missing system libs are the #1 CI failure.
- For agentic scraping, set `userAgent` and `locale` realistic; default UA is `playwright/HeadlessChrome` which gets blocked.

## AI-agent gotchas
- Codegen-generated CSS selectors are tempting but die fast. Force agents to rewrite to role/text after recording.
- LLMs add `await page.waitForTimeout(2000)` "to be safe" — ban it in CI lint rule.
- Locator strict mode: `getByRole('button')` throws if multiple match. Agents catch the error and broaden the selector — wrong fix; narrow with `name:`.
- Storage state contains tokens; agents commit `auth.json` to git. Add to `.gitignore` and pull from secret store.
- Trace artifacts contain screenshots that may include PII; redact or gate behind staging-only.
- Human-in-loop checkpoint: review the first generated test before scaling to full suite — fixing 200 brittle selectors later is worse.
- For agentic web tasks, prefer Microsoft's `playwright-mcp` (MCP server) over hand-rolled scripts; it gives the LLM accessibility-tree snapshots, much more reliable than DOM dumps.

## References
- Playwright docs — https://playwright.dev/
- Playwright Best Practices — https://playwright.dev/docs/best-practices
- playwright-mcp (LLM bridge) — https://github.com/microsoft/playwright-mcp
- Browserbase docs — https://docs.browserbase.com/
- "Cross-browser testing with Playwright" — Microsoft Build 2024.
- Sibling: `web-scraping/`, `puppeteer-automation/`, `browser-automation-overview/`.
