# Agent Integration — Pain Point Research

## When to use
- Early-stage discovery when no validated problem yet exists
- Competitor analysis phase: mining negative reviews to find gaps
- Content marketing: identifying questions your audience is actively asking
- Prioritizing a backlog of improvement ideas by actual user pain vs. assumptions
- Researching a new market niche before committing to building

## When NOT to use
- After product-market fit is found: qualitative pain mining is less useful than quantitative retention analysis
- When a decision needs quantitative confidence: pain mining is directional, not statistically significant
- Replacing direct user interviews: forum complaints lack context and nuance
- When the audience is too specialized and has no public online presence (e.g., internal enterprise users)

## Where it fails / limitations
- Public forum signals are biased toward vocal minority — angry users write; satisfied users are silent
- LLMs hallucinate forum posts and review quotes; every quote must be verified against the actual source URL
- Pain scoring (frequency × severity × reach) is heuristic; a human must sanity-check edge cases
- Reddit and App Store data require scraping or manual collection — no universal API for all sources
- Temporal signal is lost when mining: an old pain may already be solved by a competitor update

## Agentic workflow
Pain point research is well-suited for a two-agent pipeline: a research agent collects raw pain signals from specified sources (with WebSearch or tool access), and a synthesis agent applies the Pain Intensity Matrix to rank and categorize findings. The human's role is to supply source URLs and review the final scored list before using it for decisions. Agents work well here because the task is repetitive pattern recognition over large text volumes.

### Recommended subagents
- `faion-sdd-executor-agent` — execute pain research tasks from an SDD implementation plan
- Any general Claude subagent with WebSearch — mine Reddit, G2, App Store reviews for pain signals

### Prompt pattern
```
You are a pain point researcher for the following audience: <audience>.
Search the following sources for complaints, frustrations, and workarounds:
Sources: <list of URLs or search queries>
For each pain found, output:
| Pain | Source | Category (Time/Money/Complexity/Integration/Reliability) | Quote | Severity (1-5) |
Do NOT paraphrase quotes — copy verbatim.
```

```
Given the following raw pain point list, score each using this formula:
Score = (Frequency×0.3) + (Severity×0.25) + (Reach×0.2) + (Spend×0.15) + (Alternatives×0.1)
Scale each dimension 1-5. Output a sorted table with scores.
Pain list: <paste list>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| snscrape | Twitter/X scraping (no API key needed) | `pip install snscrape` / github.com/JustAnotherArchivist/snscrape |
| PRAW | Reddit API Python wrapper | `pip install praw` / praw.readthedocs.io |
| google-play-scraper | App Store review scraping (Android) | `pip install google-play-scraper` |
| app-store-scraper | iOS App Store review scraping | `pip install app-store-scraper` |
| Playwright | Browser automation for sites without APIs | `pip install playwright` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reddit API | OSS/SaaS | Yes (REST API + PRAW) | Read-only; rate-limited at 60 req/min |
| G2 | SaaS | Partial (no public review API) | Scraping only; exports require login |
| Capterra | SaaS | No public API | Manual or browser automation required |
| Trustpilot | SaaS | Partial (API for business owners) | Review data requires business account |
| App Store Connect | SaaS | Partial (no review API) | Use `app-store-scraper` library |
| Google Play | SaaS | Yes (via `google-play-scraper`) | Reviews accessible without API key |

## Templates & scripts
See `templates.md` for the Pain Point Research Log and Reddit Mining Template.

Inline script — Reddit PRAW pain collector:
```python
# reddit_pain_collector.py — collect top posts matching pain keywords
import praw

reddit = praw.Reddit(client_id="ID", client_secret="SECRET", user_agent="pain-research/1.0")
subreddit = reddit.subreddit("freelance")
keywords = ["hate", "frustrated", "annoying", "waste", "can't figure", "broken"]

results = []
for submission in subreddit.search(" OR ".join(keywords), sort="top", limit=50):
    results.append({
        "title": submission.title,
        "score": submission.score,
        "url": submission.url,
        "body": submission.selftext[:300],
    })

for r in sorted(results, key=lambda x: -x["score"])[:20]:
    print(f"{r['score']:5d}  {r['title']}")
    print(f"       {r['url']}")
```

## Best practices
- Mine at least 3 source types to triangulate (forum complaints + review sites + job boards)
- Record the source URL for every quote — verification is required before any decision
- Group pains into categories before scoring; categorization reveals systemic patterns invisible in individual items
- Use job board queries ("looking for someone to...") to find pain points users are willing to pay to outsource
- Run pain mining monthly for active markets — pain landscape shifts with competitor product updates
- Note who is complaining (segment) as carefully as what they are complaining about

## AI-agent gotchas
- LLMs will confabulate plausible-sounding Reddit posts or review quotes — always verify with source links
- Do not ask an agent to scrape live sites directly without tool integration; instruct it to process pre-collected data
- Pain scoring is subjective; agent scores should be treated as a starting hypothesis, not ground truth
- Human checkpoint before using scored output: the researcher must read the top 5 raw pain items themselves
- Agents cannot assess recency of complaints; a heavily upvoted complaint from 3 years ago may be irrelevant today

## References
- https://www.reddit.com/dev/api/ (Reddit API docs)
- praw.readthedocs.io (PRAW Python library)
- Rob Fitzpatrick, "The Mom Test" — on separating signal from noise in customer conversations
- https://www.intercom.com/blog/pain-points/
- Clayton Christensen, "The Innovator's Dilemma" — root cause of underserved pain
