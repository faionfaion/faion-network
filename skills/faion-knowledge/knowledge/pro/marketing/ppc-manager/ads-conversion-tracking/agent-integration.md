# Agent Integration — Conversion Tracking

## When to use
- New site launch — install pixel + CAPI before any paid spend.
- Auditing an existing site where Meta-reported conversions diverge >25% from GA4 / server revenue.
- Migrating from cookie-only tracking to a server-side / first-party stack (CAPI, GA4 Measurement Protocol, gtag server-side).
- Reconciling offline/CRM conversions back into ad platforms for Smart Bidding signal.
- Setting up multi-platform tracking (Meta + Google + LinkedIn + TikTok) with consistent event names.

## When NOT to use
- One-off campaign on an existing well-tracked site — the tracking is already there, just add a new conversion action.
- Pre-product-market-fit: < 100 conversions/month total — investing in CAPI infra is overkill, get the basic pixel right.
- Site with no commercial events (purely content) — track engagement in GA4, skip ad-platform pixels.

## Where it fails / limitations
- iOS 14.5+ ATT, Safari ITP, and EU consent banners cut browser-only pixel coverage by 30-60% — server-side is mandatory for accurate numbers.
- Meta CAPI events without `event_id` get deduped against the pixel by `event_name + timestamp` window — easy to double-count if you skip event IDs.
- `predicted_ltv` on Meta is a custom param Meta doesn't actually use for bidding (yet) — don't optimize on it.
- LinkedIn Insight Tag has 90-day attribution but only fires on direct site visits — single-page apps need explicit `_linkedin_partner_id` push on route change.
- gtag/GTM server containers don't replicate Meta's automatic advanced matching — you must hash and send PII fields explicitly.
- Apple's Private Relay strips IP from server-side requests for some users — fingerprinting fallbacks degrade silently.

## Agentic workflow
Tracking work has two phases: **build** (one-time) and **monitor** (continuous). Build phase is high human-in-loop: agent generates pixel snippets, infra agent deploys them, QA agent runs synthetic conversions and verifies. Monitor phase is autonomous: agent diffs Meta Events Manager numbers vs GA4 vs server logs nightly, alerts on > 10% delta. Never let an agent silently re-deploy pixel code without seeing a live Test Event — broken tracking is invisible until the campaign report.

### Recommended subagents
- `faion-ads-agent` — generates pixel/CAPI code per platform, configures conversion actions in ad platforms.
- `faion-improver` — nightly reconciliation: pixel vs server vs GA4, drift alerts.
- `faion-sdd-executor-agent` — gates production deploy of new tracking behind synthetic tests.

### Prompt pattern
```
Generate pixel + CAPI for {platform=Meta} on {framework=Next.js}. Events:
PageView (auto), ViewContent (product page), AddToCart, InitiateCheckout,
Purchase. Use event_id = order_id for dedup. Hash email/phone with SHA-256
before sending. Output: client snippet, server endpoint, env-var list.
```

```
Reconcile {date_range}: pull Meta Insights conversions, GA4 events, Stripe
payments. Group by date. Report rows where |meta - stripe| / stripe > 0.15.
For each, list missing event_ids and propose fix (CAPI gap vs pixel block).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Meta Pixel Helper | Verify browser pixel | Chrome extension |
| Google Tag Assistant Companion | Verify gtag/GTM | Chrome extension + standalone debugger |
| `facebook-business` Python SDK | CAPI server events | `pip install facebook-business` |
| `gtag-validator` (community) | gtag CI smoke tests | https://github.com/topics/gtag |
| Stape sGTM CLI | Deploy server-side GTM | https://stape.io/docs |
| `httpie` / `curl` | Manually post Measurement Protocol events | system |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Conversions API Gateway | SaaS (Meta) | Yes | Free, runs in your AWS/GCP — drop-in CAPI |
| Stape | SaaS | Yes | Hosted server-side GTM; great for non-infra teams |
| Segment / RudderStack | SaaS / OSS | Yes | Single-source tracking → multi-platform fanout |
| Customer.io | SaaS | Yes | Server-side events forwarder |
| Snowplow | OSS | Yes | Self-hosted event pipeline; full control + fingerprinting |
| Triple Whale | SaaS | Partial | E-com attribution layer; agent-readable but UI-heavy |
| Hyros | SaaS | Partial | First-party tracking for offers/info products |

## Templates & scripts
See `templates.md` for per-platform event maps. Inline reconciliation script — the daily sanity check every account needs:

```python
import os, datetime as dt
import requests
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

def reconcile(start, end, ad_account_id, stripe_total):
    """Compare Meta-reported revenue vs Stripe ground truth."""
    FacebookAdsApi.init(access_token=os.environ["META_TOKEN"])
    insights = AdAccount(ad_account_id).get_insights(params={
        "time_range": {"since": str(start), "until": str(end)},
        "level": "account",
        "fields": ["action_values"],
    })
    meta_rev = 0.0
    for row in insights:
        for av in row.get("action_values", []):
            if av["action_type"] == "purchase":
                meta_rev += float(av["value"])
    delta = (meta_rev - stripe_total) / stripe_total if stripe_total else 0
    return {"meta": meta_rev, "stripe": stripe_total, "delta_pct": delta}
```

## Best practices
- Always send a unique `event_id` (order ID, lead ID) on both pixel and CAPI for the same event — Meta dedupes within a 48-hour window. No event_id = double-count.
- Hash PII (email, phone, first/last name, city, zip) with lowercase-trim then SHA-256 before sending — and verify in Events Manager that match-quality score is > 5.0.
- Fire one and only one Purchase per order. If your thank-you page can be reloaded, gate the pixel on `sessionStorage` or send only from server.
- Keep event names canonical across platforms via a single mapping table; never sprinkle platform-specific names through the codebase.
- Set CAPI as the source of truth in the ad platform once both are stable — pixel becomes a redundant backup, not the primary signal.
- Test on an iOS Safari device with Private Relay on — that's where 30% of the data loss hides.

## AI-agent gotchas
- An agent generating pixel snippets will sometimes use the example `YOUR_PIXEL_ID` — always validate the substitution against an env var, not a string template.
- Don't let an agent "fix" a pixel error by setting `partial_failure=True` and ignoring the error — that masks data loss.
- Test events go to a different bucket than production events; if an agent never flips off `test_event_code`, real conversions never feed Smart Bidding.
- Server-side events from a CRM webhook can fire days after the click — Meta drops events older than 7 days; agents must alert on backlog, not silently drop.
- Human-in-loop checkpoint: any change to production pixel/CAPI on a site doing > $1K/day in tracked revenue. Below that, run the agent's diff through a staging environment first.
- When Consent Mode v2 is on, GA4 silently models conversions; an agent reading raw vs modeled numbers without the distinction will produce nonsense reports.

## References
- https://developers.facebook.com/docs/marketing-api/conversions-api
- https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events
- https://developers.google.com/tag-platform/devguides/consent
- https://www.linkedin.com/help/lms/answer/a423304 (LinkedIn Insight Tag)
- https://stape.io/blog/server-side-tracking
