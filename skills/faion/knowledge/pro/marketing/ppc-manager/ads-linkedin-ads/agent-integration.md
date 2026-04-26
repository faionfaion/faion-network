# Agent Integration — LinkedIn Ads

## When to use
- B2B campaigns where buyer is identifiable by job title, seniority, or company (account-based marketing).
- Lead-gen forms with LinkedIn-prefilled fields (email, company, title) for high-quality MQLs.
- Reach narrow ICPs that are unreachable on Meta or Google (e.g., VP Engineering at fintech 200-1000 employees).
- Retargeting site visitors with the LinkedIn Insight Tag for warm-funnel B2B nurture.

## When NOT to use
- B2C, low-AOV products, or impulse purchases — CPC of $5-15 destroys unit economics below ~$1k LTV.
- Daily budgets under $50 — LinkedIn's optimizer cannot exit the learning phase and burns budget on noise.
- Audiences <20k — costs spike, learning never converges, frequency caps trigger fatigue early.
- Pure brand awareness on a tight budget — Meta/YouTube cost-per-impression is 5-10x cheaper.

## Where it fails / limitations
- Conversion API (CAPI) on LinkedIn is less mature than Meta — server-side dedup quirky, expect 10-20% loss vs. true conversions.
- Reporting lag: 24-48h before stable numbers appear; do not retune daily.
- API quotas: developer-tier apps capped at 500 requests/day; production-tier requires partner approval.
- Lead Gen Form CSV exports are the only source of truth for some fields — webhook delivery has occasional gaps.
- No dynamic creative optimization at the level Meta offers; manual A/B testing required.

## Agentic workflow
A subagent owns the full LinkedIn Ads loop: ICP → campaign brief → API-driven setup → daily pacing checks → weekly creative refresh recommendations. Use the LinkedIn Marketing Developer Platform (Campaign Manager API) for campaign and creative operations, plus the Lead Sync API for delivering Lead Gen Form submissions to the CRM. Human-in-loop required for: final ad copy approval, ABM target-account list sign-off, budget changes >25%.

### Recommended subagents
- `faion-ads-agent` (referenced in methodology metadata) — owns campaign creation, asset upload, audience-list management.
- `faion-sdd-executor-agent` (existing in `agents/`) — runs structured optimization tasks against acceptance criteria (e.g., "CPL < $75 within 14 days").
- A purpose-built `linkedin-ads-optimizer` subagent (suggested) — daily pacing audit, weekly creative-fatigue scan, ICP-overlap detection across campaigns.

### Prompt pattern
```
You are a LinkedIn Ads optimizer. Goal: <CPL target, MQL volume>.
Inputs: campaign IDs, last 14d metrics CSV, ICP definition.
Output JSON: {pause: [...], scale: [...], creative_refresh: [...], rationale}.
Hard rule: never increase budget >25% in one step; require human approval above.
```

```
Generate 5 LinkedIn Single Image ad variants for ICP <persona>.
Constraints: intro <150 chars, headline <70, description <100.
Each variant uses a distinct angle: pain, social proof, ROI, urgency, contrarian.
Return XML with <variant id> blocks.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linkedin-api` (Python, unofficial) | Quick campaign reads, scraping for research | `pip install linkedin-api` |
| `python-linkedin-v2` | Official OAuth client wrapper for Marketing API | `pip install python3-linkedin` |
| `gcloud` + Conversions API | Server-side conversion uploads via direct HTTPS | docs: linkedin.github.io/Conversions-API |
| `curl` + `jq` | Direct REST against `api.linkedin.com/rest/adAccounts/...` | preinstalled |
| Looker Studio LinkedIn connector | Reporting dashboards | datastudio.google.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LinkedIn Campaign Manager | SaaS (native) | Partial — Marketing API covers ~80% of UI | Daily edits, asset upload, reporting |
| Zapier LinkedIn Lead Ads connector | SaaS | Yes — webhook trigger | Push leads to CRM/Slack/Notion |
| HubSpot LinkedIn integration | SaaS | Yes | Native lead sync, attribution |
| Make.com (Integromat) | SaaS | Yes — REST connector | Free up to 1k ops/month |
| Dreamdata / HockeyStack | SaaS | Yes — API | B2B multi-touch attribution; closes LinkedIn-to-revenue loop |
| Phantombuster | SaaS | Limited — TOS-risky | Audience research only, not for ad ops |

## Templates & scripts
See `templates.md` for campaign-setup checklist and ad-copy template. Inline helper for daily pacing audit:

```python
# pacing_audit.py — flag campaigns spending too fast/slow
import requests, os, datetime as dt

TOKEN = os.environ["LI_ACCESS_TOKEN"]
ACCOUNT = os.environ["LI_AD_ACCOUNT_URN"]  # urn:li:sponsoredAccount:123

def fetch_today_spend(campaign_id):
    url = (f"https://api.linkedin.com/rest/adAnalytics?q=analytics"
           f"&pivot=CAMPAIGN&campaigns=List(urn%3Ali%3AsponsoredCampaign%3A{campaign_id})"
           f"&dateRange=(start:(year:{dt.date.today().year},month:{dt.date.today().month},day:{dt.date.today().day}))"
           f"&fields=costInLocalCurrency,impressions,clicks")
    h = {"Authorization": f"Bearer {TOKEN}", "LinkedIn-Version": "202410"}
    return requests.get(url, headers=h).json()

def audit(campaign_id, daily_cap_usd):
    data = fetch_today_spend(campaign_id)
    spend = float(data["elements"][0]["costInLocalCurrency"]) if data.get("elements") else 0
    hour_pct = dt.datetime.now().hour / 24
    expected = daily_cap_usd * hour_pct
    return {"campaign": campaign_id, "spend": spend, "expected": expected,
            "variance": (spend - expected) / max(expected, 1)}
```

## Best practices
- Build the audience in 3 layers: ABM list (named accounts) → ICP (title + size + industry) → similar audience expansion. Run as separate campaigns, not one targeting blob.
- Always use Lead Gen Forms in parallel with Website Conversions — LGF has higher volume but lower intent; track both to revenue, not just CPL.
- Refresh creative every 14-21 days. CTR decay on LinkedIn is faster than Meta because feed is sparser.
- Use Matched Audiences company list for retargeting site visitors AND running ABM in parallel — cheaper than buying intent data from third parties.
- Exclude existing customers and converted leads via uploaded customer-list audiences; LinkedIn has no native "exclude converters" toggle the way Meta does.
- Set frequency caps manually (default is too high): 5/week for awareness, 2/week for conversion.
- Bid manually CPC for first 2 weeks of any new campaign, then switch to Maximum Delivery once you have 50+ form fills for the optimizer.

## AI-agent gotchas
- Token rotation: LinkedIn access tokens expire in 60 days; agent must refresh via OAuth refresh-token flow or it silently fails at midnight.
- API versioning: `LinkedIn-Version` header is required and changes monthly; agents pinning a version >6 months old will hit deprecation 410s.
- Rate limits per app, not per account — multi-tenant agents must implement per-app token bucket and back off on 429.
- Lead Gen Form schema drift: custom fields appear with auto-generated keys (`question_1ab23`); cache the field-map per form, do not assume order.
- Cost data is in `costInLocalCurrency` micros (multiply by 1 not 1M like Google) — easy off-by-1M bug.
- Insight Tag conversions backfill for up to 90 days — do not declare a campaign a loser before that window.
- Asset library has a 24h propagation lag for image assets in some regions; agents staging campaigns at 23:59 UTC may launch with broken creative.

## References
- LinkedIn Marketing API: https://learn.microsoft.com/en-us/linkedin/marketing/
- Conversions API: https://learn.microsoft.com/en-us/linkedin/marketing/conversions/
- Lead Sync API: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/lead-sync/
- Audience Targeting reference: https://learn.microsoft.com/en-us/linkedin/marketing/audiences/
- Token & versioning: https://learn.microsoft.com/en-us/linkedin/marketing/versioning
