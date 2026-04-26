# Agent Integration — Puppeteer Automation

## When to use
- Headless Chrome scripting jobs that need DevTools Protocol features (CDP sessions, request interception, coverage, tracing).
- Generating PDFs / screenshots from rendered HTML inside a Node-only pipeline.
- Light scraping where stealth is already handled (reCAPTCHA-free targets) and you want minimum dependencies.
- Running on serverless (chromium binary via `@sparticuz/chromium`) where Playwright bundles are too large.

## When NOT to use
- Cross-browser testing — use Playwright (Firefox + WebKit are first-class there, Puppeteer is Chromium-only since the Firefox driver was deprecated).
- E2E test suites with parallelism, retries, fixtures — Playwright Test or Cypress give you that for free.
- Long-running scraping farms against bot-defended targets — switch to Playwright + `playwright-extra`/stealth, or a managed service.
- Anything where the agent must sustain a session past a single tool call without a stateful runner.

## Where it fails / limitations
- Chromium-only. Firefox protocol support is no longer maintained.
- `headless: 'new'` changes selector behaviour vs. `false` — flaky scripts often pass headed and fail headless.
- `waitUntil: 'networkidle0'` hangs forever on sites with long-poll/WebSocket traffic; agents loop until timeout.
- `puppeteer-extra-plugin-stealth` lags behind Cloudflare/Datadome detection; expect arms-race.
- Single browser instance leaks RAM under churn — must `browser.close()` and recycle every N pages.
- Chrome auto-update via `puppeteer` install can break CI if the bundled version drifts; pin via `PUPPETEER_SKIP_DOWNLOAD` + a manual chromium path.

## Agentic workflow
Drive Puppeteer from a worker process the agent invokes via Bash, not from inside the LLM turn. The agent writes a script (or fills a parametric template), launches it with a hard timeout, captures `console`/screenshots/HAR to disk, then reads structured artifacts back. Long sessions belong in a daemonised runner the agent talks to over a queue or HTTP — keep the LLM stateless.

### Recommended subagents
- General-purpose Bash-driven worker — no project-specific Puppeteer agent exists yet; the closest fit is `faion-sdd-executor-agent` for one-shot script generation + execution.
- Pair with `password-scrubber-agent` before logging artifacts that may include cookies, headers, or filled credentials.

### Prompt pattern
```
Write a Node script at /tmp/scrape.js that:
- launches puppeteer-extra with stealth plugin
- navigates to {URL}, waits for selector "{S}"
- emits { title, h1, status } as JSON to stdout
- exits non-zero on any thrown error
Run it with `timeout 60 node /tmp/scrape.js > out.json`.
Return the JSON only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `puppeteer` | Bundled Chromium driver | `npm i puppeteer` · https://pptr.dev |
| `puppeteer-core` | Driver without bundled browser | `npm i puppeteer-core` |
| `puppeteer-extra` + `puppeteer-extra-plugin-stealth` | Bot-detection evasion | `npm i puppeteer-extra puppeteer-extra-plugin-stealth` |
| `@sparticuz/chromium` | Lambda/Cloud Run compatible chromium | `npm i @sparticuz/chromium` |
| `chrome-aws-lambda` (legacy) | Older serverless chromium | superseded by `@sparticuz/chromium` |
| `pageres-cli` | One-shot screenshot CLI built on Puppeteer | `npm i -g pageres-cli` |
| `lighthouse` (CLI) | Audits pages via Puppeteer-driven Chrome | `npm i -g lighthouse` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Browserless.io | SaaS | Yes — REST/WS endpoints | Drop-in `puppeteer.connect({ browserWSEndpoint })`; bills per second. |
| ScrapingBee / ScraperAPI | SaaS | Yes — HTTP API | Hides Puppeteer behind a request; good when you only need the HTML. |
| Bright Data Scraping Browser | SaaS | Yes — WS endpoint | Bundles residential proxies + unlock; $$$ but defeats most anti-bot. |
| Apify | SaaS/OSS SDK | Yes — actors expose HTTP | Crawlee SDK wraps Puppeteer/Playwright with queues, retries, proxies. |
| Browserless self-hosted | OSS Docker | Yes | Run `ghcr.io/browserless/chromium` for shared, sandboxed instances. |
| Rendertron | OSS | Yes | Headless render-as-service for SSR/SEO; abandoned by Google but still works. |

## Templates & scripts
Inline minimal harness an agent can drop into a tool call:

```javascript
// /tmp/run.js — usage: node run.js <url>
const puppeteer = require('puppeteer-extra');
const Stealth = require('puppeteer-extra-plugin-stealth');
puppeteer.use(Stealth());

(async () => {
  const url = process.argv[2];
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  try {
    const page = await browser.newPage();
    await page.setDefaultTimeout(15000);
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
    const data = await page.evaluate(() => ({
      title: document.title,
      h1: document.querySelector('h1')?.innerText ?? null,
    }));
    process.stdout.write(JSON.stringify({ status: resp.status(), ...data }));
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e.message); process.exit(1); });
```

See `templates.md` for richer launchers (proxy pool, mobile emulation, PDF).

## Best practices
- Always `await browser.close()` in `finally` — orphan Chromium processes pin GBs.
- Prefer `domcontentloaded` + explicit `waitForSelector` over `networkidle0` for SPA targets.
- Block images/fonts/stylesheets via `setRequestInterception` when you only need DOM data — 3-5x speedup.
- Persist a `userDataDir` per logical identity, not per run — avoids re-doing logins and warms HSTS/cache.
- Use `page.exposeFunction()` to call back into Node from page scripts instead of polling for DOM mutations.
- Set `process.env.PUPPETEER_CACHE_DIR` to a writable path in CI; default `~/.cache/puppeteer` breaks in read-only containers.
- Pin chromium revision (`puppeteer.executablePath()` + lockfile) so headless behaviour is reproducible across agent runs.

## AI-agent gotchas
- The model often writes `await page.waitForTimeout(N)` (deprecated removed in Puppeteer 22) — instruct it to use `new Promise(r => setTimeout(r, N))` or proper `waitForSelector`.
- Selectors generated from screenshots are unstable; require the agent to fetch DOM via `page.content()` first and pick attribute-based selectors.
- LLMs love `networkidle0`; it is a foot-gun on auth/analytics-heavy pages. Force `domcontentloaded` + targeted waits in prompts.
- Stealth plugin can change navigator props the agent later asserts on — pick one stance and stick with it.
- Human-in-loop checkpoint: any flow involving credentials, captchas, or 2FA must pause and surface a screenshot; never let the agent loop on a login form.
- Cost trap on managed services (Browserless): unbounded retries on 429s burn budget fast; set `--max-retries=2` and circuit-break on 4xx.
- File downloads: Puppeteer's CDP `Page.setDownloadBehavior` is per-session; agents that recycle pages without re-issuing it lose the path silently.

## References
- https://pptr.dev — official docs
- https://github.com/berstend/puppeteer-extra — extras + stealth
- https://github.com/Sparticuz/chromium — serverless chromium build
- https://crawlee.dev — Apify Crawlee (Puppeteer + Playwright crawlers)
- https://www.browserless.io/docs — managed browser API
