# Agent Integration — Google Performance Max

## When to use
- E-commerce or lead-gen advertisers with solid conversion tracking (≥30 conv/month) wanting cross-channel reach (Search + YouTube + Display + Gmail + Discover + Maps) under one campaign.
- Existing Smart Shopping campaigns being migrated (Google deprecated Smart Shopping → PMax in 2022).
- Established brands with rich asset libraries (5+ images, 5+ videos, multiple text variants) and strong audience signals.
- Accounts seeking to consolidate spend and let Google's AI handle channel arbitrage.

## When NOT to use
- New accounts with <30 conversions in last 30 days — PMax cannot exit learning phase, burns budget randomly.
- Brands needing channel-level transparency (PMax hides which placements/queries spend went to; reporting is asset-group level only).
- Pure brand-defense search campaigns — PMax cannibalizes branded search and inflates CPA.
- Niche B2B with narrow ICP — PMax goes broad by default, breaks targeting precision.
- Compliance-heavy verticals (housing, employment, credit) — Google restricts PMax automation here.

## Where it fails / limitations
- Black-box reporting: no query-level visibility unless you pull the `search_term_view` (recently exposed but limited). You cannot block specific queries before damage.
- URL expansion enabled by default sends traffic to pages you may not want indexed for ads.
- Asset group reporting buckets: `Best`, `Good`, `Low`, `Pending` — qualitative, not quantitative.
- Negative keyword support added 2023 but limited to account-level via support request; campaign-level negatives via API only.
- 4-6 week learning phase; pausing/restarting resets it.
- Audience signals are hints, not constraints — PMax can ignore them if optimizer disagrees.
- Cannot see individual placement CPA — only campaign-level.

## Agentic workflow
A subagent owns the asset-group lifecycle: gather creative → generate text-asset variants from product/landing-page content → upload via google-ads-python → monitor asset performance label → swap low-performers weekly. Critical: agents must enforce minimum-asset thresholds (5 headlines, 5 long headlines, 4 descriptions, 4 images) BEFORE submission or campaign goes nowhere. Human-in-loop: brand-safety review of generated copy, target ROAS/CPA changes, URL expansion toggle.

### Recommended subagents
- `faion-ads-agent` — runs PMax campaign + asset-group + asset-group-asset mutations against the Google Ads API.
- A purpose-built `pmax-asset-refresher` subagent — weekly: pull asset performance, identify `Low` labels, generate replacements via LLM grounded on product copy, queue for human approval.
- `faion-sdd-executor-agent` (existing) — runs setup as a multi-step task with QA gates (asset count, conversion-tracking sanity check).

### Prompt pattern
```
You are a PMax asset-group builder. Inputs: product URL, brand voice doc, image URLs.
Generate JSON with:
- 5 headlines (≤30 chars each, distinct value props)
- 5 long_headlines (≤90 chars)
- 4 descriptions (≤90 chars, include CTA)
Validate char limits. Reject any output with truncation.
```

```
Audit PMax asset performance for last 14 days. Asset labels: <list>.
For each `Low` label, propose a replacement preserving brand tone.
Output: {keep: [...], retire: [...], replacements: [{type, text, rationale}]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` SDK | Full PMax campaign / asset / asset-group ops | `pip install google-ads`, developers.google.com/google-ads/api/docs/client-libs/python |
| Google Ads Editor | Bulk offline edits, including PMax asset groups | ads.google.com/intl/en/home/tools/ads-editor/ |
| Google Ads Scripts (JS) | In-account automation, no external infra | developers.google.com/google-ads/scripts |
| `googleads-bash` | curl-based for quick checks | github.com/googleads/google-ads-api-utilities |
| Looker Studio (Google Ads connector) | Asset-group performance dashboards | datastudio.google.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads UI | SaaS native | Yes via API | Some PMax features UI-only briefly after release |
| Optmyzr | SaaS | Yes — API | PMax script library, asset alerts |
| AdEspresso | SaaS | Limited | More Meta-focused, partial PMax coverage |
| Adriel | SaaS | Yes | Cross-channel reporting incl. PMax |
| Triple Whale | SaaS | Yes | E-comm attribution incl. PMax incrementality |
| Google Merchant Center | SaaS native | Yes — Content API | Required for retail PMax (product feed) |

## Templates & scripts
See `templates.md` for asset-group structure. See `examples.md` for full Python setup. The README contains full `create_performance_max_campaign`, `create_asset_group`, and `add_asset_group_assets` functions — ready for agent use.

Inline helper for asset-performance audit:

```python
# pmax_asset_audit.py
from google.ads.googleads.client import GoogleAdsClient

def audit_assets(client, customer_id, asset_group_id):
    ga = client.get_service("GoogleAdsService")
    q = f"""
      SELECT asset_group_asset.field_type, asset_group_asset.performance_label,
             asset.text_asset.text, asset.resource_name
      FROM asset_group_asset
      WHERE asset_group_asset.asset_group = '{asset_group_id}'
    """
    by_label = {"BEST": [], "GOOD": [], "LOW": [], "PENDING": []}
    for row in ga.search(customer_id=customer_id, query=q):
        label = row.asset_group_asset.performance_label.name
        by_label.setdefault(label, []).append({
            "type": row.asset_group_asset.field_type.name,
            "text": row.asset.text_asset.text,
            "resource": row.asset.resource_name,
        })
    return by_label
```

## Best practices
- Wait for ≥30 conversions before turning on Target CPA/ROAS — otherwise the bidder over-fits to noise.
- Start with Maximize Conversions (no target) for 14 days, then layer the target.
- Keep budget at minimum 3x target CPA daily, otherwise PMax stalls on auction-bidding constraints.
- Use audience signals from your best-converting customer-match list, not generic interest segments — PMax weights converter-similarity heavily.
- Always disable URL expansion for shopping/lead-gen unless your site is small and every page is conversion-relevant.
- Add account-level negative keywords (request via support) for brand-protection terms competitors might trigger on.
- Run PMax alongside (not instead of) branded Search to keep brand-defense intact and avoid attribution muddle.
- Refresh assets quarterly minimum; PMax fatigue manifests as gradual CPA creep, not a sudden cliff.

## AI-agent gotchas
- Asset-type field enums change across API versions (e.g., `MARKETING_IMAGE` vs `LANDSCAPE_LOGO`); pin the API version and refresh client stubs on Google's release schedule (~quarterly).
- The `customer_id` must be unhyphenated (`1234567890`, not `123-456-7890`); easy bug if pulled from UI clipboard.
- Image upload uses asset resource names — agents must `mutate_assets` first, then reference, in the same call to a fresh API session token.
- `final_urls` requires HTTPS; agent submitting `http://` will see a generic auth-failure error, not a clear schema error.
- Conversion goals must be configured AT THE ACCOUNT level for PMax to optimize correctly — agents must validate `conversionAction` resources before campaign creation, otherwise PMax silently optimizes for the wrong action.
- Performance label values lag 7-14 days; agents triggering creative swap on Day-3 data will churn assets unnecessarily.
- API requires login-customer-id header for MCC accounts — easy 401 if missing on multi-account agents.
- Budget micros: $50/day = `50_000_000` (multiply by 1M), unlike LinkedIn (which uses local-currency floats).

## References
- Performance Max Campaigns: https://support.google.com/google-ads/answer/10724817
- API reference (PMax): https://developers.google.com/google-ads/api/docs/performance-max/overview
- Asset group reference: https://developers.google.com/google-ads/api/reference/rpc/v17/AssetGroup
- Asset performance labels: https://support.google.com/google-ads/answer/12433993
- Audience signals API: https://developers.google.com/google-ads/api/docs/performance-max/audience-signals
