# Agent Integration — Trend Analysis

## When to use
- Pre-niche-selection: deciding if a vertical has tailwind before committing 6+ months.
- Quarterly portfolio review: re-scoring active bets against fresh signals (funding, search volume, hiring).
- New-product wedge hunting: pairing STEEP output with personal-fit filter to short-list 3-5 ideas.
- Competitor threat scan: detecting that a category you operate in is shifting stage (early → mainstream → decline).
- Content/SEO planning: catching a search term inflection point so blog/SEO bets land before Big Players arrive.

## When NOT to use
- Sub-week tactical decisions (today's content topic, a single ad creative) — trend windows are months, not days.
- Validating an already-paying problem: customer-development interviews beat trend-extraction here.
- Pure science/research questions that need ground-truth data, not directional momentum.
- Deeply local B2B niches where there is no public signal source (Google Trends/HN/PH all blank).
- When you already have product-market fit — switching on every shiny trend is the failure mode this methodology warns against.

## Where it fails / limitations
- **Survivorship bias in sources.** HN/PH/Crunchbase over-index on dev-tooling and SF-flavored startups; consumer-physical and emerging-market trends barely register.
- **Lagging signal mistaken for leading.** Gartner Hype Cycle and McKinsey reports trail the actual inflection by 12-18 months.
- **Google Trends noise.** Tiny-volume terms get smoothed to zero; new terms have no historical baseline; a term rename (e.g., "AI agent" vs "agentic AI") splits the curve.
- **STEEP scoring is subjective.** Two analysts score the same trend 3.0 and 4.5 — without rubric anchors, the framework becomes self-reinforcing.
- **Counter-trend blindness.** The framework rewards "X is rising" but rarely surfaces "Y collapsed adjacent to X" (e.g., crypto winter killing Web3 dev tools).
- **LLM hallucinated stats.** When agents answer "what is the CAGR of X?" without grounding, they confidently invent numbers — every figure must be source-anchored.

## Agentic workflow
Trend analysis is a fan-out / fan-in pipeline: one orchestrator dispatches per-source collectors (HN, PH, Google Trends, Crunchbase, GitHub, arXiv, job boards), each returning structured signal records; a synthesizer normalizes them into the STEEP and Trend-Strength tables; a critic agent runs counter-signal search ("why might this trend fail?") before recommendation. Run on a recurring cadence (monthly) so the dashboard table compares deltas, not absolute snapshots. Cache raw source pulls to disk so re-runs cost only the synthesis step.

### Recommended subagents
- `faion-market-researcher-agent` — primary orchestrator, owns the STEEP + scoring rubric and final report.
- `faion-research-agent` (mode: `market` / `niche`) — dispatches the multi-source collection in parallel.
- `web-search-collector` (haiku) — runs WebSearch / WebFetch against signal sources, returns JSON rows only.
- `data-quantifier` (sonnet) — converts raw source dumps into Google Trends deltas, GitHub star-velocity, funding totals.
- `counter-signal-critic` (sonnet) — adversarial agent: searches for cooling indicators, failed precedents, regulatory blockers.
- `personal-fit-scorer` (haiku) — applies the user's skill/audience/interest filter from a memory file, prevents shiny-object capture.

### Prompt pattern
```
You are the trend-analysis orchestrator. Analyze trend "{TREND}".
Output ONLY this JSON schema:
{
  "trend": "...",
  "category": "fad|trend|megatrend|shift",
  "stage": "innovator|early|mainstream|decline",
  "evidence": [{"metric":"", "value":"", "yoy":"", "source_url":""}],
  "steep": {"social":"","tech":"","econ":"","env":"","political":""},
  "score": {"growth":1-5,"stage":1-5,"incumbents":1-5,"investment":1-5,"fit":1-5,"weighted_total":0-5},
  "counter_signals": ["..."],
  "recommendation": "pursue|monitor|skip",
  "next_review": "YYYY-MM-DD"
}
Rules: every numeric field MUST cite source_url. If unknown, write "unknown" — never estimate.
```

```
You are the counter-signal critic. Given trend "{TREND}" and the prior bullish report,
search for: (a) declining adjacent metrics, (b) regulatory threats,
(c) prior cycle failures with same shape, (d) incumbent moats that prevent entry.
Return 3-7 bullets, each with a source URL.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytrends` | Unofficial Google Trends API (interest-over-time, related queries, geo) | `pip install pytrends` |
| `gtrends-cli` | CLI wrapper over pytrends, pipe-friendly CSV out | `pip install gtrends-cli` |
| `gh search repos --sort=stars` | GitHub trending / star-velocity proxy | `gh` CLI |
| `crunchbase-cli` (community) | Funding round queries; needs CB API key | github.com/crunchbase community wrappers |
| `producthunt-graphql` (curl + token) | Daily/weekly top, category filter | api.producthunt.com/v2/api/graphql |
| `hn-search` (Algolia) | HN front-page + comments search, no key needed | hn.algolia.com/api |
| `arxiv` | Paper metadata, category counts as research-momentum proxy | `pip install arxiv` |
| `searxng` (self-hosted) | Federated web search without rate limits, ideal for agent loops | docs.searxng.org |
| `linkedin-jobs-scraper` | Job-posting volume by skill keyword | `pip install linkedin-jobs-scraper` |
| `glasp` / `readwise reader` API | Saved-article corpus → trend topic clustering | readwise.io/reader_api |
| `WebSearch` / `WebFetch` (Claude Code) | Native agent web access, default for ad-hoc queries | Claude Code built-in |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Google Trends | Free | Yes via pytrends | Daily quota, smoothing on low-volume terms |
| Exploding Topics | Paid SaaS | API on Pro plan | Curated trend list, good seed source |
| Glimpse | Paid SaaS / extension | Limited API | Augments Google Trends with absolute volume |
| Crunchbase | Paid API | Yes | Funding/investor signal, $$ tier |
| PitchBook | Enterprise | Yes (expensive) | Better than CB for late-stage / private |
| CB Insights | Enterprise | Reports only | Trend reports, not real-time agent diet |
| Product Hunt | Free GraphQL | Yes | Daily top, category, maker info |
| Hacker News (Algolia) | Free | Yes, no key | Best free signal for dev-tool trends |
| GitHub Trending | Free (scrape) | Yes | Repo star velocity = adoption proxy |
| LinkedIn Jobs / Talent Insights | Paid | Scraper-only for free tier | Hiring volume = strongest lagging-validation signal |
| Indeed Hiring Lab | Free reports | RSS only | Macro labor trends |
| Statista | Paid | API on enterprise | Pre-formatted market-size charts |
| Similarweb | Paid | Yes | Web-traffic momentum for incumbents |
| BuiltWith | Paid | Yes | Tech-stack adoption curves |
| Reddit (PRAW) | Free API | Yes | Subreddit subscriber growth, post velocity |
| TikTok Creative Center | Free | Limited API | Consumer/creator trend signal |
| Gartner / Forrester | Paid | PDF only | Slow but authoritative for B2B |
| Perplexity API | Paid | Yes | Cited web answers, good for evidence rows |
| Linkup / Tavily / Exa | Paid (LLM-search) | Yes | Agent-grade web search with citations |

## Templates & scripts
See `templates.md` for full Trend Report and Monthly Dashboard. Inline collector skeleton:

```python
# trend_signals.py — minimal multi-source collector, ~40 lines
import json, datetime as dt
from pytrends.request import TrendReq
import requests

def google_trends(term: str) -> dict:
    p = TrendReq(); p.build_payload([term], timeframe="today 12-m")
    df = p.interest_over_time()
    if df.empty: return {"yoy": None, "source": "google_trends"}
    last, first = df[term].iloc[-1], df[term].iloc[0]
    yoy = None if first == 0 else round((last - first) / first * 100, 1)
    return {"yoy_pct": yoy, "last": int(last), "source": "google_trends"}

def hn_hits(term: str) -> dict:
    r = requests.get("https://hn.algolia.com/api/v1/search",
                     params={"query": term, "tags": "story",
                             "numericFilters": f"created_at_i>{int(dt.datetime.now().timestamp())-2592000}"}).json()
    return {"hits_30d": r.get("nbHits", 0), "source": "hacker_news"}

def gh_repos(term: str) -> dict:
    r = requests.get("https://api.github.com/search/repositories",
                     params={"q": f"{term} created:>{(dt.date.today()-dt.timedelta(days=180))}",
                             "sort": "stars", "order": "desc"}).json()
    return {"new_repos_180d": r.get("total_count", 0),
            "top_stars": (r.get("items") or [{}])[0].get("stargazers_count", 0),
            "source": "github"}

def collect(term: str) -> dict:
    return {"term": term, "ts": dt.datetime.utcnow().isoformat(),
            "signals": [google_trends(term), hn_hits(term), gh_repos(term)]}

if __name__ == "__main__":
    import sys; print(json.dumps(collect(sys.argv[1]), indent=2))
```

## Best practices
- **Anchor every number to a URL.** Reject unsourced rows from agent output — this kills the #1 hallucination class.
- **Score deltas, not absolutes.** Last-month vs this-month change in HN hits / star velocity beats raw counts.
- **Run monthly, not on demand.** Trend strength is read from the slope across runs — first run alone is near-useless.
- **Pair with a counter-signal critic.** A bullish-only pipeline will recommend "pursue" on every trend. The critic prompt is non-negotiable.
- **Keep a kill-list memory.** Trends marked "skip" with reason persist across sessions, so the orchestrator does not re-recommend them.
- **Personal-fit filter before scoring, not after.** Filtering 100 trends to 10 by fit, then scoring, beats scoring 100 and rejecting on fit at the end.
- **Two-week sanity gap.** Never act on a trend the same session it was discovered — log it, re-evaluate next dashboard run.
- **Collapse near-duplicate terms.** "AI agent", "agentic AI", "AI agents" point at the same trend — synonym-merge before scoring.

## AI-agent gotchas
- **Numeric hallucination.** LLMs invent CAGRs, funding totals, and "+312% YoY" with full confidence. Force JSON schema with `source_url` required; reject rows without it.
- **Stale training data masquerading as live.** Without web tools, an agent will report 2023 funding rounds as current. Always wire WebSearch/WebFetch and check `current_date` against returned URLs.
- **Source bias amplification.** Letting the agent pick its own sources collapses to "search Google → cite first SEO-spam page". Pin the allow-list of sources in the system prompt.
- **STEEP padding.** Agents fill all five STEEP cells even when Environmental is irrelevant — accept "n/a" as a valid output, otherwise the framework over-weights noise.
- **Recommendation drift toward "pursue".** Default LLM tone is helpful/optimistic; the critic agent and a forced "skip" budget (e.g., reject ≥40% of trends per run) counteract this.
- **Subreddit/HN sample-of-one.** A single viral thread spikes the count; require ≥3 independent sources before stage-promoting a trend.
- **Token blowup on raw source dumps.** Never paste full HTML/JSON into the synthesizer — collectors must return ≤20-row distilled records.
- **Date-window mismatch.** One source returns 30-day, another YoY, another all-time. Normalize windows in the collector layer or comparisons are meaningless.
- **Crunchbase/PitchBook gating.** Agents silently degrade to "unknown" when API keys are missing; surface a hard error so the user notices the blind spot.

## References
- https://trends.google.com/trends/ — official UI, baseline source.
- https://github.com/GeneralMills/pytrends — pytrends library.
- https://www.producthunt.com/api — Product Hunt GraphQL docs.
- https://hn.algolia.com/api — free Hacker News search API.
- https://docs.github.com/en/rest/search — GitHub repo/code search.
- https://explodingtopics.com/ — curated emerging topics list.
- https://www.cbinsights.com/research/ — quarterly trend reports.
- https://a16z.com/big-ideas/ — annual VC thesis dump, lagging but high-signal.
- https://www.gartner.com/en/research/methodologies/gartner-hype-cycle — Hype Cycle reference.
- https://www.crunchbase.com/api — funding-data API docs.
- https://docs.tavily.com/ — agent-grade web search with citations.
- https://docs.perplexity.ai/ — cited-answers API for evidence rows.
