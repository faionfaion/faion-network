# Agent Integration — Browser Automation Overview

## When to use
- Choosing between Puppeteer and Playwright for a new automation/scraping/E2E project — this overview is the routing layer.
- Onboarding a new project that needs headless browser tasks (PDF, screenshots, form fill, scraping, E2E).
- Triaging an existing browser-automation codebase: which tool is in use, where are the gaps vs the canonical pattern files.
- Centralizing browser-automation knowledge for a single agent that will fan out to one of three sibling skills.

## When NOT to use
- For deep how-to: jump directly to `puppeteer-automation/`, `playwright-automation/`, or `web-scraping/`. This file is an index.
- For mobile app automation (Appium, Detox, Maestro). Those are not browser tools.
- For API-only testing — use `api-testing` patterns; spinning up a browser is wasteful.
- For browser fingerprinting / strong anti-bot evasion at scale — that's a specialist domain (residential proxies, real-browser farms) beyond this overview.
- For accessibility audits — Lighthouse / axe-core have purpose-built drivers; Playwright integration is fine but the audit logic is not in this file.

## Where it fails / limitations
- The file is a 100-line router; all real patterns live in the three child files. Agents must read the chosen child file before producing code.
- Comparison table is correct as of 2024-2025 but does not capture: Playwright's Chrome-only `chromium-headless-shell` (faster, smaller), Puppeteer's official Firefox channel (still labelled experimental), or BiDi protocol convergence.
- "Stealth mode" via `puppeteer-extra-plugin-stealth` is a moving target; bot defences improve faster than the plugin.
- No coverage of resource limits (memory leaks per browser context), Docker base images, or CI parallelism — those bite hard in production.
- "PDF/screenshot generation" lumped under Puppeteer is fine, but Playwright now matches feature parity.
- No guidance on running in serverless (Lambda layer for Chromium, Cloudflare Browser Rendering, Browserless) — major omission for solopreneur stacks.

## Agentic workflow
Use a routing agent: it reads the user request, picks Puppeteer vs Playwright using the comparison table, then delegates to the corresponding sibling skill's deeper file. Keep browser execution in a sandboxed worker (its own container or `--no-sandbox` is for desktop-only; in CI use `--disable-dev-shm-usage`). Always run with a timeout per page action; agents that lack timeouts hang CI for hours. For scraping at scale, route through a managed browser pool (Browserless, Bright Data, Apify) rather than letting an agent fork dozens of local Chrome instances.

### Recommended subagents
- `general-purpose` — initial language/tool decision and bootstrap.
- `faion-browser-agent` (mentioned in the README) — actual page automation; keep it Sonnet-tier; only escalate to Opus for selector-design or anti-bot reasoning.
- A narrow `selector-stabilizer` task agent — converts brittle CSS selectors to role/text/data-testid; optional pass.
- A `screenshot-diff` task agent — paired with Percy/Chromatic/Playwright trace viewer for visual regression.

### Prompt pattern
```
Read solo/dev/automation-tooling/browser-automation-overview/README.md.
The task is: <task>. Decide tool (Puppeteer/Playwright) using the comparison
table; justify in one paragraph. Then read the relevant sibling
(puppeteer-automation/ or playwright-automation/) and produce a runnable
script with: timeout per action, browser-launch flags suitable for Linux CI,
explicit cleanup in finally, and a non-zero exit code on selector miss.
```
```
Audit <repo> for browser automation. Catalogue: tool used, version, headless
mode, timeouts, retry policy, container base, parallelism. Flag missing
items vs the overview's "When to Use What" guidance.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx puppeteer browsers install chrome` | Pin Chromium binary | pptr.dev |
| `npx playwright install --with-deps` | Install browsers + Linux deps for CI | playwright.dev |
| `npx playwright codegen <url>` | Record a test by clicking | playwright.dev |
| `npx playwright show-trace trace.zip` | Open a trace + screenshots + DOM snapshots | playwright.dev |
| `npx puppeteer screenshot <url>` (via Puppeteer CLI projects) | Quick screenshot from CLI | n/a (homegrown) |
| `chromium --headless=new --dump-dom <url>` | Bare browser for sanity checks | apt-get chromium |
| `chrome-launcher` | Programmatic Chrome launch with sane defaults | npm |
| `lighthouse` / `lighthouse-ci` | Run perf/a11y audits driven by headless Chrome | npm |
| `playwright-mcp` | MCP server exposing Playwright as agent tools | github.com/microsoft/playwright-mcp |
| `puppeteer-mcp` (community) | MCP variant for Puppeteer | varies |
| `bx browserless-cli` | Manage remote Browserless workers | browserless.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Browserless | SaaS + OSS (self-host) | Yes | Hosted Chrome over WS; agents connect with `puppeteer.connect()` / Playwright `browserType.connect()`. |
| Cloudflare Browser Rendering | SaaS | Yes | REST + Workers binding; pay-per-use; weak BiDi. |
| Apify | SaaS | Yes | Actor model + proxy + storage; managed crawls. |
| Bright Data Scraping Browser | SaaS | Yes | Real-browser pool with residential IPs; CDP-compatible. |
| Browserbase | SaaS | Yes | Headless Chrome over CDP for AI agents; built for LLM-driven flows. |
| Steel.dev | SaaS + OSS | Yes | Browser-as-a-service tuned for agents; session replay. |
| ScrapingBee / ScraperAPI / Zyte | SaaS | Partial | Proxy + render APIs; less control than CDP. |
| Vercel/Netlify build "headless Chrome" support | SaaS | Partial | Works but cold-start hostile; prefer dedicated. |
| AWS Lambda + chrome-aws-lambda layer | SaaS | Yes | Cheap on-demand; size limits + cold start. |
| GitHub Actions runners | SaaS | Yes | `microsoft/playwright-github-action` is one line. |
| Sauce Labs / BrowserStack | SaaS | Partial | Real-device cross-browser; agent automation possible but per-minute pricing. |
| Selenium Grid 4 | OSS | Yes | If team is on Selenium; Grid hubs CDP-compatible. |

## Templates & scripts
See sibling skills for full templates. Minimum decision script for the routing agent:

```javascript
// scripts/decide-browser.js — pick Puppeteer vs Playwright
const requirements = {
  crossBrowser: false,        // need Firefox/WebKit?
  e2eTesting: false,          // running as test suite?
  videoTrace: false,          // need video / trace capture?
  scraping: true,             // primary task is data extraction?
  rolesA11y: false,           // need role/accessibility selectors?
};
const playwrightScore =
  (requirements.crossBrowser ? 3 : 0) +
  (requirements.e2eTesting   ? 2 : 0) +
  (requirements.videoTrace   ? 2 : 0) +
  (requirements.rolesA11y    ? 2 : 0);
const puppeteerScore = (requirements.scraping ? 2 : 0) + 1; // tie-break: simpler
console.log(playwrightScore >= puppeteerScore ? 'playwright' : 'puppeteer');
```

## Best practices
- Always set per-action timeouts (`page.setDefaultTimeout(15000)`) — silent hangs eat agent budget.
- Launch with `--disable-dev-shm-usage --disable-gpu --no-sandbox` only inside trusted containers.
- One browser context per concurrent task; do not share cookies between unrelated jobs.
- Capture trace+screenshot on failure; throw away on success — disk fills fast.
- Pin browser binary version in `package.json` (`puppeteer.browsers`) or `playwright.config.ts` so CI is reproducible.
- For scraping, set a realistic UA + viewport + accept-language; randomize subtly across runs.
- For E2E, prefer role/text selectors over CSS class chains — they survive UI refactors.
- In CI, run with `--workers=N` matching CPU cores; over-parallelism crashes Chrome with OOM.
- Use a remote browser service (Browserless/Browserbase) when running >20 parallel sessions — local resource contention dominates.

## AI-agent gotchas
- Selector design: agents glue together long CSS chains that break on the next deploy. Force role/text/data-testid first.
- Agents reflexively add `await page.waitForTimeout(2000)` instead of `waitForSelector`/`waitForLoadState`. Banish `waitForTimeout` from the codebase via lint rule.
- "Click then read" race: agents read DOM before navigation completes. Always `Promise.all([page.waitForNavigation(), page.click(...)])` (Puppeteer) or use Playwright's auto-wait.
- Headless detection: agents copy "stealth" snippets from blog posts that defeat 2022 bot defences and fail today. If the target has serious anti-bot, route through a managed browser farm.
- Memory: agents forget to `await browser.close()` in error paths. Wrap in `try/finally`.
- File downloads: agents miss the platform-specific download path; use `page.waitForEvent('download')` (Playwright) or CDP `Browser.downloadBehavior` (Puppeteer).
- Cookies / auth: agents will paste real session cookies into the script. Force a `storageState.json` file gitignored.
- For scraping: agents over-rotate user agents and cause more bans, not fewer; rate-limit + sticky session is the better lever.
- Cross-browser: agents claim "this works in Chromium" and ship it as Playwright cross-browser. Always run the matrix in CI.

## References
- Puppeteer: https://pptr.dev/
- Playwright: https://playwright.dev/
- Playwright MCP: https://github.com/microsoft/playwright-mcp
- Browserless: https://browserless.io/
- Browserbase: https://browserbase.com/
- Sibling: `solo/dev/automation-tooling/puppeteer-automation/`, `playwright-automation/`, `web-scraping/`.
- W3C WebDriver BiDi: https://www.w3.org/TR/webdriver-bidi/
