# Agent Integration — Distribution Channel Research

## When to use
- Pre-launch GTM planning when the team has a product hypothesis but no validated path to first 100 users.
- Post-launch when one channel is saturating and CAC is climbing — research adjacent channels before scaling spend.
- B2B/B2C pivots where the buyer or buying motion changes (PLG → sales-led, or vice versa) and the existing channel mix is no longer aligned.
- Solopreneur side-projects where the founder has limited bandwidth and must pick 1 channel to master, not 5 to dabble in.
- Periodic audits (every 2 quarters) of the active channel mix against actual customer-source data from analytics + interviews.

## When NOT to use
- Pre-PMF — channels do not fix a broken product; running channel tests before retention works produces misleading CAC and burns budget.
- Pure word-of-mouth products with strong existing organic pull (e.g. category leader with 60%+ direct traffic) — formal research adds little signal.
- One-off campaigns (event launch, single press hit) where the question is "creative" not "channel".
- When the data the research depends on (customer interviews, attribution analytics) does not exist and cannot be collected within the research window — any output will be conjecture.

## Where it fails / limitations
- Garbage-in attribution: last-click analytics over-credits paid search and under-credits content/community; the research output inherits that bias unless multi-touch + self-reported attribution are merged.
- Channel saturation drift: CAC numbers from competitor case studies are 12–24 months stale; LinkedIn Ads CPC, Google Ads CPC, and TikTok CPM all moved 2x+ in that window.
- Survivorship bias in "how competitors got users": public case studies skew toward channels that worked; you rarely see the 5 channels they killed.
- LTV uncertainty for early-stage products kills the LTV:CAC math — you cannot threshold a 3:1 ratio when LTV has a 10x confidence interval.
- The 5-step process implies a clean linear flow; in practice steps 2 (channel fit) and 3 (economics) iterate 3–5 times as new data arrives.

## Agentic workflow
Drive this methodology with a 3-stage subagent chain: a discovery agent gathers customer attribution + competitor channel evidence, a scoring agent applies the channel-fit matrix and economic model, and a test-design agent produces a ranked test plan with budgets and stop criteria. Use the repo's `faion-research-agent` orchestrator (see `skills/faion-knowledge/knowledge/pro/research/researcher/CLAUDE.md`) in `competitors` + `niche` modes to seed channel evidence; pass its output to a market-researcher subagent for scoring, then to a marketing/growth subagent (see `pro/marketing/growth-marketer`, `pro/marketing/gtm-strategist`, `pro/marketing/ppc-manager`) for execution-side reality checks (creative cost, platform constraints, ad-account requirements).

### Recommended subagents
- `faion-research-agent` (mode `competitors`) — pulls competitor primary/secondary channels, ad library snapshots, SimilarWeb traffic mix.
- `faion-research-agent` (mode `personas`) — produces "where they hang out" inputs for Step 1 (customer discovery map).
- `faion-domain-checker-agent` — only relevant if the channel test requires landing-page domains; cheap pre-flight check.
- `growth-marketer` knowledge (`pro/marketing/growth-marketer`) — channel-economics modeling and test-design templates.
- `ppc-manager` knowledge (`pro/marketing/ppc-manager`) — paid-channel CPC/CTR benchmarks and ad-account preflight.
- `gtm-strategist` knowledge (`pro/marketing/gtm-strategist`) — phasing across 0→10K→50K MRR portfolios.

### Prompt pattern
```
Role: distribution-channel research subagent.
Inputs: ICP={...}, product={...}, competitors=[...], current_channels=[...], LTV_estimate=$X.
Tasks:
 1. Map top 5 customer-discovery sources (cite interviews/analytics/competitor evidence; refuse to invent numbers).
 2. Score channels against fit matrix (audience, cost, time, scale, capability). Output table.
 3. Model economics per channel using stated LTV and benchmark CPC ranges (cite source + date).
 4. Recommend Phase-1 test plan: 1 primary + 1 backup, budget $500-2K, 4-6 week window, stop criteria.
Constraints: no time estimates in days, only complexity (low/med/high). Flag any unverified numbers with [UNVERIFIED].
Return: markdown sections matching templates.md.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gpt-researcher` (OSS) | Multi-source channel discovery research with citations | https://github.com/assafelovic/gpt-researcher |
| `firecrawl` | Scrape competitor pricing/landing pages used in channel inference | https://www.firecrawl.dev/ |
| `tavily` API | Citation-backed web search optimized for agents | https://tavily.com/ |
| `serpapi` / `searxng` | SERP scraping for keyword + competitor ad surfaces (NERO runs SearXNG self-hosted) | https://serpapi.com / `~/workspace/tools/searxng` |
| `meta-ad-library-api` | Pull competitor Meta ads to infer paid-social investment | https://www.facebook.com/ads/library/api |
| `google-ads-transparency` | Inspect competitor Google Ads creatives | https://adstransparency.google.com/ |
| `similarweb` API | Traffic source mix per competitor domain | https://developer.similarweb.com/ |
| `ahrefs` / `semrush` API | Organic + paid keyword footprint | https://ahrefs.com/api, https://www.semrush.com/api/ |
| `posthog` / `plausible` CLI + API | Self-attribution data export for "how did you hear about us" + UTM analysis | https://posthog.com/docs/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SparkToro | SaaS | API (paid) | Audience hangout discovery (sites, podcasts, social handles) — feeds Step 1. |
| BuiltWith | SaaS | API | Detect martech stack to infer channels competitors invest in. |
| SimilarWeb | SaaS | API (paid) | Channel mix per domain (search/social/direct/referral). |
| Ahrefs / Semrush | SaaS | API | Organic + paid keyword exposure, content gap. |
| Meta Ad Library | Free public | Public API + scrape | Snapshot of active Meta/Instagram ad creatives. |
| Google Ads Transparency | Free public | Scrape only | No formal API, scrape with Playwright. |
| TikTok Creative Center | Free public | Scrape | Trending creatives + audience insights. |
| LinkedIn Ad Library | Free public | Scrape | B2B ad transparency. |
| PostHog | OSS + cloud | API | Self-host attribution + UTM funnels; agent-writable events. |
| Plausible / Umami | OSS | API | Lightweight referrer + UTM stats. |
| Hotjar / FullStory | SaaS | API | Session-level "how did you arrive" + on-page surveys. |
| Typeform / Tally | SaaS | API | "How did you hear about us" surveys; Tally has a free tier and agent-friendly REST. |
| Customer.io / Loops | SaaS | API | Drive referral-loop and lifecycle channel tests. |
| Rewardful / FirstPromoter | SaaS | API | Affiliate/referral channel instrumentation. |
| Clay.com | SaaS | API | Outbound list-building + enrichment for sales-led channel tests. |

## Templates & scripts

The methodology's `templates.md` is currently empty. Inline channel-fit scorer below produces the Step-2 matrix from a YAML input. See `README.md` Step 2 for the weighting scheme.

```python
# channel_fit_scorer.py — score channels vs. fixed weights, emit markdown table
# usage: python channel_fit_scorer.py channels.yaml
import sys, yaml
WEIGHTS = {"audience": .25, "competitors": .15, "cost": .20,
           "time": .15, "scale": .15, "capability": .10}
def score(ch):
    s = sum(ch["scores"][k] * w for k, w in WEIGHTS.items())
    return round(s, 2)
def main(path):
    data = yaml.safe_load(open(path))
    rows = [(c["name"], c["scores"], score(c)) for c in data["channels"]]
    rows.sort(key=lambda r: -r[2])
    cols = list(WEIGHTS.keys())
    head = "| Channel | " + " | ".join(cols) + " | Total |"
    sep  = "|" + "---|" * (len(cols) + 2)
    print(head); print(sep)
    for name, sc, total in rows:
        cells = " | ".join(str(sc[k]) for k in cols)
        print(f"| {name} | {cells} | {total} |")
if __name__ == "__main__":
    main(sys.argv[1])
```

Companion `channels.yaml`:
```yaml
channels:
  - name: SEO
    scores: {audience: 5, competitors: 5, cost: 4, time: 2, scale: 5, capability: 4}
  - name: LinkedIn Ads
    scores: {audience: 4, competitors: 4, cost: 2, time: 5, scale: 4, capability: 3}
  - name: Referral
    scores: {audience: 3, competitors: 2, cost: 5, time: 3, scale: 3, capability: 5}
```

## Best practices
- Anchor every channel claim in either a customer interview (N≥5), an attribution datapoint, or a dated benchmark — reject anonymous "industry says" assertions in agent output.
- Run customer-source surveys with a free-text "How did you hear about us?" field, not a dropdown — dropdowns force respondents into the wrong bucket and corrupt Step 1.
- Treat the LTV:CAC > 3:1 rule as a Phase-2 gate, not a Phase-1 gate; Phase-1 micro-tests are buying signal, not unit economics.
- For each channel test, predefine a kill criterion (e.g. "if CAC > $X after $500 spend, kill") before money is spent — prevents sunk-cost continuation.
- Separate "channel" from "creative": a failed Meta Ads test often means failed creative, not failed channel; rerun with 3 distinct creative concepts before killing.
- Record competitor channel observations with capture date — Meta/TikTok ad libraries are time-windowed and the evidence rots fast.
- For B2B, weight referral and integrations channels higher than the matrix suggests if the product has any network or co-sell surface.
- Keep the "20% experiments" budget non-negotiable even when the primary channel is working; channel concentration risk is the #1 GTM failure mode at $100K+ MRR.

## AI-agent gotchas
- LLMs hallucinate CPC, CPM, and conversion benchmarks confidently — require the agent to cite source + date for every economic number, and reject answers that fail the citation requirement.
- Agents over-recommend SEO and content marketing because training data is saturated with those examples; explicitly prompt for non-obvious channels (integrations, marketplaces, niche communities, podcasts).
- Last-click attribution baked into agent reasoning under-credits dark social, podcast, and community — feed self-reported attribution data alongside analytics or the recommendation will be wrong.
- LTV estimates are the largest source of error in agent-produced economics; require sensitivity analysis (low/mid/high LTV) rather than a point estimate.
- Channel research output reads plausible but un-actionable when the agent skips Step 4 (test plan with budget + stop criteria) — enforce that section as required output.
- Do not let the agent commit to a "Phase 1 / Phase 2 / Phase 3" calendar; per workspace rules, no time estimates — phases are gated by milestones (e.g. "after 100 paying customers"), not weeks.
- Human-in-the-loop checkpoints: (1) sign off on the customer-source data before scoring, (2) sign off on benchmark sources before economics, (3) approve test budget before any spend.
- When the agent has zero customer interviews, it will fall back to competitor inference; flag this explicitly in the output header so the reader knows the input quality.

## References
- Gabriel Weinberg & Justin Mares — *Traction: How Any Startup Can Achieve Explosive Customer Growth* (the 19-channel "bullseye framework" that this methodology compresses).
- Brian Balfour — Four Fits framework: market/product/channel/model fit. https://brianbalfour.com/four-fits-growth-framework
- Andrew Chen — *The Cold Start Problem* (network-channel mechanics for viral/integration channels).
- a16z — Growth metrics + channel benchmarks. https://a16z.com/the-metrics-that-matter/
- First Round — How to think about distribution. https://review.firstround.com/
- Lenny's Newsletter — Channel benchmarks by stage. https://www.lennysnewsletter.com/
- Reforge — Growth Series channel-economics curriculum. https://www.reforge.com/
