# Agent Integration — Pain Point Research

## When to use
- Pre-MVP: you have a target audience but no validated problem yet.
- Picking between 3-5 ideas — score the underlying pain points and let the matrix break ties.
- Exploring an unfamiliar niche where your domain intuition is weak.
- Repurposing existing research output (G2 reviews, App Store reviews, Reddit threads) into a structured backlog of opportunities.

## When NOT to use
- You already have paying users — go to user interviews / cancellation post-mortems instead. Pain points from strangers add noise.
- Highly regulated domains (healthcare, finance) where complaints are tightly NDA'd and Reddit/Quora signal is misleading.
- B2B enterprise where buyers don't post complaints publicly — switch to expert calls / analyst reports.
- When you need quantitative effect sizes — pain-point mining gives qualitative signal only.

## Where it fails / limitations
- Survivorship and outrage bias: 1-star reviews skew loud edge cases, missing the "fine but mediocre" majority where most opportunity lives.
- Score weights (Frequency 30% / Severity 25% / Reach 20% / Spend 15% / Alternatives 10%) are heuristic; agents quote them as if they were calibrated, which they aren't.
- Reddit/Twitter scraping is increasingly rate-limited and ToS-restricted; agent pipelines that hit the API directly break or violate terms.
- Without demographic context, "Reach 5 = everyone" inflates score for niche pain. Always anchor reach in the defined audience scope, not the internet.
- LLMs hallucinate plausible-sounding quotes — every quote in the log MUST link back to an actual URL or it's worthless for follow-up validation.

## Agentic workflow
Run as a 3-stage pipeline. Stage 1 (haiku): mine sources in parallel — one agent per Tier source (Reddit, G2, App Store, Quora, Upwork). Each returns a JSON list of `{quote, url, source, raw_category_guess}`. Stage 2 (sonnet): a single dedupe + categorize agent merges, removes near-duplicates, assigns one of the 8 categories, and applies the scoring rubric. Stage 3 (opus): an opportunity-extraction agent reads the top-N scored points, runs 5-Whys, and proposes business angles. Human reviews stage-2 categories and stage-3 angles before any further work.

### Recommended subagents
- `faion-pain-point-researcher-agent` — the canonical agent referenced by the README; orchestrates source mining and scoring.
- A custom `reddit-miner` (haiku) — strict JSON output, one Reddit thread → list of pain quotes with permalinks.
- A custom `pain-categorizer` (sonnet) — applies the 8-category taxonomy and detects miscategorization.
- A custom `pain-deduplicator` (haiku) — collapses near-duplicate quotes by embedding similarity.
- `faion-brainstorm` — turn the top-5 scored pain points into solution candidates (diverge/converge).

### Prompt pattern
```
Read skills/faion/knowledge/solo/research/researcher/pain-point-research/README.md.
Mine pain points for audience=<X>, context=<Y>, sources=[reddit:<sub>, g2:<product>, quora].
Return JSON list of {quote, url, source, category, freq:1-5, sev:1-5, reach:1-5, spend:1-5, alt:1-5}.
Do not invent quotes — every entry must have a working URL.
```

```
Take the JSON list. Dedupe by paraphrase. Compute score = freq*0.3 + sev*0.25 + reach*0.2 +
spend*0.15 + alt*0.1. Output top 10 sorted, each with a 5-Whys chain.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `praw` (Reddit API) | Authenticated Reddit scraping | https://praw.readthedocs.io |
| `pushshift` mirrors | Historical Reddit search | https://github.com/Watchful1/PushshiftDumps (post-API-shutdown) |
| `apify` CLI | Pre-built scrapers (G2, App Store, Trustpilot) | https://docs.apify.com/cli |
| `serpapi` | Programmatic Google "People Also Ask" | https://serpapi.com/people-also-ask |
| `notion-cli` / `airtable-cli` | Persist scored pain points | https://airtable.com/developers/web/api/introduction |
| `yt-dlp` + transcript | Mine YouTube comment rants | https://github.com/yt-dlp/yt-dlp |
| Anthropic SDK / OpenAI SDK | Categorize and score in batches | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reddit API | SaaS | Partial | Rate-limited, paid for high volume; respect ToS. |
| Apify | SaaS | Yes | Hosted scrapers for G2, Capterra, Trustpilot, App Store; agent-callable via REST. |
| Bright Data / ScrapingBee | SaaS | Yes | Proxy + scrape for sites with anti-bot. |
| Sprig / Maze | SaaS | Partial | For follow-up validation interviews, not initial mining. |
| GummySearch / F5Bot | SaaS | Yes | Reddit-specialized listening; webhook-friendly. |
| Algolia App Search of forums | SaaS | Yes | When the niche has a self-hosted Discourse forum. |
| Notion / Airtable | SaaS | Yes | Long-term log; agent-writable via API. |

## Templates & scripts
See `templates.md` and the README's "Pain Point Research Log" + "Reddit Mining Template". Inline batch scorer (Python, ≤30 lines) — feed JSON list, get scored CSV:

```python
import json, csv, sys
W = {"freq":0.30, "sev":0.25, "reach":0.20, "spend":0.15, "alt":0.10}
items = json.load(sys.stdin)
out = csv.writer(sys.stdout)
out.writerow(["id","category","quote","url","score"])
for i, it in enumerate(items, 1):
    s = sum(W[k] * float(it.get(k, 0)) for k in W)
    out.writerow([f"PP-{i:03}", it.get("category",""), it.get("quote","")[:200],
                  it.get("url",""), round(s, 2)])
```

Pipe `pain_points.json | python3 score.py > pain_points.csv` and sort.

## Best practices
- Define audience + context BEFORE searching. "Founders" is too broad; "Solo founders, US, post-launch B2B SaaS, <$10k MRR" is searchable.
- Capture the verbatim quote and URL — never the agent's paraphrase. Paraphrases lose signal and can't be re-validated.
- Use ≥3 source tiers. Reddit alone is biased toward complainers; mix with Quora questions and Upwork gigs to triangulate.
- Score in a single sitting with a single agent — splitting scoring across calls drifts on the rubric.
- Re-run quarterly for the same audience; pain-point landscape shifts (LLMs killed many "I spent 2 hours on X" complaints in 2024).
- Always extract root cause via 5-Whys for the top 3. The first-order pain is rarely the right thing to build.
- Pair with `problem-validation` and `jobs-to-be-done` — a high-score pain that fails JTBD-fit is a feature, not a product.

## AI-agent gotchas
- LLMs invent plausible Reddit quotes when given a topic without raw text input. Always pass scraped text into context, not just a topic; require URLs.
- Categorization drifts mid-batch (the model "decides" Time-Waste means something different by item 40). Use one explicit category list in every system prompt.
- Models inflate Reach scores ("everyone has this") because complaints are loud. Cap Reach at 4 unless ≥3 distinct sources mention it.
- Cross-language pain points: a UA-language Reddit thread is invisible to most agents. Use a translator agent in stage 1 explicitly.
- Human checkpoint: opportunities from stage 3 should be reviewed before any go-to-market work — opus output is plausible but unvalidated; treat as hypotheses.
- Don't let the agent "summarize" — keep raw quotes in the log. Summaries lose the verbatim signal needed for downstream JTBD interviews.
- Never let the same agent both score AND extract opportunities; opportunity-pull biases scoring.

## References
- https://www.cbinsights.com/research/startup-failure-reasons-top/
- https://www.indiehackers.com/post/how-to-find-startup-ideas-by-mining-pain-points
- https://stratechery.com/2017/jobs-to-be-done-and-painted-doors/ (related framing)
- https://www.lennysnewsletter.com/p/how-to-find-the-right-customer-problem
- https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
