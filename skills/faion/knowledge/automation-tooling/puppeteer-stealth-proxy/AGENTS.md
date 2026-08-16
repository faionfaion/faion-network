# Puppeteer Stealth & Proxy

## Summary

**One-sentence:** Produces a Puppeteer stealth + proxy layer using one documented evasion stance (plugin or manual, never both), proxy rotation with circuit breaker on 4xx, and bounded retries.

**One-paragraph:** Stealth and proxy mistakes have one root cause: layering. This methodology requires picking exactly one evasion stance (puppeteer-extra-plugin-stealth alone OR manual navigator overrides alone) and documenting it. Proxy rotation uses a small bounded pool with health checks; 429/403 responses trip a circuit breaker that surfaces to the caller instead of silent looping. The artefact is the stealth + proxy config metadata; the validator enforces the canonical fields.

**Ефективно для:**

- Scrapers against targets with mild bot detection (signature checks, no Turnstile).
- Pipelines requiring rotating IPs for rate-limit avoidance.
- Workers using managed browser services (Browserless, ScrapingBee) with retry policies.
- Auditing existing scripts that mix stealth plugin + manual overrides (and breaking from there).

## Applies If (ALL must hold)

- Target has signature-based bot detection (navigator props, WebGL fingerprint) but not aggressive challenge pages.
- Run budget allows multiple retries against rate-limited responses.
- Proxy pool available (residential or DC) with health monitoring.
- Worker can surface circuit-breaker trips to the caller.

## Skip If (ANY kills it)

- Targets with hardened bot defence (Cloudflare Turnstile aggressive, Akamai BMP) — use a managed solver instead.
- Public APIs with documented rate limits — call the API, not the page.
- Local dev where no proxy is needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stealth stance choice | plugin | manual | none | team decision |
| Proxy pool | list of endpoints + auth + health URL | ops provided |
| Retry policy | max retries + backoff + circuit-breaker threshold | task brief |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[puppeteer-launch-setup]] | launch wrapper accepts proxy + extra args |
| [[puppeteer-agent-workflow]] | worker exits non-zero with status on circuit breaker |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-stance` | sonnet | decide plugin vs manual; document it |
| `emit-proxy-rotator` | sonnet | render small pool + health check + circuit breaker |
| `audit-evaluate-assertions` | haiku | scan page.evaluate calls for navigator-prop asserts that mismatch the stance |

## Templates

| File | Purpose |
|------|---------|
| `templates/stealth-worker.ts` | Stealth-plugin-only worker (stance documented at top) |
| `templates/proxy-pool.ts` | Small proxy pool with health-check + circuit breaker |
| `templates/retry.ts` | Bounded retry helper with exponential backoff |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-puppeteer-stealth-proxy.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-launch-setup]]
- [[puppeteer-page-interaction]]
- [[puppeteer-session-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/stealth-worker.ts`

```typescript
// STEALTH STANCE: plugin-only.
// Reason: puppeteer-extra-plugin-stealth is the maintained baseline. We do not
// stack manual navigator overrides on top; assertions never depend on overridden props.
import puppeteer from 'puppeteer-extra';
import Stealth from 'puppeteer-extra-plugin-stealth';
puppeteer.use(Stealth());

export async function launch(opts: { proxyHost?: string } = {}) {
  const args = ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'];
  if (opts.proxyHost) args.push(`--proxy-server=${opts.proxyHost}`);
  return puppeteer.launch({ headless: 'new', args });
}
```

### `templates/proxy-pool.ts`

```typescript
import fetch from 'node-fetch';

export interface Proxy { host: string; auth?: { user: string; pass: string } }

export async function healthy(pool: Proxy[], probeUrl: string, timeoutMs = 5000): Promise<Proxy[]> {
  const out: Proxy[] = [];
  for (const p of pool) {
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), timeoutMs);
      const res = await fetch(probeUrl, { signal: ctrl.signal });
      clearTimeout(t);
      if (res.ok) out.push(p);
    } catch { /* dead proxy */ }
  }
  return out;
}

export class CircuitBreaker {
  private fails = 0;
  constructor(private threshold = 5) {}
  recordFail() { this.fails++; }
  reset() { this.fails = 0; }
  open(): boolean { return this.fails >= this.threshold; }
}
```

### `templates/retry.ts`

```typescript
export async function retry<T>(fn: () => Promise<T>, max = 2, baseMs = 500): Promise<T> {
  let lastErr: unknown;
  for (let i = 0; i <= max; i++) {
    try { return await fn(); }
    catch (e) {
      lastErr = e;
      if (i === max) break;
      await new Promise((r) => setTimeout(r, baseMs * 2 ** i));
    }
  }
  throw lastErr;
}
```

### `templates/artefact.json`

```json
{
  "stance": "plugin",
  "stance_documented": true,
  "max_retries": 2,
  "circuit_breaker": true,
  "proxy_pool_size": 8,
  "proxy_health_check": true,
  "proxy_auth_method": "authenticate_api"
}
```
