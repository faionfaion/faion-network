# Agent Integration — Product Development Trends 2026

## When to use
- Quarterly trend refresh that feeds product roadmap, GTM positioning, or pricing decisions for a B2B/B2C software product.
- Pre-PRD discovery: surface AI-augmented ideation candidates and weak signals before locking spec into `faion-feature-executor`.
- Investor / board update where you must justify direction shifts ("why pivot now?") with cited macro and consumer trends.
- Competitive briefs where a methodology refresh is needed (e.g. agile→continuous discovery, waterfall→dual-track).
- Research mode `ideas` or `market` inside `faion-research-agent` when the requesting team explicitly wants a trends overlay.

## When NOT to use
- Pure tactical execution (sprint planning, story splitting) — use `pm-agile` or `sdd-planning` instead.
- Single-feature validation where one customer interview answers the question — use `user-researcher/problem-validation`.
- Pricing tear-down or TAM/SAM/SOM math — defer to `market-researcher/pricing-research` and `market-researcher/tam-sam-som`.
- Engineering practice changes (CI, testing) — use `cicd-engineer` and `code-quality` skills.
- When less than 6 weeks since the last trends pass and no triggering event (funding round, major competitor move, regulatory shift).

## Where it fails / limitations
- Trend reports decay fast: anything older than 90 days is suspect for "consumer behavior" claims; LLM training data is structurally behind real markets.
- Survivorship bias in trend articles — "AI-augmented ideation" gets cited because it's loud, not because it ships outcomes; demand a concrete shipped-vs-killed ratio.
- Confounds correlation with causation (cross-functional teams "cause" speed). Without a control case, treat as hypothesis, not finding.
- LLMs hallucinate vendor capabilities and pricing. Every tool/SaaS claim must be re-verified with WebFetch on the vendor's own page before publishing.
- "Days, not weeks" turnaround is aspirational for regulated domains (fintech, health, gov) — call out where the trend does not apply.

## Agentic workflow
Drive trend research as a three-stage pipeline: (1) signal collection by a `sonnet`-class subagent doing wide WebSearch + WebFetch; (2) signal triage and synthesis by an `opus`-class subagent that scores each signal on `recency × evidence × applicability`; (3) human checkpoint to accept/reject claims before they are written into `.aidocs/product_docs/trend-report.md`. Inside this repo, route via `faion-research-agent` (mode `ideas` or `market`) and let it spawn the per-signal sub-tasks. Persist the raw signal log under `.aidocs/research/raw/` so subsequent quarters can diff against it instead of re-scraping.

### Recommended subagents
- `faion-research-agent` — orchestrator; switch to mode `ideas` for ideation trends, `market` for adoption/competitive trends, `pricing` for monetization trends.
- `faion-domain-checker-agent` — when trends spawn product-naming candidates, verify availability before they leak into a deck.
- `faion-sdd-executor-agent` — only after the trend report is ratified; converts accepted trend implications into `backlog/` features.
- `password-scrubber-agent` — run before publishing if WebFetch surfaced API keys or session tokens in raw signal dumps.

### Prompt pattern
```
You are operating in mode=market for faion-research-agent.
Goal: produce a 2026 product-development-trends brief for <product>.
Constraints: cite each claim with a URL no older than 90 days; flag any claim
without a primary source; output to .aidocs/product_docs/trend-report.md
following the templates.md skeleton.
```
```
For each signal in raw/signals.jsonl, score recency (0-3), evidence (0-3),
applicability to <product> (0-3). Drop any with total < 5. Return a markdown
table sorted by total desc; do not invent signals not present in the input.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Mine release notes, issue trends, "awesome-X" curation | https://cli.github.com |
| `crwl` / `crawl4ai` | LLM-friendly site-to-markdown for trend article ingestion | `pip install crawl4ai` |
| `trafilatura` | Article extraction at scale, preserves dates and authors | `pip install trafilatura` |
| `pytrends` | Unofficial Google Trends API, validates "rising" claims with search volume | `pip install pytrends` |
| `pandoc` | Convert PDF analyst reports to markdown for LLM ingestion | `apt install pandoc` |
| `glow` / `mdcat` | Render finished trend report locally before publishing | https://github.com/charmbracelet/glow |
| `jq` | Slice signal JSONL piles fed to the synthesis agent | https://jqlang.github.io |
| `ddgr` | Anonymous DuckDuckGo search to cross-check WebSearch results | `apt install ddgr` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Exploding Topics | SaaS | Limited (HTML, no public API) | Best for emerging consumer trends; scrape with `crawl4ai`, respect ToS |
| Glimpse (Trends API) | SaaS | Yes (REST API) | Paid Google Trends superset with API; good for `applicability` scoring |
| CB Insights | SaaS | Partial (API is enterprise-tier) | Authoritative for VC/M&A signals; usually behind paywall |
| Crunchbase API | SaaS | Yes | Funding rounds as a leading indicator of category heat |
| ProductHunt GraphQL | SaaS (OSS client) | Yes | "What shipped this week" is a cheap weak-signal feed |
| Hacker News Algolia API | OSS | Yes | Free-tier sentiment proxy; query by domain or keyword |
| Reddit API | SaaS | Yes (with auth) | Subreddit drift is a strong consumer-trend signal |
| Gartner / Forrester | SaaS | No | Auth-walled PDFs; convert with pandoc once acquired by humans |
| Statista | SaaS | Partial | Charts are PNG; agents should request CSV exports manually |
| Mixpanel / Amplitude | SaaS | Yes (REST) | Internal product trends — anchor external claims to your own data |

## Templates & scripts
The methodology's `templates.md` is currently empty. Inline starter for a signal-scoring pass that plugs into the synthesis stage:

```python
#!/usr/bin/env python3
"""Score trend signals on recency/evidence/applicability, drop weak ones."""
import json, sys, datetime as dt

THRESHOLD = 5
TODAY = dt.date.today()

def score(sig: dict) -> dict:
    age_days = (TODAY - dt.date.fromisoformat(sig["published"])).days
    recency = 3 if age_days <= 30 else 2 if age_days <= 90 else 1 if age_days <= 180 else 0
    evidence = 3 if sig.get("primary_source") else 2 if sig.get("citations", 0) >= 3 else 1
    applicability = int(sig.get("applicability", 0))
    sig["score"] = recency + evidence + applicability
    sig["recency"], sig["evidence_score"] = recency, evidence
    return sig

def main(path: str) -> None:
    rows = [score(json.loads(l)) for l in open(path) if l.strip()]
    kept = [r for r in rows if r["score"] >= THRESHOLD]
    kept.sort(key=lambda r: r["score"], reverse=True)
    print(f"# Trend signals (kept {len(kept)}/{len(rows)})\n")
    print("| Score | Trend | Source | Date |")
    print("|-------|-------|--------|------|")
    for r in kept:
        print(f"| {r['score']} | {r['trend']} | {r['source']} | {r['published']} |")

if __name__ == "__main__":
    main(sys.argv[1])
```

Feed it JSONL where each line is `{"trend": "...", "source": "URL", "published": "YYYY-MM-DD", "primary_source": bool, "citations": int, "applicability": 0-3}`. Pipe the markdown table directly into the trend report.

## Best practices
- Anchor every macro trend to one internal data point from your own product analytics; if you cannot, downgrade the trend to "watch list" not "act".
- Force a "kill list": for every trend you adopt, name one current practice you stop. Trend reports without subtractions are theatre.
- Separate "consumer trends" (slow, demographic) from "platform trends" (fast, technology). Mixing them in one bucket is the most common failure mode.
- Date-stamp every claim at the bullet level, not just the document. Future agents diff bullet-dates to detect staleness.
- Keep a `signals.jsonl` audit trail. The diff between this quarter's and last quarter's file is more useful than the polished narrative.
- For AI-augmented ideation specifically: log the human override rate. If humans accept >90% of LLM-surfaced ideas, the LLM is not ideating — it is rubber-stamping. If <10%, the prompt is broken.
- Cap each trend at 3 sentences in the executive summary. Long entries always indicate weak evidence padding.

## AI-agent gotchas
- LLMs over-index on US/SF Bay Area sources. Force at least one EU and one APAC primary source per trend or the brief is regionally biased.
- WebSearch results are ranked by SEO, not freshness — always sort by `published` date in your scraper before summarizing.
- "Rapid pivots, quarterly cycles" is a popular LLM completion regardless of evidence. Treat any unsourced cadence claim as hallucinated.
- Cross-functional team claims usually cite the same 2–3 secondary sources (HBR, McKinsey blog). Do not let three citations to the same article inflate confidence.
- Human-in-the-loop checkpoint **before** writing into `.aidocs/product_docs/`: a human must accept the final scored signal table. Without this gate, hallucinated tool/vendor names land in deliverables.
- When the methodology spawns SDD features, route them through `faion-sdd-executor-agent` with explicit acceptance criteria — "act on trend X" is not a feature.
- Token cost: synthesis stage on `opus` with 50+ signals can blow past 100k tokens. Pre-filter with the script above before paying for synthesis.

## References
- Lenny's Newsletter — Continuous discovery and trend cadence essays (https://www.lennysnewsletter.com/)
- Teresa Torres, *Continuous Discovery Habits* (Product Talk, 2021) — the discipline behind "rapid pivots, quarterly cycles"
- Marty Cagan, *Transformed* (SVPG, 2024) — cross-functional product team mechanics, with failure cases
- ProductHunt + Hacker News weekly digests — cheap feeds for early-signal triangulation
- Gartner Hype Cycles (annual) — taxonomy reference even if individual placements are debatable
- Faion knowledge: `pro/research/researcher/CLAUDE.md`, `pro/research/market-researcher/`, `solo/product/product-planning/`
