# Agent Integration — Distribution Channel Research (Market-Researcher)

> Market-researcher variant. Focus: channel economics at the **market level**, partner-landscape mapping (distributors, resellers, marketplaces, integration partners), and channel-share quantification across competitors. For the GTM-execution / brand-side angle (test design, creative iteration, internal channel mix), see the sibling file in `pro/research/researcher/distribution-channel-research/agent-integration.md`.

## When to use
- Market entry analysis: a client/founder needs to know which channels actually move volume in a target market before committing GTM spend (e.g. "is dental SaaS sold via direct, marketplace, or channel partners in DACH?").
- Investor / strategy decks where the channel-economics slide must show market-level CPC/CAC ranges and partner take-rates with sourced citations, not back-of-envelope guesses.
- Channel-share studies: quantifying what % of category revenue flows through SEO vs paid vs partner vs direct sales across the top 10 incumbents.
- Partner-landscape mapping for B2B: identifying every distributor, reseller, MSP, marketplace, and integration partner that touches the buyer journey, with reach/exclusivity/take-rate per partner.
- Pricing & business-model research that depends on channel margin stack-ups (e.g. SaaS direct 70% gross margin vs. AWS Marketplace listing −3% take vs. reseller −20%).
- Refreshing channel benchmarks when incumbent CPC/CPM/CAC numbers in the deck are >12 months old.

## When NOT to use
- Founder needs creative/copy/test-design help — that is a growth-marketing job, not market research; route to `pro/marketing/growth-marketer` or the researcher-variant of this methodology.
- Pre-PMF single-product validation where the question is "does anyone want this" — channel research at that stage is premature optimization.
- Pure brand campaigns or one-off launches with no recurring channel decision.
- Markets where channel data is structurally unavailable (private niches, enterprise with NDAs, regulated verticals with no ad libraries) — output will be conjecture; flag and stop.
- When the requester has not specified a market boundary (geo + segment + buyer); without a boundary the channel-share denominator is undefined.

## Where it fails / limitations
- Channel-share denominators are noisy: SimilarWeb traffic mix is a proxy for channel-share, not a measurement of revenue-share; for B2B with 6-month sales cycles the gap is enormous.
- Partner take-rates are rarely public — public marketplace fees (AWS 3%, Shopify 0–20%, App Store 15–30%) are anchors, but private reseller margins (15–40%) are negotiated and leak only via job posts, RFPs, and partner-portal scrapes.
- Ad-library coverage is uneven: Meta + Google have full transparency in EU/Brazil, partial in US; LinkedIn + TikTok ad libraries are shallow; B2B podcast and newsletter sponsorship has no library at all.
- Survivorship in case studies: published "we got to $10M via SEO" stories are 1-of-100 — channel-share inference from public stories overweights organic and underweights paid.
- LTV uncertainty kills market-level LTV:CAC modeling — the right output is a **range with sensitivity bands**, not a point estimate, and agents that produce point estimates are silently wrong.
- Geographic averaging: blending US + EU + APAC CPC into one number masks 5x regional variance that destroys the strategic recommendation.
- "Channel" is fractal: "paid social" is not one channel — Meta Reels, Meta Feed, IG Stories, LinkedIn Sponsored, LinkedIn InMail behave differently. Pick the right granularity for the market question or the analysis is meaningless.

## Agentic workflow
Drive market-level channel research with a 4-stage chain. (1) **Boundary agent** locks geo + segment + buyer + product category and produces a market-definition spec — refuse to proceed without it. (2) **Channel-share agent** quantifies traffic/revenue mix across the top 10 incumbents using SimilarWeb + Ahrefs + ad libraries, emits a market-level channel-share table with confidence bands. (3) **Partner-landscape agent** maps every distributor / reseller / marketplace / integration partner, with reach, exclusivity, and known/inferred take-rate. (4) **Economics agent** layers benchmark CPC/CPM/CAC on the channel-share table and runs LTV sensitivity (low/mid/high) to produce LTV:CAC ranges per channel. The repo's `faion-research-agent` (mode `competitors` and `niche`) seeds steps 2–3; pass its citation-rich output to a market-researcher subagent for normalization. Cross-check economics with `pro/marketing/ppc-manager` knowledge (paid benchmarks) and `pro/marketing/growth-marketer` (LTV modeling). All four stages must cite source + capture date for every number.

### Recommended subagents
- `faion-research-agent` (mode `competitors`) — pulls per-competitor traffic mix, ad creatives, partner mentions, marketplace listings.
- `faion-research-agent` (mode `niche`) — produces market boundary + buyer-journey scaffold for stage 1.
- `faion-research-agent` (mode `pricing`) — feeds margin / take-rate context for partner-economics math.
- `faion-domain-checker-agent` — cheap pre-flight when partner / marketplace listings imply microsite domains for verification.
- `pro/research/market-researcher/competitor-analysis` knowledge — per-competitor channel inference.
- `pro/research/market-researcher/market-research-tam-sam-som` knowledge — sets the revenue denominator that channel-share is computed against.
- `pro/marketing/ppc-manager` knowledge — current paid-channel CPC/CPM/CAC benchmarks with regional splits.
- `pro/marketing/growth-marketer` knowledge — LTV modeling and sensitivity bands.
- `pro/marketing/gtm-strategist` knowledge — interprets channel-share output for portfolio recommendations.

### Prompt pattern
```
Role: market-level distribution-channel research subagent (market-researcher).
Inputs: market_boundary={geo, segment, buyer, category},
        incumbents=[top10_domains], LTV_low/mid/high=[$X,$Y,$Z],
        analysis_depth={share|partners|economics|all}.
Tasks:
 1. Verify market boundary is well-defined; if any field is missing, STOP and request it.
 2. For each incumbent: extract traffic-source mix (cite SimilarWeb date),
    paid-ad presence (cite ad-library date), partner/marketplace listings.
 3. Aggregate to market-level channel-share table with confidence bands
    (HIGH if >=7 incumbents agree, MED if 4-6, LOW if <=3).
 4. Map partner landscape: distributors, resellers, marketplaces, integrations.
    For each: reach (S/M/L), exclusivity (Y/N), take-rate (cite or [INFERRED]).
 5. Layer benchmark CPC/CPM/CAC ranges per channel (cite source + date,
    regional split if multi-geo).
 6. Run LTV:CAC at low/mid/high LTV, output ranges not points.
Constraints:
 - Every number cites source + capture date or is flagged [UNVERIFIED].
 - No time estimates; complexity tags only (low/med/high).
 - If <3 incumbents have data, return LOW-confidence and recommend primary research.
Return: markdown matching templates.md sections 1-5.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `similarweb` API | Per-domain traffic-source mix; foundation of market-level channel-share | https://developer.similarweb.com/ |
| `ahrefs` / `semrush` API | Organic + paid keyword footprint per competitor; partner-mention extraction | https://ahrefs.com/api, https://www.semrush.com/api/ |
| `sparktoro` API | Audience hangouts, podcasts, newsletters used by buyer segment | https://sparktoro.com/api |
| `builtwith` API | Martech + analytics + affiliate stack per domain → infers channel investment | https://api.builtwith.com/ |
| `meta-ad-library-api` | Active Meta/IG ads per competitor with spend bands (EU only) | https://www.facebook.com/ads/library/api |
| `google-ads-transparency` (scrape) | Active Google Ads creatives per advertiser; no formal API → Playwright | https://adstransparency.google.com/ |
| `linkedin-ad-library` (scrape) | B2B sponsored content snapshots | https://www.linkedin.com/ad-library/ |
| `tiktok-creative-center` | Trending creatives + advertiser inspector | https://ads.tiktok.com/business/creativecenter |
| `crunchbase` / `pitchbook` API | Partner-mention extraction from press releases + funding context | https://data.crunchbase.com/ |
| `gpt-researcher` (OSS) | Multi-source partner-landscape research with citations | https://github.com/assafelovic/gpt-researcher |
| `firecrawl` | Scrape competitor "Partners" / "Resellers" / "Integrations" pages | https://www.firecrawl.dev/ |
| `tavily` API | Citation-backed web search for take-rate and partner economics | https://tavily.com/ |
| `searxng` | Self-hosted SERP for niche / non-English markets (NERO ships SearXNG) | `~/workspace/tools/searxng` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SimilarWeb | SaaS | API (paid) | Channel-share denominator. Required input. |
| Ahrefs / Semrush | SaaS | API (paid) | Organic + paid footprint, content-gap, ad-history. |
| SparkToro | SaaS | API (paid) | "Where does the audience hang out" → partner / podcast surface. |
| BuiltWith | SaaS | API | Infers channel investment from martech stack (e.g. has FirstPromoter → affiliate channel active). |
| Meta Ad Library | Free public | API + scrape | EU-complete, US-partial; capture date matters. |
| Google Ads Transparency | Free public | Scrape | Capture creatives + run-windows per advertiser. |
| LinkedIn Ad Library | Free public | Scrape | Shallow but only B2B option. |
| TikTok Creative Center | Free public | Scrape | Audience + creative trends, not full ad library. |
| Pathmatics / AdBeat | SaaS | API (paid, enterprise) | Cross-channel ad-spend estimates per competitor — best partner-spend source if budget permits. |
| Crayon / Klue | SaaS | API | Competitor-intel platforms with channel-mix dashboards. |
| Crunchbase / PitchBook | SaaS | API | Partner mentions in press releases, M&A history, channel-partner deals. |
| Owler | SaaS | API | Public competitor monitoring incl. partner announcements. |
| AWS / Azure / GCP Marketplace | Public | Scrape | Listing presence + private-offer mechanics → channel investment signal. |
| AppSumo / Product Hunt | Public | API + scrape | Tail-channel exposure for SaaS launches. |
| G2 / Capterra / TrustRadius | Public | API/scrape | Review-volume and "users found us via" signals. |
| Reforge / a16z / First Round | Content | Manual | Periodic channel-benchmark publications; cite with date. |

## Templates & scripts

The methodology's `templates.md` covers the channel-research report and channel-test report. Below is a market-researcher-specific extension: a market-level channel-share table and a partner-landscape table, plus a Python helper that converts per-competitor traffic mixes into a market-level channel-share table with confidence bands.

```python
# market_channel_share.py — aggregate per-competitor traffic mix to market-level
# usage: python market_channel_share.py mix.yaml
# mix.yaml shape:
#   competitors:
#     - {name: A, weight: 1.0, mix: {direct: .35, search_organic: .30, search_paid: .10, social: .15, referral: .05, mail: .05}}
#     - ...
import sys, yaml, statistics
def aggregate(rows):
    chans = sorted({k for r in rows for k in r["mix"].keys()})
    out = {}
    for c in chans:
        vals = [r["mix"].get(c, 0.0) for r in rows]
        wts  = [r.get("weight", 1.0) for r in rows]
        wsum = sum(wts) or 1
        mean = sum(v*w for v, w in zip(vals, wts)) / wsum
        spread = max(vals) - min(vals)
        n_nonzero = sum(1 for v in vals if v > 0)
        if n_nonzero >= 7:   conf = "HIGH"
        elif n_nonzero >= 4: conf = "MED"
        else:                conf = "LOW"
        out[c] = {"share": round(mean, 3), "spread": round(spread, 3),
                  "n": n_nonzero, "conf": conf}
    return out
def render(agg):
    print("| Channel | Market Share | Spread (max-min) | N | Confidence |")
    print("|---|---|---|---|---|")
    for c, r in sorted(agg.items(), key=lambda x: -x[1]["share"]):
        print(f"| {c} | {r['share']*100:.1f}% | {r['spread']*100:.1f}pp | {r['n']} | {r['conf']} |")
def main(p):
    data = yaml.safe_load(open(p))
    render(aggregate(data["competitors"]))
if __name__ == "__main__":
    main(sys.argv[1])
```

Partner-landscape table (markdown skeleton):

```markdown
| Partner | Type | Reach | Exclusivity | Take-rate | Source | Capture date |
|---------|------|-------|-------------|-----------|--------|--------------|
| AWS Marketplace | Marketplace | L | N | 3% | AWS docs | YYYY-MM-DD |
| Reseller X | Reseller | M | Y (region) | ~25% [INFERRED] | job post | YYYY-MM-DD |
```

## Best practices
- Lock the **market boundary** (geo + segment + buyer + category) before any channel work; an unbounded market produces meaningless channel-share.
- Use weighted aggregation when computing market-level channel-share: weight each competitor by revenue or traffic (proxy: SimilarWeb monthly visits) — not equal weights — so micro-competitors do not skew the picture.
- Capture every public channel datapoint with `source + URL + capture-date` triple; ad libraries and traffic estimates rot in weeks.
- Report channel-share as a **range with confidence band** (HIGH/MED/LOW) tied to N of competitors with available data, not a single number.
- Always include **regional splits** for multi-geo markets — global averages hide 3–5x CPC variance that breaks the strategic recommendation.
- For partner take-rates: report public marketplace fees as facts; report reseller / channel-partner margins as `[INFERRED]` with the inference path (job post wording, RFP leak, partner-portal screenshot).
- Treat channel-share + partner-landscape outputs as **dated snapshots**, not standing truth — refresh quarterly for active markets, semi-annually for slow markets.
- Use LTV sensitivity (low/mid/high) bands not point estimates — investors and operators need to see the cliff.
- Cross-check ad-library evidence with traffic mix: a competitor with 0% paid in SimilarWeb but 200 active Meta ads is a measurement artifact, not a contradiction — flag it.
- Separate **buy-side channels** (where the buyer searches) from **fulfillment channels** (how the product is delivered) — for B2B SaaS sold via AWS Marketplace, the channel-share table needs both rows.
- Avoid the 7-tier portfolio recommendation cliché ("Phase 1 SEO, Phase 2 paid…") in market-research output — that is GTM-strategist work, not market research; stop at the channel-share + partner-landscape + economics tables.

## AI-agent gotchas
- Boundary skipping: agents will happily produce "channel mix for SaaS" without a geo or segment — enforce a stop-and-ask gate before any data work.
- Number hallucination: agents fabricate plausible CPC, CPM, take-rate, and traffic-share values; require source + URL + capture-date for every number, and reject answers that fail the citation check.
- US-bias: training data overweights US benchmarks; for non-US markets force the agent to source regional data (Statista, eMarketer regional, local Ad libraries).
- Confidence-band omission: agents collapse channel-share into single percentages — explicitly require N + confidence band per row.
- Survivorship lean: agents will overweight famous "we won via SEO" stories — prompt for the **silent majority** (incumbents that never wrote a Medium post) by sampling top-10 by traffic, not top-10 by content output.
- Partner-landscape under-reporting: agents miss MSPs, VARs, and SI partners because those rarely have web presence — require the agent to scrape "Partners / Resellers / Find a partner" pages of each incumbent and capture every named entity.
- Equal-weight aggregation bug: agents default to averaging across competitors equally; explicitly demand traffic- or revenue-weighted aggregation.
- LTV point-estimate bug: agents output a single LTV:CAC ratio; require low/mid/high sensitivity or reject the answer.
- Time-estimate leak: per workspace rules, no time estimates — agents will sneak in "Phase 1 = 3 months"; strip time language at output validation.
- Stale benchmarks: agents quote 2022 CPCs; require capture-date >= last 12 months for any economic number, else `[UNVERIFIED]`.
- Channel granularity collapse: "paid social" lumped together is a tell — force per-platform breakdown (Meta Feed, Meta Reels, IG Stories, LinkedIn Sponsored, TikTok In-Feed, X Ads).
- Human-in-the-loop checkpoints: (1) approve market boundary, (2) approve incumbent list before scraping, (3) approve confidence-band thresholds, (4) sign off on `[INFERRED]` take-rates before circulation.

## References
- Gabriel Weinberg & Justin Mares — *Traction* — 19-channel bullseye framework (channel taxonomy reference).
- Brian Balfour — *Four Fits Growth Framework*: market/product/channel/model fit. https://brianbalfour.com/four-fits-growth-framework
- Andrew Chen — *The Cold Start Problem* — network and integration channel mechanics.
- a16z — Marketplace metrics and take-rate benchmarks. https://a16z.com/the-metrics-that-matter/
- McKinsey / BCG — B2B channel-share studies (paywalled but citable).
- Statista / eMarketer — regional CPC/CPM benchmarks (paywalled, mandatory for multi-geo).
- IAB — Internet Advertising Bureau revenue reports (channel-share at the macro level, by quarter). https://www.iab.com/insights/
- Pathmatics / AdBeat — paid-channel competitive intelligence.
- Lenny's Newsletter — channel benchmarks by stage. https://www.lennysnewsletter.com/
- Reforge — Growth Series channel-economics curriculum. https://www.reforge.com/
- Sibling researcher-variant: `pro/research/researcher/distribution-channel-research/agent-integration.md` (GTM-execution focus).
