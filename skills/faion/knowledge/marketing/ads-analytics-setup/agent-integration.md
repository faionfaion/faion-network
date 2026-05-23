# Agent Integration — Analytics Setup

## When to use
- New site/app launch needing GA4 + ad-platform pixels installed correctly from day one.
- Migration from Universal Analytics to GA4 (UA was sunset in 2023; agents validate event mapping).
- Multi-channel attribution rebuild — installing UTM standards, dataLayer schema, conversion definitions.
- E-commerce or SaaS rolling out enhanced ecommerce / product analytics.
- Compliance refit (consent mode v2, GDPR/CCPA cookie banners, server-side tagging migration).

## When NOT to use
- Sites already with a working analytics stack and consistent UTM data — focus on optimization, not reinstall.
- Pure backend / API-only products with no front-end (use server-side analytics like PostHog Backend, not GA4).
- Privacy-first or low-traffic projects where Plausible/Fathom is sufficient — avoid GA4 over-engineering.
- One-page marketing sites — Plausible/Fathom + UTM macros suffice; GA4 is overkill.

## Where it fails / limitations
- GA4's event model is fundamentally different from UA's session model; reports look unfamiliar and quotas (cardinality, custom dimensions) bite at scale.
- BigQuery export is the ONLY way to get raw event data; standard UI sampled above 10M events.
- Consent Mode v2 (mandatory in EEA from March 2024) without proper signaling causes 30-50% conversion loss in reports.
- iOS Safari ITP and intelligent tracking preventions cap first-party cookies at 7 days; client-side attribution decays fast.
- gtag/GTM async loading races with single-page-app history events — `page_view` can fire before route is settled.
- Server-side tagging requires GCP infra and adds latency; wrong setup leaks PII to ad pixels.
- Cross-domain tracking requires explicit `linker` config — silent breakage common after redesigns.

## Agentic workflow
A subagent owns the analytics-install lifecycle: audit current state → produce dataLayer + event spec → generate GTM container JSON → review with human → push to staging → run automated event-fire tests (Playwright + GA Debug View API) → promote to prod. Heavy human-in-loop on: consent banner copy, PII filtering rules, conversion designation. Use Tag Assistant Companion for screenshots in the audit step.

### Recommended subagents
- A `gtm-builder` subagent — generates GTM JSON containers from a dataLayer spec, including triggers, variables, tags, and built-in events.
- A `analytics-auditor` — crawls site with headless browser, captures all `gtag`/`dataLayer.push`/network calls, diffs against spec.
- `faion-sdd-executor-agent` (existing) — runs install as SDD feature with acceptance criteria ("all 12 conversion events fire on staging without errors").
- `faion-ads-agent` — links GA4 → Google Ads, uploads conversion definitions.

### Prompt pattern
```
You are an analytics tracking-spec author.
Input: product description, key conversion actions, business model (saas|ecom|leadgen).
Output JSON spec:
- events: [{name, trigger, params, fire_on_pages, conversion: bool}]
- custom_dimensions: [{name, scope, source}]
- consent_categories: [...]
Validate GA4 reserved event names. No more than 50 custom events.
```

```
Validate event firing on staging.
Page list: <urls>. Expected events: <names>. Use Playwright + window.dataLayer interception.
Output PASS/FAIL per event with screenshot of GA4 DebugView.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Google Tag Assistant Companion | Validate tags fire correctly | tagassistant.google.com |
| GTM Server-Side preview | Test server-tag config before deploy | tagmanager.google.com |
| `gtag.js` debug | URL `?gtm_debug=1` reveals tag state | docs |
| Playwright + dataLayer hook | E2E event-fire tests | `npm i playwright` |
| `bq` CLI | Query GA4 BigQuery export | cloud.google.com/bigquery/docs/bq-command-line-tool |
| Measurement Protocol API | Server-side event posting | developers.google.com/analytics/devguides/collection/protocol/ga4 |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Tag Manager | SaaS native | Yes — API + container JSON | Standard install vehicle |
| Segment | SaaS | Yes — API | Routes events to GA4 + Mixpanel + ad pixels |
| Rudderstack | OSS / SaaS | Yes — API | Open-source Segment alternative |
| Mixpanel | SaaS | Yes — API + ingest | Product analytics, deep funnels |
| Amplitude | SaaS | Yes — API | Similar to Mixpanel, stronger experimentation |
| Plausible | OSS / SaaS | Yes — API | Privacy-first, lightweight |
| PostHog | OSS / SaaS | Yes — API | Self-hostable, all-in-one |
| Stape.io | SaaS | Yes | Managed server-side GTM hosting |

## Templates & scripts
See `templates.md` and the README's "Event Tracking Plan" + "UTM Convention Document" — drop-in for new projects.

Inline staging validator (Playwright):

```javascript
// validate_events.js
const { chromium } = require('playwright');

const expected = ['page_view', 'sign_up', 'purchase'];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const seen = new Set();
  await page.exposeFunction('captureEvent', (n) => seen.add(n));
  await page.addInitScript(() => {
    const orig = window.dataLayer = window.dataLayer || [];
    const push = orig.push.bind(orig);
    orig.push = (e) => { if (e.event) window.captureEvent(e.event); return push(e); };
  });
  await page.goto('https://staging.example.com/signup');
  await page.fill('#email', 'test@ex.com');
  await page.click('#submit');
  await page.waitForTimeout(2000);
  const missing = expected.filter(e => !seen.has(e));
  console.log(missing.length ? `FAIL missing: ${missing}` : 'PASS');
  await browser.close();
})();
```

## Best practices
- Define the event spec BEFORE writing tracking code; treat it as a versioned doc in the repo.
- Use the dataLayer pattern even with gtag-direct — abstracts source of truth from the tag.
- Hash all PII (email, phone) before sending to ad pixels; ideally via server-side tagging.
- Implement Consent Mode v2 from day one even outside EEA — saves a future migration.
- Standardize UTM naming in code (a constant export); humans typo `Facebook` vs `facebook` vs `fb`.
- Link GA4 to Google Ads, BigQuery, and Search Console immediately — these unlock report features without extra work.
- Run event-firing E2E tests in CI; analytics drift silently otherwise.
- Mark conversion events explicitly; GA4's automatic detection is unreliable.
- For e-commerce: implement enhanced ecommerce 1.0 schema (`view_item`, `add_to_cart`, `purchase` with `items` array) — Meta and Google both consume this.

## AI-agent gotchas
- GA4 has reserved event names (`session_start`, `first_visit`, etc.); using them as custom events causes silent collision.
- 50 custom dimensions / 50 metrics limit per property — agents creating dimensions per feature will hit cap and break new tracking.
- Cardinality: high-cardinality custom dimensions get aggregated to `(other)` in reports; agents adding `user_id` as a dimension waste a slot.
- Real-time report has 30-min lag; "real-time" means "less than 30 min", not seconds. DebugView is the only sub-second view.
- BigQuery export is daily by default; streaming export is paid.
- iframe contexts: events fired inside iframes don't reach parent's gtag — agents auto-instrumenting embeds will see ghost data.
- gtag config calls are queued; calling `gtag('event', ...)` before `gtag('config', ...)` runs sends events to wrong property.
- GTM containers exported as JSON have all secrets stripped — agents importing across accounts must re-link API keys manually.
- Measurement Protocol requires `client_id` matching the gtag-set first-party cookie for sessions to stitch — server-side events without this create new sessions.
- `purchase` event with `transaction_id` is required for de-dup; missing it causes inflated revenue.

## References
- GA4 Events: https://support.google.com/analytics/answer/9322688
- GA4 Reserved Events: https://support.google.com/analytics/answer/13316687
- Consent Mode v2: https://support.google.com/analytics/answer/9976101
- Measurement Protocol: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- BigQuery export schema: https://support.google.com/analytics/answer/7029846
- Server-side GTM: https://developers.google.com/tag-platform/tag-manager/server-side
