# Agent Integration — Twitter/X Growth

## When to use
- Generating daily tweet batches (3-5 posts) across content pillars for a defined brand voice and audience
- Drafting threads: hook tweet, promise tweet, 5-8 value tweets, summary + CTA
- Writing bio, pinned tweet, and banner copy for profile optimization
- Producing build-in-public update templates (monthly revenue, wins/losses, next steps)
- Analyzing tweet performance data (exported CSV) to identify which content types and hooks drive most engagement

## When NOT to use
- Automated posting or replying — X API Basic tier limits post creation; bot-style automation risks account suspension
- Generating content for trending topics without current context — agent's knowledge of what is trending is outdated
- Mass DM outreach — X ToS prohibits unsolicited commercial DMs at scale; agent-generated sequences sent in bulk will get the account flagged
- Engagement pods — coordinated inauthentic engagement violates platform rules and is detectable

## Where it fails / limitations
- Tweet hooks that perform well are highly context-specific (niche, audience maturity, current events); agent hooks are structural templates, not guaranteed performers
- X algorithm behavior (distribution of threads vs single tweets, effect of external links) changes frequently and is undocumented
- Build-in-public content requires real data (MRR, user counts, churn); the agent can produce the template but cannot fill in authentic numbers
- The "reply to large accounts" strategy requires knowing which accounts are currently relevant in the niche — agent cannot browse Twitter to identify them
- Analytics CSV structure varies by export method (Twitter Analytics native, Tweetdeck, third-party); agent must be given column names to parse correctly

## Agentic workflow
Two-phase approach: (1) weekly content generation — Haiku call produces 20-30 tweet drafts and 2 thread outlines from pillar definitions and brand voice; human selects, personalizes, and schedules; (2) monthly performance review — Sonnet call consumes analytics CSV export and produces engagement rate analysis, top hook pattern identification, and next-month pillar adjustment recommendations. Human executes all posting and engagement; agent handles content drafting and analysis.

### Recommended subagents
- `faion-sdd-executor-agent` — execute Twitter growth SDD tasks (profile audit, content calendar setup, analytics review)
- `password-scrubber-agent` — clean DM or follower data exports before analysis

### Prompt pattern
```
You are a Twitter/X content strategist for <niche>. Brand voice: <voice>. ICP: <icp>.
Content pillars: <pillar_1> (40%), <pillar_2> (30%), <pillar_3> (20%), personal (10%).

Generate this week's content:
- 15 single tweets (3/day Mon-Fri), mix of opinions, tips, and questions
- 1 thread (8 tweets): hook + promise + 5 points + summary + CTA
- 1 build-in-public update template (fill-in fields: revenue, users, win, loss, next)

Format each tweet on a separate line. Mark threads with T1, T2, etc.
```

```
Analyze Twitter analytics export:
<csv_with_impressions_engagements_columns>

Find: (1) top 5 tweets by engagement rate, (2) common patterns in their hooks (first 15 words), (3) best-performing days/times, (4) thread performance vs single tweet performance. Output: 3 content strategy recommendations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tweepy` (Python) | Official X API v2 client: read tweets, analytics, followers | `pip install tweepy` / https://docs.tweepy.org |
| `typefully-api` | Draft, schedule, and analyze threads | https://typefully.com/developers |
| `tweetdeck` | Column-based monitoring for reply engagement (manual) | https://tweetdeck.twitter.com |
| `buffer` API | Cross-platform scheduling including X | https://buffer.com/developers/api |
| `hypefury` | X-specific scheduling with auto-retweet and analytics | https://hypefury.com (no public API, use UI) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| X (Twitter) API v2 | SaaS | Yes (OAuth 2.0) | Read/write access; Basic tier: 1,500 posts/month limit |
| Typefully | SaaS | Yes (API) | Best thread drafting + scheduling; analytics included |
| Buffer | SaaS | Yes (REST API) | Multi-platform; X scheduling supported |
| Hypefury | SaaS | No public API | Auto-retweet, engagement automation; manual UI use |
| TweetDeck | SaaS | No API | Column-based monitoring; manual engagement |
| Shield App | SaaS | Partial (export) | Twitter analytics; better than native analytics export |
| Twemex | Browser ext | No API | Surfaces past tweets in sidebar; inspiration tool |

## Templates & scripts
See `templates.md` for Thread Template, Build in Public Post, and Product Launch Tweet.

```python
# Parse Twitter Analytics CSV for engagement rate analysis
import csv, statistics

def twitter_analysis(csv_path):
    """
    Expects Twitter Analytics export with columns:
    'impressions', 'engagements', 'Tweet text'
    """
    rows, rates = [], []
    with open(csv_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            imp = int(row.get("impressions", 0) or 0)
            eng = int(row.get("engagements", 0) or 0)
            text = row.get("Tweet text", "")[:60]
            if imp > 100:  # filter noise
                rate = eng / imp * 100
                rates.append(rate)
                rows.append((rate, text))
    rows.sort(reverse=True)
    return {
        "avg_engagement_rate": round(statistics.mean(rates), 2) if rates else 0,
        "top_5_hooks": [r[1] for r in rows[:5]],
        "posts_analyzed": len(rates),
    }

result = twitter_analysis("twitter_analytics.csv")
print(result)
```

## Best practices
- The first 15 words of every tweet are the hook — if they do not create curiosity or promise value, nothing else matters
- Thread tweet 1 must standalone as a compelling post without reading the rest; it is the main distribution surface
- External links in tweets reduce reach significantly on X; put links in the first reply or in the bio/pinned tweet instead
- Build-in-public posts with real numbers (MRR, user count, specific percentage) outperform vague narrative posts by 2-5x on engagement
- Reply strategy compounds: being a consistent, early, thoughtful voice in 3-5 large accounts' comments builds recognition faster than standalone posting
- Schedule posts but do not automate replies — algorithmic detection of reply bots has increased; manual engagement is detectable as human and preferred by the platform

## AI-agent gotchas
- **API tier limits:** X API Basic tier allows 1,500 posts/month — agent-driven bulk scheduling can exhaust this; track usage carefully
- **Link suppression:** If the agent includes links in tweet drafts, flag them for relocation to first comment before posting
- **Hook genericness:** Agent thread hooks default to "I went from X to Y in Z days" — this pattern is overused; push for niche-specific, counterintuitive hooks
- **Trending topic blindness:** Agent cannot see current trending conversations; strategy recommendations based on "join trending conversations" require human judgment on what is actually trending
- **Account age matters:** Engagement advice calibrated for established accounts (5K+ followers) does not apply to new accounts; adjust expectations in prompts
- **Policy volatility:** X platform rules and API access have changed rapidly since 2022; any agent recommendation about automation or API use should be validated against current ToS

## References
- https://business.twitter.com/en/resources.html
- https://blog.hootsuite.com/how-to-use-twitter/
- https://buffer.com/twitter
- https://help.twitter.com/en/managing-your-account/using-the-tweet-activity-dashboard
- https://developer.twitter.com/en/docs/twitter-api — X API v2 documentation
