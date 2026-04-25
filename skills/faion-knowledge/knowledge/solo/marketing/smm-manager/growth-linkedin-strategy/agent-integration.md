# Agent Integration — LinkedIn Strategy

## When to use
- Drafting a batch of LinkedIn posts (text, carousels, story posts) aligned to defined content pillars
- Generating personalized connection request messages and DM welcome sequences for a specific ICP
- Auditing a LinkedIn profile (headline, About, Featured) and producing rewrite suggestions
- Analyzing engagement data exports to identify top-performing content patterns
- Building a 4-week content calendar with post types, topics, and posting times

## When NOT to use
- Real-time engagement (commenting, replying) — requires human authenticity; automated comments are detectable and harm credibility
- LinkedIn Sales Navigator automation — violates LinkedIn ToS; accounts get banned
- Generating content for accounts the agent has no brand context for — generic posts perform poorly
- Replacing human relationship-building in DMs — initial nurture sequences can be drafted but must be sent and adapted by a human

## Where it fails / limitations
- Agent-generated posts often lack the personal story specificity that drives LinkedIn engagement; they need editing to add real anecdotes
- LinkedIn algorithm behavior is undocumented and changes without notice — timing and format recommendations go stale
- Carousel creation requires a separate visual design step (Canva/Figma); the agent produces text + slide structure only
- Engagement rate analysis requires exporting LinkedIn analytics CSV; the agent cannot pull live platform data
- The personalized DM formula is effective only if the agent receives real profile data for the recipient

## Agentic workflow
Use a two-stage pipeline: a planning subagent consumes brand context, ICP definition, and content pillars to produce a monthly calendar JSON, then a drafting subagent generates post drafts per calendar slot using the templates from `templates.md`. Human review and personal-story injection happen between stages. For profile audits, a single Sonnet call with the current profile text as input and the README framework as system prompt is sufficient.

### Recommended subagents
- `faion-sdd-executor-agent` — execute structured LinkedIn content calendar tasks from a spec
- `password-scrubber-agent` — strip personal data from analytics exports before processing

### Prompt pattern
```
You are a LinkedIn content strategist. Given:
- Content pillars: <pillars>
- ICP: <icp>
- Brand voice: <voice>

Generate 5 LinkedIn post drafts: 2 personal story posts, 2 how-to posts, 1 carousel outline (10 slides). Follow the hook-gap-story-value-CTA structure from the style guide.
```

```
Audit this LinkedIn profile for <role>. Score each element (Headline, About, Featured, Experience) 1-10. Provide specific rewrites for anything below 7.

Profile:
<profile_text>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linkedin-api` (Python) | Unofficial read-only API for profile and post data | `pip install linkedin-api` / https://github.com/tomquirk/linkedin-api |
| `shield-app` CLI export | Analytics CSV export from Shield (requires Shield account) | https://shieldapp.ai — manual export, parse with pandas |
| `buffer` CLI | Schedule posts via Buffer API | https://buffer.com/developers/api |
| `canva-cli` | Programmatic carousel creation (Canva Apps SDK) | https://www.canva.com/developers/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Buffer | SaaS | Yes (REST API) | Schedule posts; supports LinkedIn pages and profiles |
| Hootsuite | SaaS | Yes (REST API) | Multi-platform scheduling; analytics export |
| Shield | SaaS | Partial (manual export) | Best LinkedIn-specific analytics; CSV exportable |
| LinkedIn Marketing API | SaaS | Yes (OAuth) | Official API; limited for personal profiles |
| Taplio | SaaS | No public API | LinkedIn growth tool; useful for manual inspiration |
| Canva | SaaS | Yes (Apps SDK) | Carousel and banner generation |
| PhantomBuster | SaaS | Yes (API) | Automation for connection requests — use carefully, ToS risk |

## Templates & scripts
See `templates.md` for Story Post, How-To Post, and Carousel Structure templates.

```python
# Parse Shield analytics CSV to find top 5 posts by engagement rate
import csv

def top_posts(csv_path, n=5):
    rows = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            impressions = int(row.get("impressions", 0) or 0)
            engagements = int(row.get("engagements", 0) or 0)
            if impressions > 0:
                row["eng_rate"] = engagements / impressions
                rows.append(row)
    rows.sort(key=lambda r: r["eng_rate"], reverse=True)
    return rows[:n]

for post in top_posts("shield_export.csv"):
    print(f"{post['eng_rate']:.1%} — {post['text'][:80]}")
```

## Best practices
- Write the first line of every post as if it is the only line the reader will see — LinkedIn truncates after 2-3 lines; the hook must earn the "see more" click
- Avoid posting links in the body text of posts — LinkedIn suppresses external link posts; put URLs in the first comment
- Comment quality on others' posts compounds over time — one substantive comment on a 50K-follower post can drive more profile visits than a standalone post
- Carousel posts have the highest save rate on LinkedIn; prioritize them for evergreen frameworks
- Creator Mode enables the newsletter CTA and follower button; enable it before any growth push
- Personalize connection requests with a specific observation — generic requests have a 20-30% acceptance rate vs 50%+ for personalized ones

## AI-agent gotchas
- **ToS boundary:** LinkedIn's automation policies prohibit scraping and bulk messaging; agent-driven outreach must stay within manual-equivalent rates (5-10 connection requests/day)
- **Personal story gap:** Agent drafts are structural scaffolds — the human must inject specific dates, dollar amounts, and named individuals before posting; generic LinkedIn content performs below average
- **Engagement timing:** The agent cannot monitor when a post goes live to trigger early-engagement behavior; human must be available for first-hour engagement
- **Analytics lag:** LinkedIn analytics have a 24-48h delay; agent analysis on fresh posts will underestimate reach
- **Creator Mode state:** Agent profile audits must know whether Creator Mode is enabled — the profile elements and CTA options differ significantly

## References
- https://business.linkedin.com/marketing-solutions
- https://www.linkedin.com/help/linkedin (Help Center)
- https://blog.hootsuite.com/how-to-use-linkedin/
- https://buffer.com/linkedin
- https://shieldapp.ai — LinkedIn analytics benchmarks
