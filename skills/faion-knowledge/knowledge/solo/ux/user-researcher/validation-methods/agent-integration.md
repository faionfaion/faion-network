# Agent Integration — Validation Methods

## When to use
- Early discovery phase: before any code or design work begins
- Deciding whether to pivot a product idea or kill it
- Evaluating a new niche against a portfolio of opportunities
- After user complaints surface — checking if a recurring pain is widespread
- Pre-sprint: confirming a feature addresses a real problem before scoping

## When NOT to use
- When you already have paying customers validating with their wallets
- When the team is iterating on an existing shipped feature (switch to analytics + retention)
- When the hypothesis is too vague to score against the 5-criteria model
- For internal tooling with a captive user base who must use the product

## Where it fails / limitations
- Niche viability scoring is directionally useful but not a precision instrument; weights are opinionated
- Pain-point mining from public forums misses silent majority who don't post
- Search volume signals lag actual demand; niche communities may not search
- Agent-collected evidence from forums/reviews cannot distinguish real users from bots or promotional posts
- Willingness-to-pay responses in interviews are unreliable (stated vs. revealed preference)

## Agentic workflow
A Claude subagent can automate pain-point mining by querying search APIs for forum threads, scraping public review data, and aggregating signals into the Problem Validation Report template. Scoring can be done entirely by the agent when market size data (from Statista, SimilarWeb) and competitor data (Product Hunt, G2) are available as structured inputs. Human validation is required before the final Proceed/Pivot/Kill decision.

### Recommended subagents
- `faion-research-agent` (mode: validate) — runs problem-validation and niche-viability-scoring end-to-end
- `faion-research-agent` (mode: pains) — performs pain-point mining from structured source list

### Prompt pattern
```
You are a product validation agent. Given the problem hypothesis below, collect evidence
across the listed sources, score each criterion, and output a filled Problem Validation Report.
Do NOT recommend a decision — return raw scores and evidence only.

Hypothesis: {who} struggles with {what} because {why}
Sources to mine: Reddit (r/{sub}), App Store ({app}), G2 ({product})
```

```
Score this niche using the 5-criteria model. Return JSON:
{"market_size": {"score": N, "evidence": "..."}, "competition": ..., ...}
Do not apply weights — return raw scores only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ahrefs` / `semrush` API | Search volume, keyword difficulty | ahrefs.com/api, developers.semrush.com |
| `google-trends-api` (pytrends) | Trend signals for problem keywords | `pip install pytrends` |
| `apify` CLI | Scrape Reddit, G2, App Store reviews | `npm i -g apify-cli`, docs.apify.com |
| `jq` | Parse and filter scraped JSON evidence | built-in on most systems |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reddit Search API | OSS (PRAW) | Yes | `pip install praw`; rate-limited without auth |
| G2 Crowd | SaaS | Partial | No official API; Apify actor available |
| Apify | SaaS/OSS | Yes | Actors for Reddit, App Store, G2, Trustpilot |
| SimilarWeb | SaaS | Yes (API tier) | Market size proxies via traffic data |
| Statista | SaaS | Partial | Data exports; no real-time API |
| Exploding Topics | SaaS | No | Manual discovery only |

## Templates & scripts
See `templates.md` for Problem Validation Report and Niche Viability Scorecard.

Inline helper — aggregate Reddit pain mentions by theme:
```python
import praw, collections, re

reddit = praw.Reddit(client_id="...", client_secret="...", user_agent="validator/1.0")

def mine_pains(subreddit: str, query: str, limit: int = 100) -> dict:
    counts = collections.Counter()
    for post in reddit.subreddit(subreddit).search(query, limit=limit):
        text = (post.title + " " + post.selftext).lower()
        for keyword in ["slow", "broken", "missing", "hate", "wish", "expensive", "confusing"]:
            if keyword in text:
                counts[keyword] += 1
    return dict(counts.most_common())

results = mine_pains("projectmanagement", "frustrating OR hate OR problem", limit=200)
print(results)
```

## Best practices
- Collect evidence from at least 3 independent source types before scoring; single-source validation is fragile
- Use verbatim quotes as primary evidence — paraphrases lose signal in synthesis
- Apply the 5-criteria model AFTER evidence collection, not during, to avoid confirmation bias
- For niche scoring, research market size from multiple proxies (search volume + TAM reports + competitor revenue estimates) and take the geometric mean
- Record your Proceed/Pivot/Kill decision log with the evidence snapshot so future agents can re-evaluate as new data arrives
- Pain-point mining is most reliable on platforms where users are not trying to sell something (Reddit > LinkedIn)

## AI-agent gotchas
- Agents will hallucinate search volume numbers if the search API is not provided; always inject real data as context
- G2 and Trustpilot block automated scraping aggressively — use cached Apify datasets or rate-limit to 1 req/5s
- Pain-point categorization by LLM is inconsistent across runs; use a fixed taxonomy and ask the agent to classify, not generate categories
- Niche viability scoring requires the agent to have explicit market size data; without it, the agent will anchor on vague impressions and produce unreliable scores
- Human checkpoint required before acting on Proceed/Kill decisions — agent can surface evidence but not own the strategic call

## References
- Rob Fitzpatrick: *The Mom Test* — interview-based problem validation
- Strategyzer: Value Proposition Design (Osterwalder et al.)
- https://www.nngroup.com/articles/discovery-phase/
- https://praw.readthedocs.io — Python Reddit API Wrapper
- https://docs.apify.com/api/v2 — Apify scraping platform
