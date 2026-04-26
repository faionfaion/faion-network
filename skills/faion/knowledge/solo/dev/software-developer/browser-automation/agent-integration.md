# Agent Integration — Browser Automation

## When to use
- E2E testing of web apps (faion-net-e2e Playwright suite, neromedia preview verification).
- Scraping public sites without an API: news feeds, marketplaces, regulator portals.
- Programmatic screenshot/PDF generation for reports, OG cards, invoice rendering.
- Form fill + submit automation for portals lacking an API (gov, banks, partner dashboards).
- Visual regression on Storybook builds — `storybook.faion.net` snapshot diffs.
- AI-agent-driven web tasks: book a flight, fill a form, click through a wizard the human dictated.

## When NOT to use
- The site offers an API (REST/GraphQL/RSS) — always prefer the API; browser automation is brittle and slow.
- Sites with strong anti-bot (Cloudflare Turnstile, PerimeterX, DataDome) — fight cost > value, use official partner channel or commercial scrape API.
- High-throughput scraping (>100 pages/sec) — use HTTP-only scraping (`httpx`, `scrapy`) without a browser.
- Tasks requiring credentials you don't legitimately own — illegal/unethical, do not script.
- Behind-VPN or zero-trust portals where headless browser fingerprint trips MFA.

## Where it fails / limitations
- Headless detection: `navigator.webdriver`, missing fonts, missing GPU, broken `chrome.runtime` — sites detect and serve different content.
- Selectors break on every redesign; CSS-class-based selectors are especially fragile (Tailwind hash classes).
- Timing flakiness: race between SPA hydration, animations, lazy loads, and your `click()`. Auto-wait helps, doesn't eliminate.
- Memory leaks under long runs: each `newPage()` accumulates, kill the browser every N pages.
- Captchas: hCaptcha/reCAPTCHA cannot be solved reliably; commercial solvers are expensive and ToS-questionable.
- File downloads to ephemeral paths in headless mode — CDP `Page.setDownloadBehavior` differs across versions.
- Cookies/localStorage isolation between contexts; agents reuse one context and leak auth state across tasks.
- Native dialogs (auth prompt, file picker on `<input type="file">` chooser) require special handlers.

## Agentic workflow
Drive browser tasks as: (1) agent inspects target page (DOM dump, accessibility tree), (2) generates a Page Object Model file, (3) writes the action script using POM, (4) runs in headed mode locally for one iteration to verify, (5) switches to headless for CI/cron. For scraping: emit JSON Schema first, then write extractor; LLM never invents fields not in schema. Pair Playwright Trace Viewer with the agent — feed back failed traces for self-repair.

### Recommended subagents
- `faion-browser-agent` — primary executor, owns Puppeteer/Playwright invocation.
- `faion-frontend-component-agent` — when automating Storybook for visual capture.
- `faion-sdd-executor-agent` — wraps automation flows under SDD when they're test/quality artifacts.

### Prompt pattern
```
Inspect <url> in headed Playwright. Output: (1) accessibility tree of the
visible viewport, (2) form fields with current values, (3) primary CTA buttons
with their `role=` selectors. Do not click anything yet.
```

```
Given the target schema {title:string, price:number, sku:string},
generate a Playwright extractor against <selector_root>. Use locator
`role=` and `text=` selectors before CSS. After running, validate result
with zod/pydantic; on schema fail, dump page.content() and report.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx playwright` | Test runner, codegen, trace viewer, browser install | npm i -D @playwright/test; npx playwright install |
| `npx playwright codegen <url>` | Record actions → generates script | bundled |
| `npx playwright show-trace trace.zip` | Inspect failed run timeline | bundled |
| `puppeteer` | Chrome-only DevTools automation | npm i puppeteer |
| `chromedp` | Go bindings to Chrome DevTools | go get github.com/chromedp/chromedp |
| `selenium` + `geckodriver`/`chromedriver` | Cross-browser, legacy stacks | https://www.selenium.dev |
| `webrecorder/browsertrix` | High-fidelity archival crawl | https://browsertrix.com |
| `lighthouse-cli` | Audit accessibility/perf via headless Chrome | npm i -g lighthouse |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Browserbase | SaaS | yes (SDK) | Headless cloud + stealth + session replay; Anthropic uses it in Claude computer-use demos. |
| Browserless.io | SaaS | yes (REST + WS) | `puppeteer.connect()`-compatible, scales horizontally. |
| Playwright Cloud (Microsoft) | SaaS | yes | Hosted browsers + parallel runners. |
| BrowserStack/Sauce Labs | SaaS | yes (API) | Real-device cross-browser; expensive but only option for IE/Safari edge cases. |
| ScrapingBee / ScraperAPI / ZenRows | SaaS | yes (REST) | "Scrape-as-a-service"; handles proxies + JS render + captchas. |
| Apify | SaaS | yes (Actor API) | Pre-built scrapers + serverless runners. |
| Bright Data Web Unlocker | SaaS | yes | Premium anti-block + residential proxies. |
| Selenium Grid | OSS | yes | Self-host parallel browsers; pair with k8s. |

## Templates & scripts
See `templates.md` for full POM scaffold. Inline minimal Playwright extractor:

```javascript
// scripts/extract.js — npx playwright install chromium first
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
    userAgent: 'Mozilla/5.0 (compatible; faion-bot/1.0)',
  });
  const page = await context.newPage();
  await page.route('**/*.{png,jpg,svg,woff2}', (r) => r.abort());

  await page.goto(process.env.URL, { waitUntil: 'networkidle' });
  const raw = await page.locator('article.product').evaluateAll((els) =>
    els.map((e) => ({
      title: e.querySelector('h2')?.textContent?.trim(),
      price: parseFloat(e.querySelector('.price')?.textContent?.replace(/[^0-9.]/g, '')),
      url: e.querySelector('a')?.href,
    })),
  );

  const items = raw.map((r, i) => {
    const result = Item.safeParse(r);
    if (!result.success) console.error(`row ${i} skipped:`, result.error.flatten());
    return result.success ? result.data : null;
  }).filter(Boolean);

  console.log(JSON.stringify(items, null, 2));
  await browser.close();
})();
```

## Best practices
- Prefer `role=` and `text=` locators over CSS — survive class/styling refactors.
- Always pass `waitUntil: 'networkidle'` for SPAs; use `domcontentloaded` only for static pages.
- Block images/fonts/analytics on scraping runs — 3-5x speedup, drops bandwidth ~80%.
- Persist auth via `context.storageState({ path })` and reuse — login flows are fragile, run them once.
- Wrap every action in retry-with-backoff; use `expect.poll(...).toPass()` for flaky assertions.
- Run headed in dev (`PWDEBUG=1`), headless in CI; never debug a headless flake without `trace: 'on-first-retry'`.
- Keep one POM file per page; never put selectors inline in tests — selectors change, tests shouldn't.
- Set `slowMo: 50-100` only for demo/recording; production headless should be 0.
- Use `--shard=N/M` for CI parallelism; Playwright handles it natively.
- Honor `robots.txt` for scraping; rate-limit yourself even when site doesn't enforce.

## AI-agent gotchas
- Agents love `page.waitForTimeout(2000)` — explicitly forbid in prompts; require condition-based waits (`waitForSelector`, `waitForResponse`).
- LLMs generate selectors from imagined HTML — feed them the actual DOM (`page.content()` or accessibility tree) before asking for selectors.
- Self-improving agents that retry failed runs can OOM the host by spawning N browsers; cap concurrency in launcher with semaphore.
- Stealth plugins are an arms race; agents pulling latest `puppeteer-extra-plugin-stealth` may break on patch updates — pin versions and re-validate weekly.
- When agent runs scrape against JS-rendered SPA, it sees pre-hydration HTML if it doesn't await network idle — leads to "site is empty" hallucination.
- Captcha appearance is silent — page just shows challenge; agent times out after 30s with no diagnostic. Add screenshot-on-error and detect challenge URLs (`/challenges/`, `cf-mitigated`).
- Human-in-loop checkpoint: any flow involving payment, account creation, or destructive form submit (delete, transfer) — pause and ask human to confirm the rendered form before submit.
- Computer-use models (Claude 3.5+) can drive Playwright via screenshots; for non-deterministic UIs that's better than selector-based scripts. Use `Browserbase` or local CDP.

## References
- Playwright docs — https://playwright.dev
- Puppeteer docs — https://pptr.dev
- Browserbase + Claude — https://docs.browserbase.com/integrations/claude
- Anthropic computer-use overview — https://docs.anthropic.com/en/docs/build-with-claude/computer-use
- "Web scraping ethics" (Apify) — https://blog.apify.com/is-web-scraping-legal/
- `puppeteer-extra-plugin-stealth` — https://github.com/berstend/puppeteer-extra
- Playwright Trace Viewer — https://playwright.dev/docs/trace-viewer
