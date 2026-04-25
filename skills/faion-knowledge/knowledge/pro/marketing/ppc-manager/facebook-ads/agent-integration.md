# Agent Integration — Facebook (Meta) Ads API

## When to use
- Programmatic Meta Ads management: bulk ad-set duplication for A/B tests, scheduled budget shifts, automated creative rotation.
- Server-side Conversions API (CAPI) wiring — agents push deduplicated events from backend to Meta to recover signal lost to iOS ATT.
- Cross-account audits across a Business Manager hierarchy (agency / multi-brand owner).
- Continuous creative refresh: agent generates creative variants, uploads via Marketing API, links to Advantage+ asset feeds.

## When NOT to use
- Active learning phase (first ~50 conversions per ad set) — automated bid/budget tweaks reset learning and burn money.
- Tiny budgets (<$30/day per ad set) — Meta has minimum-spend signal floors and the API surface adds operational risk for no upside.
- Special Ad Categories (housing, employment, credit, social issues) without explicit category flag — agents must set `special_ad_categories` correctly or campaigns get rejected.
- One-off creative judgement calls (which hero image wins) — humans still beat agents on visual taste; use Advantage+ Creative Optimization instead.

## Where it fails / limitations
- Graph API versions deprecate after ~2 years; v20.0 today, v21.0 next. Hard-coded versions silently break on sunset.
- Budget fields are in account currency MINOR units (USD cents). Setting `daily_budget: 50` = $0.50, not $50 — common LLM bug.
- Targeting `flexible_spec` with too many `interests` / `behaviors` triggers `Audience too narrow` and the ad set never delivers.
- iOS 14+ ATT crushed pixel-only attribution; without CAPI + Advanced Matching, optimization signal is unreliable.
- Rate limits are per-app, per-user, AND per-ad-account (BUC). Bursting bulk operations across 50 accounts trips ad-account limits.
- Async video upload requires polling `status=ready` before creative creation — race conditions break naive scripts.
- Special Ad Categories disable lookalike, custom-age, location-radius targeting — agents must branch on category.

## Agentic workflow
Spawn a single Meta-ads agent that holds the System User access token (long-lived) and the Business Manager / ad-account ID list. For reads, use Insights API with `breakdowns` + `time_increment`; for writes, batch creates via the JSON Batch API (`/batch?include_headers=false`) up to 50 ops per call. Always upload images first, then video (poll for ready), then creative, then ad — these are sequential dependencies. Use the dry-run pattern: serialize the would-be POST body and have a human approve before sending.

### Recommended subagents
- `faion-ads-agent` — Meta + Google Ads execution, holds tokens.
- `faion-sdd-executor-agent` — runs quality gates when Meta API code lands in product.
- `password-scrubber-agent` — strip System User tokens / app secrets from logs and commits.

### Prompt pattern
```
System: You are the Meta Ads agent. All money values are in account-currency
        minor units (cents). Never POST to /ads without first verifying the
        creative was uploaded and got a creative_id. For Special Ad
        Categories, refuse to add lookalike or location-radius targeting.
User:   Duplicate ad set 1234 with 2 new creatives, swap targeting to
        US 25-34 women, set daily_budget to $40. Dry-run first.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook-business` (Python SDK) | Official Meta Marketing SDK | `pip install facebook-business` |
| `facebook-nodejs-business-sdk` | Node SDK | `npm i facebook-nodejs-business-sdk` |
| Marketing API Explorer | Web tool to test Graph requests | https://developers.facebook.com/tools/explorer/ |
| `gh-meta-conversions-api` server | Reference CAPI gateway | https://github.com/facebookincubator/meta-conversions-api |
| `curl` | Direct Graph API calls — the SDKs are thin wrappers | universal |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Marketing API | SaaS | Yes (REST) | Needs app review for `ads_management` if used outside own BM. |
| Meta Conversions API (CAPI) | SaaS | Yes (REST) | Use for server-side events; pair with pixel for dedup via `event_id`. |
| Meta Business Manager | SaaS | Partial | UI-first; API exposes assets and System Users. |
| Meta Events Manager | SaaS | UI mostly | Where pixel + dataset attribution windows are configured. |
| Supermetrics / Funnel | SaaS | Yes | Connectors to BigQuery / Sheets if you skip raw Marketing API. |
| Triple Whale, Northbeam | SaaS | Yes (API) | MMM / multi-touch attribution, often paired with Meta agents. |
| Smartly.io | SaaS | Yes | Bulk creative + scaling; agents can call its API instead of Meta's directly for some flows. |

## Templates & scripts
See `templates.md` and `examples.md` for full curl payloads. Minimal CAPI server-event poster (lets an agent fire conversions when a backend webhook detects a sale):

```python
# capi_send.py — server-side conversion event with deduplication
import time, hashlib, requests

def send_purchase(pixel_id: str, token: str, event_id: str,
                  email: str, value: float, currency: str = "USD"):
    h = lambda s: hashlib.sha256(s.lower().strip().encode()).hexdigest()
    payload = {
        "data": [{
            "event_name": "Purchase",
            "event_time": int(time.time()),
            "event_id": event_id,        # MATCH the pixel's eventID for dedup
            "action_source": "website",
            "user_data": {"em": [h(email)]},
            "custom_data": {"value": value, "currency": currency},
        }]
    }
    r = requests.post(
        f"https://graph.facebook.com/v20.0/{pixel_id}/events",
        params={"access_token": token},
        json=payload, timeout=10,
    )
    r.raise_for_status()
    return r.json()
```

## Best practices
- Pin SDK version AND Graph version (`FacebookAdsApi.init(api_version='v20.0')`) and bump on a calendar, not by accident.
- Use a System User token (non-expiring) for agents — never a personal user token.
- Always supply `event_id` on both pixel and CAPI for the same conversion; missing dedup inflates counts ~30%.
- Use `is_dynamic_creative=true` + asset feeds instead of writing 50 ads — Meta does the combinatorics for you.
- Minimum 50 conversions per ad set per week to escape "Learning Limited" — agents should not split budget below that floor.
- For agency/multi-account: assign each ad account to its own request queue with its own rate-limit tracker.
- Validate `objective` enum on the v20+ list; old `LINK_CLICKS` / `CONVERSIONS` codes are gone.

## AI-agent gotchas
- Cents bug: LLMs default to dollars. Add an assert: `assert daily_budget >= 100, "budgets are in cents; <100 means <$1"`.
- Targeting JSON is brittle — `interests` requires Meta's interest IDs, not strings. Look up via `/search?type=adinterest&q=...` first.
- Async video upload — polling logic must time out cleanly; agents that loop forever on `status=processing` block other work.
- Special Ad Categories: agent must check the campaign's category before composing targeting; otherwise creates rejected ads silently.
- Token rotation: rotating System User tokens invalidates ALL agents using that token. Roll out new tokens before revoking old.
- Human-in-loop checkpoint: any spend-change >2x current daily budget, any audience expansion >5x, any switch from PAUSED → ACTIVE.
- "Learning Limited" status is a hint, not an error — agents should skip optimization on those ad sets, not "fix" them.
- Models often confuse `campaign.daily_budget` (CBO) with `adset.daily_budget` (set-level). Setting both raises validation errors.

## References
- Meta Marketing API — https://developers.facebook.com/docs/marketing-apis/
- Conversions API — https://developers.facebook.com/docs/marketing-api/conversions-api
- Graph API versioning — https://developers.facebook.com/docs/graph-api/changelog
- Insights API breakdowns — https://developers.facebook.com/docs/marketing-api/insights/breakdowns
- facebook-business Python SDK — https://github.com/facebook/facebook-python-business-sdk
