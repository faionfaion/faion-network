# Agent Integration — Google Ads Campaign Setup

## When to use
- Templating new Google Ads accounts: agent provisions a "starter" Search campaign with conversion tracking, RSAs, extensions, and naming convention enforced.
- Onboarding agency / multi-tenant clients where the same campaign skeleton repeats across many accounts.
- Pre-launch QA: agent walks the campaign-launch checklist and refuses to flip status to `ENABLED` until every item passes.
- Migrating from manual campaigns to Smart Bidding by templating fresh campaigns and copying historical conversions for the algorithm to learn from.

## When NOT to use
- One-off campaigns where the human launches in the UI in 20 minutes; API setup overhead doesn't pay back.
- Campaigns that depend on UI-only features (some recommendations, brand suitability tweaks, certain Performance Max settings).
- Heavily creative-led campaigns where the asset/copy variation is the work; setup is a small fraction.
- Already-running accounts with established Smart Bidding — re-templating restarts learning and tanks performance.

## Where it fails / limitations
- "Maximize Conversions" without seeded conversion data wastes budget for ~14 days during learning.
- API supports nearly all settings, but newer features (Demand Gen, some PMax controls, brand-suitability) trail the UI by months.
- Conversion tracking requires `gtag.js` / GTM on the site — purely API-driven setup cannot install client-side tracking; humans must verify it fires.
- Sitelink, callout, and structured-snippet extensions live as `Asset` resources in newer API versions; older code referencing `*Extension` resources breaks.
- Location targeting accepts `geoTargetConstants/<id>`; agents using country names as strings fail validation.
- "Search Network only" is the default UI rec but NOT the API default — campaigns silently opt into Search Partners and Display unless explicitly disabled.
- Some campaign types (PMax) have hard prerequisites (asset groups, audience signals) that single-step setup scripts miss.

## Agentic workflow
Setup agent reads a YAML "campaign spec" (objective, budget, locations, languages, ad-group themes, assets, extensions). It validates the spec, calls Google Ads API in order: budget → campaign → ad groups → keywords → assets → RSAs → extensions, and emits a final "what was created" report. Status is left as `PAUSED` for human review before flipping to `ENABLED`. Always pair with the `google-ads-reporting` agent so a fresh campaign is monitored from minute one.

### Recommended subagents
- `faion-ads-agent` — campaign creation + mutation calls.
- `faion-feature-executor` — wraps "set up new client account" as a multi-step SDD task.
- `faion-sdd-executor-agent` — runs quality gates around the campaign-spec parser + idempotency tests.
- A copy-generation sub-agent for headline/description drafting that the executor consumes.

### Prompt pattern
```
System: You are the campaign-setup agent. Always create with status PAUSED.
        Default network = Search only (target_search_network=False,
        target_content_network=False, target_partner_search_network=False).
        Refuse to ENABLE without conversion tracking verified firing in
        the last 24 hours and at least one RSA per ad group.
User:   Bootstrap a Search campaign for SaaS X: $50/day, US+CA, en, three
        ad-group themes [main, alternative, competitor]. Use spec.yaml.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | API client | `pip install google-ads` |
| Google Ads Editor | Bulk offline edit + diff before pushing | https://ads.google.com/intl/en/home/tools/ads-editor/ |
| Google Tag Manager | Conversion tracking install (web side) | https://tagmanager.google.com |
| Google Tag Assistant | Verify tag fires correctly | https://tagassistant.google.com |
| `pyyaml` / `pydantic` | Validate the campaign spec YAML before API calls | `pip install pyyaml pydantic` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads (Search) | SaaS | Yes (API) | The base surface this methodology targets. |
| Google Ads Editor | desktop | Partial | Useful for diff/preview when API output is unclear. |
| Google Analytics 4 | SaaS | Yes (Data API) | Conversion definitions imported into Ads as conversion actions. |
| Google Tag Manager | SaaS | Yes (API) | Container management; can install gtag programmatically. |
| Optmyzr / Adalysis | SaaS | Yes | Pre-built audits + bulk launchers if you don't want to roll your own. |
| Looker Studio | SaaS | Partial | Dashboard for the freshly-launched campaign. |

## Templates & scripts
See `templates.md` for the campaign / ad-group / RSA templates. Inline pre-launch gate script the agent must pass before flipping `ENABLED`:

```python
# launch_gate.py — pre-flight checks for a Google Ads campaign
def can_enable(client, customer_id: str, campaign_id: int) -> dict:
    ga = client.get_service("GoogleAdsService")
    rows = list(ga.search(customer_id=customer_id, query=f"""
        SELECT ad_group.id, ad_group_ad.ad.id, ad_group_ad.ad.responsive_search_ad.headlines,
               campaign.network_settings.target_content_network,
               campaign_budget.amount_micros
        FROM ad_group_ad
        WHERE campaign.id = {campaign_id}
    """))
    issues = []
    if not rows:
        issues.append("no ads in campaign")
    if any(r.campaign.network_settings.target_content_network for r in rows):
        issues.append("Display network is on — disable for Search-only")
    for r in rows:
        if len(r.ad_group_ad.ad.responsive_search_ad.headlines) < 3:
            issues.append(f"ad {r.ad_group_ad.ad.id}: <3 headlines")
    if rows and rows[0].campaign_budget.amount_micros < 1_000_000:
        issues.append("budget <$1/day — likely a unit error")
    return {"ok": not issues, "issues": issues}
```

## Best practices
- Generate a campaign-spec schema (pydantic / JSON Schema) and validate before any API call — most setup failures are typos.
- Default to PAUSED status; require an explicit "go-live" step.
- Lock naming convention to a regex; agents producing "Test Test 1" should fail their own lint.
- Verify conversion tracking fires (Tag Assistant or gtag debug) BEFORE creating any campaign that targets a conversion goal.
- Start with Maximize Conversions (no Target CPA) for the first 30 conversions; switch to Target CPA only after enough data lands.
- Add all relevant assets (sitelinks, callouts, structured snippets) at account or campaign level; missing them lowers ad-rank meaningfully.
- For multi-account agency setups, drive everything from a CSV / YAML so spec changes are reviewable in git before they hit accounts.
- Set `start_date` / `end_date` explicitly; default end-date is "forever" and agents that forget to set it accumulate stale forever-running campaigns.

## AI-agent gotchas
- Network-settings default trap: agents that omit `network_settings.*` get Search Partners + Display turned ON; verify post-create.
- Budget micros confusion (1,000,000 = $1) — same trap as everywhere in Google Ads.
- Location targeting accepts `geoTargetConstants/2840`, not `"United States"`. Agents emitting strings fail.
- RSA char limits (30 / 90); agents producing borderline-length headlines should run length validation client-side.
- Conversion-tracking install runs OUTSIDE the API; agents that mark "tracking installed" without verifying gtag fires create silent-fail campaigns.
- Smart Bidding: setting a manual CPC bid on a Smart Bidding campaign no-ops — agents that "fix" performance this way achieve nothing.
- Human-in-loop checkpoint: enabling the campaign, raising budget >25%, switching bid strategy, removing extensions, opening a new geo.
- Asset versioning: extensions are now `Asset` resources; agents using deprecated `Extension` services hit "deprecated resource" errors.
- DSA / Performance Max have non-trivial extra setup (page feeds, asset groups). One-size-fits-all setup scripts skip these and produce broken campaigns.

## References
- Campaign setup guide — https://support.google.com/google-ads/answer/6324971
- Bidding strategies overview — https://support.google.com/google-ads/answer/2472725
- Responsive Search Ads — https://support.google.com/google-ads/answer/7684791
- Asset-based extensions — https://developers.google.com/google-ads/api/docs/extensions/overview
- Conversion tracking — https://support.google.com/google-ads/answer/1722022
