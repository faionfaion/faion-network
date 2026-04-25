# Agent Integration — Influencer Marketing

## When to use
- Need to reach new audiences via trusted voices when SEO/paid ads have plateaued or unit economics are unfavorable.
- Launching a product to a niche where 10-100K micro-influencers drive purchase decisions (DTC, SaaS prosumer, creator tools).
- Building UGC pipeline cheaply via gifting + reuse rights, instead of producing content in-house.
- Pre-launch: seeding to micro creators in target niche to generate authentic content for D-day amplification.

## When NOT to use
- B2B enterprise (>$10K ACV) where buying committees ignore creator endorsements; prefer analyst relations/case studies.
- Highly regulated verticals (medical, financial advice, securities) where FTC + sector rules make compliance brittle.
- Sub-$5K marketing budget — fixed costs (vetting, outreach, contracts) erode ROI; better to start with referral programs.
- When product has no clear "hero moment" — creators need a 30-second demo-able value or content falls flat.

## Where it fails / limitations
- Vanity reach metrics: "2M impressions" with zero conversions because audience doesn't match ICP.
- Bought followers — 30-50% of mid-tier creators show inflated numbers; engagement-rate gating is mandatory.
- One-shot campaigns: single post at single creator yields no compounding effect; long-term ambassadorship outperforms 5x.
- FTC violations (#ad missing, hidden in 30 hashtags) — creates legal exposure and platform downranking.
- Attribution: last-touch credits the creator but iOS 14.5 + cookie loss break tracking; rely on UTM + discount codes.

## Agentic workflow
Claude subagents are strong at the discovery, vetting, and outreach phases — they can scrape candidate lists, score engagement-rate quality, and draft personalized outreach at volume. Keep contract negotiation, content approval, and payment release under human control. Treat the workflow as four phases: discover (agent) → vet (agent + human gate) → outreach (agent) → execute (human + agent for reporting).

### Recommended subagents
- `general-purpose` — discovery scraping, audience overlap analysis, engagement-rate scoring per candidate.
- `faion-content-agent` (referenced in README) — drafting personalized outreach DMs and campaign briefs aligned with brand voice.
- `password-scrubber-agent` — sanitize affiliate-link spreadsheets and rate cards before sharing externally.

### Prompt pattern
- "Given this list of 50 Instagram handles in [niche], pull follower count, last-90-day engagement rate, and audience-country breakdown. Flag any with >5x follower spike in last 30 days as suspect."
- "For each vetted creator, draft a 5-line outreach DM referencing their most-recent relevant post and proposing [gifting + 15% affiliate]. Output as CSV: handle, hook, body, CTA."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `instaloader` | Scrape public IG profile + post metadata | `pip install instaloader` |
| `yt-dlp` | YouTube channel/video metadata pull | `pip install yt-dlp` |
| `tweepy` | Twitter/X API client for creator metrics | `pip install tweepy` |
| `httpx` + `playwright` | Custom scrapers for TikTok/IG (when API limits hit) | `pip install httpx playwright` |
| `pandas` | Score and rank creator candidates | `pip install pandas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Modash | SaaS | API yes | Discovery + audience demographics, $99+/mo |
| HypeAuditor | SaaS | API yes | Fraud detection, audience-quality score |
| Upfluence | SaaS | API yes | End-to-end CRM + payments |
| CreatorIQ | SaaS | API yes | Enterprise IRM, deep API |
| Aspire | SaaS | Limited API | Mid-market campaign mgmt |
| Grin | SaaS | API yes | Shopify-native, good for DTC |
| Klear | SaaS | API yes | Twitter-heavy discovery |
| BuzzSumo | SaaS | API yes | Content + creator discovery |
| Heepsy | SaaS | API yes | Cheaper Modash alternative |
| Tagger (Sprout) | SaaS | API yes | Acquired by Sprout Social, integrated workflows |

## Templates & scripts
See `templates.md` for outreach email and campaign brief. Inline scoring helper:

```python
# score_creator.py — rank candidates by ICP fit + engagement quality
import pandas as pd

def score(row):
    er = row["engagement_rate"]
    audience_match = row["audience_country_pct_target"]
    suspect = row["follower_spike_90d"] > 3
    if suspect or er < 0.015:
        return 0
    # weights: engagement 0.4, audience match 0.3, niche fit 0.2, content quality 0.1
    return (
        min(er / 0.05, 1.0) * 0.4
        + audience_match * 0.3
        + row["niche_fit_0_1"] * 0.2
        + row["content_quality_0_1"] * 0.1
    )

df = pd.read_csv("candidates.csv")
df["score"] = df.apply(score, axis=1)
df.sort_values("score", ascending=False).head(20).to_csv("shortlist.csv", index=False)
```

## Best practices
- Open with affiliate + gifting hybrid for unproven creators; convert top performers to flat-fee retainers after 60 days of data.
- Use a unique discount code per creator (`SARAH15`) — survives cookie loss, gives clear attribution, doubles as audience incentive.
- Negotiate UGC reuse rights upfront ("90-day paid-social usage rights"); the creative compounds via Meta/TikTok ads at 3-5x ROAS.
- Cohort creators by content style, not follower count — three "deep-review YouTubers" outperform fifteen IG static posts in SaaS.
- Pay micro creators within 7 days; faster-than-industry payment terms become a recruiting moat.

## AI-agent gotchas
- LLMs hallucinate engagement rates and follower counts — always pull live data via API/scrape; never trust a model's "I checked".
- Personalization at scale falls into "I love your work on [TOPIC]" generic patterns; require the agent to quote a specific post URL + line.
- Don't let the agent send DMs autonomously — Instagram/TikTok shadow-ban accounts that exceed ~50 DMs/day; queue + human-confirm.
- Brand-safety filtering: scan last-30-post captions for political/NSFW terms before approving outreach; one bad creator can undo a quarter.
- FTC compliance: agent must include "post must contain #ad in first three hashtags" in every brief — humans still check final post pre/post-go-live.
- Currency conversion: when negotiating with creators in IN/BR/PH, get the agent to quote both USD and local currency; mismatched expectations break deals.

## References
- FTC Endorsement Guides: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Modash API docs: https://modash.io/docs/api
- HypeAuditor fraud-detection methodology: https://hypeauditor.com/blog/
- Influencer Marketing Hub Benchmark Report (annual)
