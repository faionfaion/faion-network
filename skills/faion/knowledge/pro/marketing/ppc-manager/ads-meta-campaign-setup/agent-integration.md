# Agent Integration — Meta Campaign Setup

## When to use
- Spinning up the first Facebook/Instagram campaign for a new account or product launch.
- Scaling from one Sales/Leads campaign into a structured CBO + multi-ad-set tree.
- Standardizing campaign and ad-set naming across many products / clients (agency setup).
- Migrating off boosted posts into structured Ads Manager campaigns.

## When NOT to use
- Account already has > $5K/mo spend with proven structure — work the existing structure, don't refactor.
- Single-creative test under $20/day — use the boosted post or a single ad set, not a full CBO.
- B2B target list of < 10K people — use LinkedIn Matched Audiences instead, Meta will starve.
- Pixel + CAPI is not yet installed and verified — campaign setup is wasted effort without tracking.

## Where it fails / limitations
- Apple ATT + iOS 14 means Meta-reported conversions undercount by 15-40% on iOS; campaign reporting won't match GA4/server-side numbers.
- Learning phase needs ~50 conversions/ad-set/week — small advertisers running 4 ad sets at $20/day will live in permanent learning.
- CBO rebalances across ad sets daily; tiny ad sets (<10% of total spend) get starved silently — review and consolidate.
- Advantage+ Audience overrides "detailed targeting" defaults in 2024+ accounts — tightly defined interests are now suggestions, not hard filters.
- Editing budget by > 20% inside learning phase resets it; agents that auto-rebalance daily can keep a campaign permanently in learning.

## Agentic workflow
A marketing agent decides objective + audience hypotheses; a code agent (or workflow tool) creates the campaign tree via the Marketing API or Meta Ads MCP. Always lock pixel + CAPI verification as a hard gate before any Spend > 0 — make this a tool that returns true/false, not a checklist the agent skims. After launch, freeze structure for 3-7 days while learning phase completes; agent's job is monitoring, not editing.

### Recommended subagents
- `faion-ads-agent` — owns Marketing API client, campaign/ad-set/ad creation, pixel verification.
- `faion-marketing-manager` — chooses objective, sets initial budgets, defines audience tree.
- `faion-improver` — post-launch loop: read insights, propose creative refresh / audience expansion.

### Prompt pattern
```
Build a Meta campaign for {product} with daily budget ${budget}, objective Sales,
3 ad sets: (1) interest-based, (2) 1% lookalike of purchasers, (3) 30-day cart
retargeting. CBO at campaign level. 3 RSAs per ad set. STOP if pixel test event
isn't seen in last 24h. Return campaign_id, ad_set_ids, draft ads (not published).
```

```
Audit campaign {id}: list every ad set with <10% campaign spend share, every ad
with frequency >3, every ad set still in learning after 14 days. Produce a
prioritized action list (consolidate / refresh / kill).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook-business` Python SDK | Official Marketing API client | `pip install facebook-business` · https://developers.facebook.com/docs/marketing-apis/sdks |
| `facebook-nodejs-business-sdk` | Node Marketing API client | `npm i facebook-nodejs-business-sdk` |
| Meta Ads MCP server | Lets Claude/agents drive Ads Manager directly | https://github.com/pipeboard-co/meta-ads-mcp |
| Meta Pixel Helper | Verify pixel & events in browser | Chrome extension |
| `business-manager-cli` (community) | Bulk asset moves across BMs | https://github.com/jasonsalas |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Marketing API | SaaS API | Yes | App needs `ads_management` permission + business verification for production |
| Meta Conversions API Gateway | SaaS (Meta-hosted) | Yes | Drop-in CAPI without writing server code; deploys on AWS/GCP |
| Stape | SaaS | Yes | Server-side GTM hosting for CAPI + GA4 |
| Madgicx / Revealbot | SaaS | Partial | Rule-based automation; agents can read but rules conflict |
| Smartly.io | SaaS | Limited | Enterprise creative automation; UI-first |
| n8n / Make / Zapier | OSS/SaaS | Yes | Glue: agent decisions → API mutations |

## Templates & scripts
See `templates.md` for naming conventions and ad-set YAML. Inline pre-launch verification gate (the most common reason campaigns fail silently):

```python
import time
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adspixel import AdsPixel

def verify_pixel_ready(pixel_id, access_token, max_age_hours=24):
    """Block campaign launch if pixel hasn't fired a Purchase/Lead recently."""
    FacebookAdsApi.init(access_token=access_token)
    pixel = AdsPixel(pixel_id)
    stats = pixel.get_stats(params={"aggregation": "event"})
    cutoff = time.time() - max_age_hours * 3600
    seen = {s["event"]: s["count"] for s in stats if s["start_time"] >= cutoff}
    required = {"PageView", "Purchase"}  # adjust per business
    missing = required - seen.keys()
    if missing:
        raise RuntimeError(f"Pixel not ready: missing events {missing}")
    capi = pixel.api_get(fields=["last_fired_time", "automatic_matching_fields"])
    if not capi["last_fired_time"]:
        raise RuntimeError("CAPI never fired — server-side tracking missing")
    return True
```

## Best practices
- Name everything before launch using `[product]_[objective]_[audience]_[YYYYMM]` — agents reading insights need this to parse without metadata.
- Start with ONE objective per account; mixing Sales + Leads + Engagement campaigns confuses Smart Promotion and bidding auctions.
- 3 ad sets max for first 2 weeks. Add more only after each existing one exits learning. Otherwise CBO has nothing to balance.
- Set `daily_budget` not `lifetime_budget` for ongoing campaigns — lifetime budget freaks out under CBO and pacing breaks.
- For Sales objective, always pick a single conversion event (Purchase) and let the rest be `custom_event` — multi-event optimization waters down signal.
- Put creative refresh on a 14-day cron; CTR decay above 20% is the real signal but most agents only catch it after CPA already doubled.

## AI-agent gotchas
- Agents will happily set `optimization_goal=LINK_CLICKS` for a Sales campaign because the API allows it — costs you 60% efficiency. Validate that goal matches objective.
- Editing `daily_budget` mid-learning resets the phase; an agent that "optimizes budget daily" can hold a campaign in permanent learning. Throttle budget changes to weekly outside learning.
- Meta returns success on creating an ad with a broken landing URL; agents must run a synthetic HEAD request on every `link_url` before publish.
- `Standard Enhancements` is enabled by default in 2024+ accounts and silently rewrites copy. If brand voice matters, explicitly disable per ad.
- Human-in-loop checkpoint: budget > $100/day, audience > 50M, or first creative on a new account. Below those, autopilot is fine.
- Watch token expiry: Marketing API tokens expire 60 days after issue without refresh; agents should warn at 7 days remaining, not on expiry day.

## References
- https://developers.facebook.com/docs/marketing-apis/overview
- https://www.facebook.com/business/help/1438417719786103 (campaign structure best practices)
- https://www.facebook.com/business/help/1619591734742116 (bidding strategies)
- https://github.com/pipeboard-co/meta-ads-mcp
- https://developers.facebook.com/docs/marketing-api/conversions-api
