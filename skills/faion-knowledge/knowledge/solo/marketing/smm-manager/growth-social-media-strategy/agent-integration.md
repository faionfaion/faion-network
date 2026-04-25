# Agent Integration — Social Media Strategy

## When to use
- Building a platform selection scorecard given a specific ICP, product type, and content capability
- Drafting a 4-week content calendar with pillar distribution, post types, and scheduling slots
- Generating a batch of post drafts (text posts, threads, carousels) for a defined pillar and platform
- Producing a monthly strategy review template: what worked, what to double down on, what to cut
- Creating a social media brief for a new product or campaign (platform, pillars, frequency, KPIs)

## When NOT to use
- Real-time trend hijacking — requires human to judge whether a trend fits brand voice and is safe to join
- Competitor monitoring and reactive content — speed and judgment are required; agent batches are too slow
- Community management and comment response — must be human for relationship quality
- Generating content for all platforms simultaneously from one prompt — quality degrades; run platform-specific prompts

## Where it fails / limitations
- Platform algorithm preferences change without documentation updates; agent recommendations on posting times and formats go stale within 3-6 months
- Content pillar distribution (40/30/20/10) is a starting heuristic, not a law; real performance data overrides it
- The agent cannot observe actual post performance; it requires the human to feed in analytics before refining strategy
- Cross-platform repurposing requires adaptation the agent often misses — a Twitter thread repurposed to LinkedIn verbatim underperforms
- The 5-5-5 engagement method requires daily human attention; agent cannot execute it

## Agentic workflow
Run strategy in two phases: (1) planning — a single Sonnet call with brand/ICP/resource constraints produces platform selection, pillar definitions, frequency targets, and KPI baselines; (2) execution — a Haiku call batch-generates post drafts from the plan. Inject real engagement data monthly for a Sonnet strategy review. Human executes posting and engagement; agent handles content generation and analysis only.

### Recommended subagents
- `faion-sdd-executor-agent` — drive through monthly social media planning tasks from a spec
- `password-scrubber-agent` — clean any analytics exports containing PII before analysis

### Prompt pattern
```
You are a social media strategist for a <product_type> targeting <ICP>. Given:
- Platform: <platform>
- Content pillars: <pillars>
- Posting frequency: <frequency>
- Brand voice: <voice>

Generate a 4-week content calendar. Output JSON:
{
  "week": 1-4,
  "day": "Mon"-"Sun",
  "pillar": "...",
  "post_type": "text|thread|carousel|video",
  "topic": "...",
  "hook_draft": "..."
}
```

```
Platform scorecard: score Twitter/X, LinkedIn, Instagram, TikTok 1-5 for each criterion:
- ICP audience present
- Content type match for <product_type>
- Competitor activity level
- Organic reach potential in 2026

Recommend the top 1-2 platforms with rationale.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `buffer` API | Schedule posts across platforms | https://buffer.com/developers/api |
| `hypefury` | Twitter/X and LinkedIn scheduling with analytics | https://hypefury.com (no public API) |
| `later` API | Instagram, TikTok, Pinterest scheduling | https://developers.later.com |
| `brand24` API | Brand mention monitoring | https://brand24.com/api |
| `sprout-social` API | Full multi-platform analytics export | https://developers.sproutsocial.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Buffer | SaaS | Yes (REST API) | Post scheduling; analytics export per platform |
| Hootsuite | SaaS | Yes (REST API) | Enterprise scheduling + analytics |
| Sprout Social | SaaS | Yes (REST API) | Best analytics export; expensive |
| Later | SaaS | Yes (REST API) | Strong for Instagram/TikTok visual planning |
| Hypefury | SaaS | No public API | Twitter/LinkedIn-focused; manual use |
| Brand24 | SaaS | Yes (REST API) | Mention tracking; sentiment tagging |
| Canva | SaaS | Yes (Apps SDK) | Visual content creation for carousels |
| CapCut | SaaS | No API | Video editing; manual use |

## Templates & scripts
See `templates.md` for Content Calendar Template and platform-specific post templates (Twitter thread, LinkedIn post).

```python
# Weekly engagement rate tracker from platform analytics CSVs
import csv, statistics

def engagement_summary(csv_path, impressions_col, engagements_col):
    rates = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            imp = int(row.get(impressions_col, 0) or 0)
            eng = int(row.get(engagements_col, 0) or 0)
            if imp > 0:
                rates.append(eng / imp * 100)
    if not rates:
        return {}
    return {
        "avg_engagement_rate": round(statistics.mean(rates), 2),
        "median_engagement_rate": round(statistics.median(rates), 2),
        "top_post_rate": round(max(rates), 2),
        "posts_analyzed": len(rates),
    }

print(engagement_summary("twitter_export.csv", "impressions", "engagements"))
```

## Best practices
- Choose platform based on where the ICP already spends time, not where it is easiest to post — follower migration is slow
- Batch content creation into 2-3 hour weekly sessions rather than daily single-post creation; consistency improves and creative quality is higher in blocks
- The 80/20 value-to-promo rule is minimum; for accounts under 1K followers, go 95/5 — trust is not yet established
- Engagement time (5-5-5 method) drives more growth than posting frequency for accounts under 10K followers; if forced to choose, engage over post
- Track engagement rate, not follower count, as the primary KPI for the first 6 months — follower growth is a lagging indicator
- Platform analytics are available natively and free; use them before paying for third-party tools

## AI-agent gotchas
- **Stale algorithm knowledge:** Agent recommendations for optimal posting times and formats reflect training data, not current platform behavior; validate against native analytics quarterly
- **Tone mismatch across platforms:** One-shot cross-platform content generation produces copy that is too Twitter-terse for LinkedIn or too LinkedIn-formal for Twitter; run separate prompts per platform
- **Volume trap:** Agents can generate unlimited content, leading to over-posting that burns audience goodwill; constrain output to the human-validated frequency targets
- **CTA fatigue:** Agent-generated posts tend to add the same CTA template to every post; rotate CTAs and omit them entirely from value posts
- **Analytics interpretation:** Engagement rate spikes from a viral post skew monthly averages; flag outliers before using data to adjust strategy

## References
- https://blog.hootsuite.com/social-media-marketing/
- https://sproutsocial.com/insights/
- https://buffer.com/resources/
- https://blog.hubspot.com/marketing/social-media-strategy
- Vaynerchuk, G. (2013). *Jab, Jab, Jab, Right Hook*. HarperBusiness.
