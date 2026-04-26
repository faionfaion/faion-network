# Agent Integration — Retargeting

## When to use
- Standing up multi-platform retargeting (Meta + Google + LinkedIn) from a single source-of-truth event spec.
- Maintaining segmented retargeting audiences (visitors → product viewers → cart abandoners) and rotating creative on a schedule to avoid fatigue.
- Auto-pausing retargeting ad sets when frequency exceeds caps or CTR drops a configured threshold.
- Sequential retargeting playbooks (Day 1-3 reminder → Day 4-7 benefit → Day 8-14 social proof → Day 14+ urgency) driven by audience-membership windows.
- Reconciling pixel data with server-side CAPI / Enhanced Conversions to recover post-iOS losses.

## When NOT to use
- Pre-traffic stage. Need ~10k monthly visitors before retargeting moves the needle; below that, allocate 100% to acquisition.
- Long sales cycles (6+ months B2B enterprise). Retargeting fatigue beats benefit; better off using account-based outreach.
- Restricted verticals (housing, credit, health, employment) — Meta Special Ad Category disables most retargeting audiences; LinkedIn similarly limits matched audiences.
- One-off purchase products with no upsell path. Customers blacklisted from retargeting after purchase = audience near-zero.

## Where it fails / limitations
- Pixel-only retargeting on iOS Safari/14.5+ ATT loses 40-70% of audience. Without CAPI, agent will report shrinking audience sizes month over month with no obvious cause.
- Frequency caps in Meta apply per ad set, not per user across the campaign — naive agent setup leads to one user seeing 5 ad sets × 3/week = 15 impressions.
- "Visitors last 180 days" auto-decays daily. Audience sizes look smaller on Mondays after weekend visit drops; agent alerts on size drops will false-positive.
- Cross-domain tracking (subdomain → main, app → web) requires explicit pixel config; missing it splits retargeting pools.
- GDPR / ePrivacy: EU/UK users without consent must be excluded; if Consent Mode v2 not wired, agent uploading email lists violates lawful basis.

## Agentic workflow
The retargeting agent owns three loops: (1) event-spec sync — reads a YAML/JSON event taxonomy and verifies pixel + CAPI fire on each route via headless Playwright; (2) audience builder — reads a segment matrix and upserts platform audiences with deterministic naming; (3) campaign runtime — monitors frequency, CTR decay, and exclusion drift, pausing or rotating creative when thresholds trip. Human-in-the-loop on creative approval and any spend-impacting threshold change.

### Recommended subagents
- `faion-ads-agent` — Marketing API surfaces (Meta, Google, LinkedIn) for audience + ad set CRUD.
- `faion-sdd-executor-agent` — wraps quarterly retargeting playbook updates as SDD tasks with test-plan gates (event-fire test, exclusion test, frequency-cap test).
- `password-scrubber-agent` — scrubs hashed customer lists from logs.

### Prompt pattern
```
Goal: verify pixel + CAPI parity for events [PageView, ViewContent, AddToCart, InitiateCheckout, Purchase].
For each event: navigate route in Playwright, capture network calls, assert pixel fired AND CAPI server received same event_id within 5s.
Output: pass/fail matrix; halt downstream audience build if any event missing CAPI.
```

```
Goal: rotate creative for all retargeting ad sets where frequency >5 OR CTR has dropped 30% from 7-day baseline.
Action: pause ad, swap to next-in-queue creative from approved library, log rotation.
Do NOT mutate budget. Do NOT touch ad sets without an approved creative in queue.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook-business` Python SDK | Meta audiences, frequency capping, ad rotation | `pip install facebook-business` |
| `google-ads-python` | Google Ads remarketing lists, RLSA, customer match | `pip install google-ads` |
| `linkedin-api` (community) / direct REST | LinkedIn Matched Audiences | https://learn.microsoft.com/linkedin/marketing/ |
| `playwright` | Headless event-fire verification on staging + prod | `pip install playwright && playwright install` |
| `gtm-cli` (community) | Manage GTM containers as code | https://github.com/google/site-kit-wp |
| Stape / ServerGTM | sGTM container deploys for CAPI | https://stape.io/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Conversions API | First-party API | Yes | Required for iOS recovery. Use event_id dedupe. |
| Google Ads Customer Match | First-party API | Yes | Hashed email upload; 1k minimum. |
| Google Enhanced Conversions | First-party | Yes | Recovers attribution; gtag config. |
| LinkedIn Matched Audiences | First-party API | Yes | 300 minimum; slow refresh (24-48h). |
| Stape sGTM | SaaS | Yes | Deploy server-side GTM via API; agent can manage containers. |
| Segment / RudderStack | CDP (SaaS / OSS) | Yes | Single event spec → fan-out to all ad platforms. |
| Klaviyo / Customer.io | ESP | Partial | Native Meta/Google audience sync; agent triggers via webhook. |

## Templates & scripts
Inline: pause Meta ad sets where frequency exceeds cap. Idempotent, dry-run by default.

```python
import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

def cap_fatigued_ad_sets(account_id: str, freq_max: float = 5.0, dry_run: bool = True):
    FacebookAdsApi.init(access_token=os.environ["META_TOKEN"])
    acct = AdAccount(f"act_{account_id}")
    insights = acct.get_insights(
        params={"date_preset": "last_7d", "level": "adset", "fields": ["adset_id", "frequency", "ctr"]},
    )
    actions = []
    for row in insights:
        if float(row.get("frequency", 0)) > freq_max:
            actions.append({"adset_id": row["adset_id"], "frequency": row["frequency"], "ctr": row.get("ctr")})
            if not dry_run:
                from facebook_business.adobjects.adset import AdSet
                AdSet(row["adset_id"]).api_update(params={"status": "PAUSED"})
    return actions
```

See `templates.md` for retargeting audience setup and campaign structure.

## Best practices
- Adopt one event spec (Segment-style) and fan out to Meta + Google + LinkedIn from the same payload. Drift across platforms is the #1 retargeting bug.
- Always pair pixel + CAPI with `event_id`. Without it, dedupe fails and ROAS attribution is double-counted.
- Frequency caps belong at the campaign level, not ad set, on Meta where Reach & Frequency objective allows it.
- Always exclude purchasers (90-180d window) at the campaign level. Codify the exclusion audience IDs in a registry; agents must verify the exclusion is attached after every save.
- Refresh creative every 14-21 days. Use a creative queue table (status: approved / live / retired) the agent can read.
- Run retargeting at 20-30% of total spend. Higher means acquisition starves; lower means leaving warm leads on the table.

## AI-agent gotchas
- Meta's `frequency` field is over a 7-day rolling window, not lifetime. Agents that compare lifetime frequency to a 7-day cap will pause everything.
- Cart abandoner audiences need `time_window` of 1-7 days for urgency, but Meta defaults new audiences to 30 days. Agent must explicitly set `retention_days`.
- Customer Match in Google Ads needs ≥1000 matched users to activate; smaller lists upload OK but never serve. Agent must check `match_rate` after upload.
- LinkedIn Matched Audience refresh is async with no callback; agent should poll status, not assume immediate availability.
- iOS users may show in audience size but never receive impressions. Don't tune frequency caps based on audience size alone — use delivery insights.
- Sequential retargeting requires audience exclusions across stages (Day 4-7 ad set excludes Day 1-3 audience). Easy to break when cloning campaigns; agent must verify exclusion graph after any campaign duplication.

## References
- https://developers.facebook.com/docs/marketing-api/conversions-api
- https://www.facebook.com/business/help/1474662202748341
- https://support.google.com/google-ads/answer/2453998 (Remarketing Lists)
- https://support.google.com/google-ads/answer/9888656 (Enhanced Conversions)
- https://learn.microsoft.com/linkedin/marketing/integrations/ads-reporting/matched-audiences
