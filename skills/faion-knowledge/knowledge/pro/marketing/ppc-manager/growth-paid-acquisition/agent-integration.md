# Agent Integration — Paid Acquisition (Growth)

## When to use
- Founder / solopreneur needs a structured "ads from zero" workflow with unit-economics gating before any spend.
- Routinely launching campaigns across multiple channels and you want a single agent to orchestrate channel selection, structure, tracking, and weekly optimization.
- Codifying the test → kill → scale loop so the same playbook applies to Meta, Google, LinkedIn without re-thinking it.
- Generating weekly performance reports + reallocation recommendations across mixed channels.

## When NOT to use
- LTV / payback period not modelled — agents will happily scale unprofitable ad sets if the human supplies fake numbers.
- Pre-product-market-fit; ads amplify your funnel, they do not fix conversion below ~1% landing-page CVR.
- Pure brand / awareness spend where ROI is intentionally indirect — this methodology is performance-first.
- Single-channel pure execution (just Google Search) — use the channel-specific methodologies (`google-search-ads`, `facebook-ads`) directly.

## Where it fails / limitations
- The methodology assumes platform conversion data is correct; iOS ATT, ad-blockers, and walled-garden self-reporting silently distort it.
- LTV:CAC of 3:1 is a heuristic, not a law — subscription churn, refunds, fraud can flip a "winner" in month 3.
- "Kill after 1000 impressions" works for high-intent search, fails for upper-funnel video where 10k impressions is the minimum signal.
- Weekly cadence is too slow for fast-moving e-com promotions (Black Friday) and too fast for B2B with 90-day sales cycles.
- Cross-channel attribution is hand-waved here — pair with `ads-attribution-models` for a defensible rollup.
- Budget benchmarks ($500/mo Meta minimum etc.) are channel-defaults; specific verticals (legal, finance) need 5-10x that.

## Agentic workflow
Use a planner-executor split: a strategy agent (`opus` model) calculates LTV / CAC / max-CPA, picks the channel, drafts campaign + ad-set structure; an execution agent (`haiku` model) creates resources via `google-ads-basics` / `facebook-ads`. A weekly review agent runs the kill/scale rules from this methodology against the previous 7 days of data. Always gate `ENABLE` and any budget increase >25% behind a human checkpoint. Persist decisions (kill, scale, hold) to a small log so the agent can explain "why we paused this" later.

### Recommended subagents
- `faion-ads-agent` — channel-specific execution (Meta + Google Ads APIs).
- `faion-sdd-executor-agent` — wraps tracking-pixel installation + UTM helpers as feature work.
- `faion-feature-executor` — useful when paid-acquisition ties into a broader "launch a campaign" SDD task graph.
- `faion-brainstorm` — diverge/converge agent for generating 5+ creative angles when the human is stuck.

### Prompt pattern
```
System: You are the growth strategist. Refuse to recommend any spend until
        you've recorded LTV, target CAC, and tracking status. Use the
        kill/scale rules: CTR<0.5% & 1k impressions=kill, CPA<target for
        3 days=scale +25%. All recommendations must cite the data row.
User:   Plan week 1 of paid acquisition for a $30/mo SaaS with $400 LTV
        and 3% trial→paid conversion. Budget: $1500.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | Google Ads execution | `pip install google-ads` |
| `facebook-business` | Meta Ads execution | `pip install facebook-business` |
| `gtag` / `gtag-helpers` | Conversion / pixel install (browser side) | https://developers.google.com/tag-platform |
| `dbt` | LTV cohort modelling on raw warehouse data | https://docs.getdbt.com |
| `urlcanon` / hand-rolled UTM builder | Consistent UTM tagging across channels | any |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads | SaaS | Yes (API) | High-intent / search; required for SaaS B2B. |
| Meta Ads | SaaS | Yes (Marketing API) | B2C; needs CAPI for iOS-era signal. |
| LinkedIn Ads | SaaS | Yes (Marketing API) | B2B; expensive but converts. |
| TikTok Ads | SaaS | Yes (Marketing API) | Young/B2C/viral; creative-hungry. |
| GA4 | SaaS | Yes (Data API) | Source of truth for cross-channel CVR + cohorts. |
| BigQuery + Looker Studio | SaaS | Yes (SQL/REST) | Where weekly reports actually live. |
| Triple Whale / Northbeam | SaaS | Yes | E-com MMM + channel deduplication. |
| Unbounce / Webflow / Carrd | SaaS | Partial (API) | Landing-page builders an agent can populate. |

## Templates & scripts
See `templates.md` for the campaign-planning template + weekly-report template. Inline LTV/CAC gate the agent should run before any new campaign:

```python
# unit_econ_gate.py — refuse to launch if ratios are bad
def unit_econ_ok(arpu_monthly: float, lifetime_months: float,
                 conv_rate: float, cac: float):
    ltv = arpu_monthly * lifetime_months
    max_cpa = (ltv / 3) * conv_rate
    payback_months = cac / arpu_monthly if arpu_monthly else float("inf")
    ok = ltv >= 3 * cac and payback_months <= 12
    return {
        "ok": ok,
        "ltv": ltv,
        "ltv_cac_ratio": round(ltv / cac, 2) if cac else None,
        "max_cpa": round(max_cpa, 2),
        "payback_months": round(payback_months, 1),
        "reason": None if ok else "LTV:CAC<3 or payback>12mo — fix before scaling",
    }
```

## Best practices
- Lock the unit-economics inputs (ARPU, churn, gross margin) to the warehouse, not a slide deck — agents read fresh values weekly.
- Standardize UTM grammar before the first campaign: `utm_source` = platform, `utm_medium` = `paid`, `utm_campaign` = stable slug. Agents enforce.
- Start narrow: one channel, one offer, 3-5 audiences, 3-5 creatives. Expanding to a second channel before mastering the first dilutes signal.
- Track the leading indicator (CTR, CPC) AND the lagging one (CPA, ROAS). Agents that only watch ROAS miss creative fatigue.
- 20–30% budget increments only when scaling; >50% jumps reset platform learning and tank performance.
- Route every channel's spend through one ledger (warehouse table) — never compare platform reports head-to-head; they over-attribute.
- Have a kill list per week. If the agent has zero kills, it's not looking hard enough.

## AI-agent gotchas
- LLMs love to "optimize" winning ads by tweaking copy mid-flight, killing performance. Lock winners for ≥7 days.
- "Conversions" reported by platforms double-count; agents that sum across platforms report inflated revenue. Use GA4 / warehouse total.
- Models often skip the LTV gate if the user gives them a budget directly. Hard-code the gate as a precondition.
- Human-in-loop checkpoints: enabling a campaign, increasing daily budget by >25%, expanding to a new channel, opening a new geo.
- Time-based reasoning is weak: agents will compare a 3-day-old campaign to a 90-day baseline. Force "min-data" assertions before judging.
- Creative tone drift: agent-written ad copy on its 5th iteration becomes generic. Reset the creative agent with fresh brand-voice context.
- Currency / FX: multi-region accounts mix USD/EUR/GBP cost rows; agents must normalize before computing CPA.

## References
- LTV / CAC primer (Brian Balfour) — https://brianbalfour.com/quick-takes/ltv-cac
- Reforge growth methodology — https://www.reforge.com/programs/growth-series
- WordStream PPC benchmarks — https://www.wordstream.com/blog/ws/2023/02/20/ppc-benchmarks
- GeoLift incrementality (Meta) — https://github.com/facebookincubator/GeoLift
- Andrew Chen — startup growth essays — https://andrewchen.com
