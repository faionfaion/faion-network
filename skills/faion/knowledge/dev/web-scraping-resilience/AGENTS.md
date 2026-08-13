# Web Scraping — Resilience

## Summary

**One-sentence:** Produces a resilience config that wraps the scrape pipeline with jittered rate-limit, exponential-backoff retry capped at 5, safeExtract fallbacks, browser-crash recovery, and anti-detection headers.

**One-paragraph:** Production scrapers need three layers that the development-grade pipeline lacks. (1) Rate-limit with random jitter — fixed-interval requests are a fingerprint sites ban on. (2) Exponential-backoff retry capped at 5 attempts — re-throw on the final to allow caller logging. (3) safeExtract that wraps every page.$eval with timeout + default — a single failing element should not crash the row. Add browser-crash recovery (detect "Target closed" / "Session closed", relaunch) and anti-detection headers (Accept-Language, override navigator.webdriver, stealth plugin where supported). Output is a config artefact + code wrappers; the per-run scrape consumes the config rather than copy-pasting these settings each time.

**Ефективно для:**

- Solo dev whose dev-grade scraper started getting 429-banned in production.
- AI-assisted code review — the rules block "just retry on failure" loops without backoff.
- Long-running scrapes (overnight cron) where a single browser crash should not abort.
- Sources with mild bot-detection (Cloudflare's basic JS challenge level).

## Applies If (ALL must hold)

- Scrape runs unattended (cron, scheduled task).
- Source produces transient failures (timeouts, 5xx, 429).
- Browser-based scraper (Puppeteer / Playwright).
- A target rate exists (requests per minute per domain).

## Skip If (ANY kills it)

- Source has an SLA-backed public API — use it, this is overkill.
- Hardline anti-bot (Cloudflare Turnstile, CAPTCHA at every page) — fundamental rethink needed, not just resilience.
- One-off ad-hoc scrape — manual retry is cheaper.
- Source explicitly forbids scraping AND no legal exception — stop.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target requests/min per domain | int | source policy / robots.txt |
| Browser handle | Puppeteer / Playwright | runtime |
| Anti-detection plugin | npm pkg | playwright-stealth / puppeteer-extra |
| Logger | code | repo |
| Concurrency cap | int | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/web-scraping-agentic-workflow` | Umbrella — resilience is the production-hardening layer. |
| `solo/dev/automation-tooling/web-scraping-pagination` | Pool config consumed by this layer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: jitter, exp-backoff cap 5, safeExtract, crash-recover, anti-detect headers, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for resilience config artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: tight loop, no jitter, infinite retry, webdriver visible | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: probe rate-limit → wire jitter → wire retry → wrap extracts → arm crash-recover | 700 |
| `content/06-decision-tree.xml` | essential | Tree: error-class? → action (jitter, retry, recover, alarm) → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `set-rate-limit` | haiku | Mechanical: requests/min cap + jitter window. |
| `wire-retry` | sonnet | Coding task: exp-backoff with jitter. |
| `wrap-safe-extract` | sonnet | Helper authoring with sensible defaults. |

## Templates

| File | Purpose |
|------|---------|
| `templates/web-scraping-resilience.json` | JSON Schema for the resilience config artefact. |
| `templates/safe-extract.ts` | safeExtract + retryWithBackoff helpers in TypeScript. |
| `templates/anti-detect.ts` | Header set + navigator.webdriver override + stealth plugin wiring. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-web-scraping-resilience.py` | Validate the resilience config JSON against schema + consistency rules. | On scrape start; nightly in CI. |

## Related

- [[web-scraping-agentic-workflow]] — umbrella.
- [[web-scraping-pagination]] — pool config consumed here.
- [[web-scraping-element-extraction]] — safeExtract wraps it.

## Decision tree

See `content/06-decision-tree.xml`. The tree classifies the error class observed during the run (transient 5xx, 429 rate-limit, timeout, browser crash, captcha) and routes to the matching action: jitter+retry, back-off doubled, page recover, browser relaunch, or human-escalate. Leaves emit `apply`, `escalate-human`, or `block-fatal`. Each leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/web-scraping-resilience.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/web-scraping-resilience.json",
  "type": "object",
  "required": [
    "artefact_id",
    "source",
    "delay_ms_min",
    "delay_ms_max",
    "max_retries",
    "base_delay_ms",
    "safe_extract_timeout_ms",
    "anti_detect_enabled",
    "crash_recover_enabled",
    "concurrency_cap",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^wsrr-[a-z0-9-]{6,}$"
    },
    "source": {
      "type": "string",
      "minLength": 1
    },
    "delay_ms_min": {
      "type": "integer",
      "minimum": 100,
      "maximum": 60000
    },
    "delay_ms_max": {
      "type": "integer",
      "minimum": 100,
      "maximum": 60000
    },
    "max_retries": {
      "type": "integer",
      "minimum": 0,
      "maximum": 5
    },
    "base_delay_ms": {
      "type": "integer",
      "minimum": 100,
      "maximum": 10000
    },
    "safe_extract_timeout_ms": {
      "type": "integer",
      "minimum": 100,
      "maximum": 5000
    },
    "anti_detect_enabled": {
      "type": "boolean"
    },
    "crash_recover_enabled": {
      "type": "boolean"
    },
    "concurrency_cap": {
      "type": "integer",
      "minimum": 1,
      "maximum": 50
    },
    "stealth_lib": {
      "type": [
        "string",
        "null"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/safe-extract.ts`

```typescript
export interface ResilienceConfig {
  delay_ms_min: number;
  delay_ms_max: number;
  max_retries: number;
  base_delay_ms: number;
  safe_extract_timeout_ms: number;
}

export async function safeExtract<T>(
  fn: () => Promise<T>,
  defaultValue: T,
  timeoutMs: number = 5000
): Promise<T> {
  try {
    const timeout = new Promise<T>((_, rej) =>
      setTimeout(() => rej(new Error("safe-extract-timeout")), timeoutMs)
    );
    return await Promise.race([fn(), timeout]);
  } catch (_) {
    return defaultValue;
  }
}

export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  cfg: Pick<ResilienceConfig, "max_retries" | "base_delay_ms">
): Promise<T> {
  let lastErr: unknown;
  for (let attempt = 0; attempt <= cfg.max_retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (attempt === cfg.max_retries) break;
      const delay = cfg.base_delay_ms * 2 ** attempt + Math.floor(Math.random() * 1000);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw lastErr;
}

export async function jitteredSleep(min: number, max: number): Promise<void> {
  const ms = min + Math.floor(Math.random() * (max - min));
  return new Promise(r => setTimeout(r, ms));
}
```

### `templates/anti-detect.ts`

```typescript
import type { BrowserContext } from "playwright";

const USER_AGENTS = [
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
];

export async function applyAntiDetect(ctx: BrowserContext): Promise<void> {
  const ua = USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
  await ctx.setExtraHTTPHeaders({
    "User-Agent": ua,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  });

  await ctx.addInitScript(() => {
    // navigator.webdriver -> undefined
    Object.defineProperty(navigator, "webdriver", { get: () => undefined });
    // plugins must look populated
    Object.defineProperty(navigator, "plugins", { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, "languages", { get: () => ["en-US", "en"] });
  });
}
```
