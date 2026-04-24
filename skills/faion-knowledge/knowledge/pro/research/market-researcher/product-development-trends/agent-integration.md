# Agent Integration — Product Development Trends (market-researcher)

## When to use
- Quarterly market-trend refresh that feeds GTM positioning, pricing tier design, or category framing for a B2B/B2C product.
- Pre-investment decision: a category looks "hot" and the market team must separate hype from durable adoption before budget is committed.
- When competitive intel uncovers a methodology shift in the market (waterfall → continuous discovery, hand-coded → AI-augmented) and you need to decide whether to follow, ignore, or counter-position.
- Annual / semi-annual board memo where the market lens (not the product lens) is the deliverable: TAM expansion, sub-segment emergence, pricing-power shifts.
- Inside `faion-research-agent` mode `market` or `ideas` when the requesting team explicitly asks for a "what's changing in this space" overlay, not a feature-level discovery.

## When NOT to use
- Product roadmap or sprint planning — defer to `pro/research/researcher/product-development-trends` (same name, product-side framing) or to `pm-agile`.
- Pure pricing benchmark — use `market-researcher/pricing-research` and `market-research-tam-sam-som`.
- Single-feature validation — use `user-researcher/problem-validation` or `continuous-discovery`.
- Competitive tear-down of one named rival — use `market-researcher/competitor-analysis` and `competitive-intelligence`.
- Less than 90 days since the last trends pass and no triggering event (funding round, regulatory shift, major launch). Trend churn faster than that is noise.

## Where it fails / limitations
- "Trend" articles are written for SEO, not signal. Survivorship bias dominates; "AI-augmented ideation" gets cited because it's loud, not because adoption shipped business outcomes.
- LLM training data lags real markets by 6–18 months. Anything in the README dated 2025/2026 must be re-verified before it lands in a deliverable.
- Conflates correlation with causation ("cross-functional teams cause speed"). Without a counterfactual, treat as hypothesis.
- US/SF Bay Area over-representation. Without forced EU/APAC sources, the brief misreads regulated markets (DE, JP, BR) where "days, not weeks" is illegal in regulated workflows.
- "Eco-friendly / brands that do good" is a ten-year-old trend recycled — agents will happily restate it. Demand a 2025-or-later primary source per consumer-trend bullet or drop it.
- Vendor/tool capability claims hallucinate at high rates; every named SaaS line below must be re-verified with `WebFetch` on the vendor's own pricing page before publishing.

## Agentic workflow
Run as a three-stage pipeline behind `faion-research-agent` (mode `market` for adoption/positioning trends, `ideas` for emerging-category trends): (1) wide signal collection — a `sonnet` subagent does WebSearch + WebFetch and dumps to `.aidocs/research/raw/signals.jsonl`; (2) synthesis — an `opus` subagent scores each signal on `recency × evidence × applicability` and proposes a market implication; (3) human checkpoint — accept/reject before the synthesis is written into `.aidocs/product_docs/market-research.md` or a dedicated `trend-report.md`. Persist the raw signal log so next quarter's run diffs against it instead of re-scraping. Keep this methodology distinct from the product-side sibling at `researcher/product-development-trends` by writing market implications (TAM, pricing, positioning) and explicitly linking — not duplicating — the product implications.

### Recommended subagents
- `faion-research-agent` — orchestrator; mode `market` for adoption/positioning, `ideas` for emerging-category, `pricing` when trend implies a tier-design shift.
- `faion-domain-checker-agent` — when emerging categories surface naming candidates for a new product line, verify availability before they land in a deck.
- `faion-sdd-executor-agent` — only after the trend memo is ratified; converts accepted GTM/positioning implications into `backlog/` features (e.g. landing page rewrite, pricing tier change).
- `password-scrubber-agent` — run before publishing if WebFetch surfaced API keys or session tokens in raw signal dumps.

### Prompt pattern
```
You are operating in mode=market for faion-research-agent.
Goal: produce a 2026 market-side product-development-trends brief for <product/category>.
Constraints: cite each claim with a primary URL no older than 90 days; flag any
claim without a primary source; force at least one EU and one APAC source;
output to .aidocs/product_docs/trend-report.md following templates.md.
For each trend, write the MARKET implication (TAM shift, pricing power,
positioning) — do NOT restate product/roadmap implications (those live in
researcher/product-development-trends).
```
```
For each signal in raw/signals.jsonl, score recency (0-3), evidence (0-3),
applicability to <category> (0-3). Drop any with total < 5. Return a markdown
table sorted by total desc; do not invent signals not present in the input.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Mine release notes / "awesome-X" curation as adoption proxy | https://cli.github.com |
| `crawl4ai` | LLM-friendly site-to-markdown for trend articles and analyst posts | `pip install crawl4ai` |
| `trafilatura` | Article extraction at scale; preserves dates and authors | `pip install trafilatura` |
| `pytrends` | Unofficial Google Trends API; validates "rising" claims with search volume | `pip install pytrends` |
| `pandoc` | Convert PDF analyst reports (Gartner / Forrester) to markdown for LLM ingestion | `apt install pandoc` |
| `jq` | Slice signal JSONL piles fed to the synthesis stage | https://jqlang.github.io |
| `ddgr` | Anonymous DuckDuckGo search to cross-check WebSearch results and reduce SEO bias | `apt install ddgr` |
| `glow` / `mdcat` | Render the finished trend report in terminal before publishing | https://github.com/charmbracelet/glow |
| `lynx -dump` | Fast text fetch for paywalled-but-text-leaky pages | `apt install lynx` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Exploding Topics | SaaS | Limited (HTML, no public API) | Strong for emerging consumer trends; scrape with `crawl4ai`, respect ToS |
| Glimpse Trends API | SaaS | Yes (REST API) | Paid Google Trends superset; useful for `applicability` scoring |
| Crunchbase API | SaaS | Yes | Funding rounds = leading indicator of category heat and TAM expansion |
| CB Insights | SaaS | Partial (API enterprise-tier) | Authoritative for VC/M&A signals; usually paywalled |
| ProductHunt GraphQL | SaaS (OSS client) | Yes | Weekly "what shipped" feed; cheap weak-signal source |
| Hacker News Algolia API | OSS | Yes | Free sentiment proxy; query by domain, keyword, or competitor name |
| Reddit API | SaaS | Yes (with auth) | Subreddit drift is a strong consumer-side trend signal |
| G2 / Capterra | SaaS | Limited (HTML) | Review-volume deltas indicate adoption shifts in B2B categories |
| SimilarWeb | SaaS | Yes (paid API) | Traffic-share trend per category; useful for GTM positioning |
| Statista | SaaS | Partial | Charts are PNG; agents should request CSV exports manually |
| Gartner / Forrester | SaaS | No | Auth-walled PDFs; convert with `pandoc` after a human acquires them |

## Templates & scripts
This methodology's `templates.md`, `examples.md`, `checklist.md`, and `llm-prompts.md` are currently empty. Inline starter that scores raw signals before paying for `opus` synthesis:

```python
#!/usr/bin/env python3
"""Score market-trend signals on recency/evidence/applicability; drop weak ones."""
import json, sys, datetime as dt

THRESHOLD = 5
TODAY = dt.date.today()

def score(sig: dict) -> dict:
    age_days = (TODAY - dt.date.fromisoformat(sig["published"])).days
    recency = 3 if age_days <= 30 else 2 if age_days <= 90 else 1 if age_days <= 180 else 0
    evidence = 3 if sig.get("primary_source") else 2 if sig.get("citations", 0) >= 3 else 1
    applicability = int(sig.get("applicability", 0))
    sig["score"] = recency + evidence + applicability
    return sig

def main(path: str) -> None:
    rows = [score(json.loads(l)) for l in open(path) if l.strip()]
    kept = sorted([r for r in rows if r["score"] >= THRESHOLD],
                  key=lambda r: r["score"], reverse=True)
    print(f"# Trend signals (kept {len(kept)}/{len(rows)})\n")
    print("| Score | Trend | Region | Source | Date | Market implication |")
    print("|-------|-------|--------|--------|------|--------------------|")
    for r in kept:
        print(f"| {r['score']} | {r['trend']} | {r.get('region','?')} | "
              f"{r['source']} | {r['published']} | {r.get('market_impl','')} |")

if __name__ == "__main__":
    main(sys.argv[1])
```

JSONL row shape: `{"trend": "...", "source": "URL", "published": "YYYY-MM-DD", "primary_source": bool, "citations": int, "applicability": 0-3, "region": "US|EU|APAC|...", "market_impl": "..."}`. Pipe the markdown table directly into the trend memo.

## Best practices
- Anchor every macro trend to one quantifiable market datapoint — funding round, traffic-share delta, review-count trajectory. If you cannot, label the trend "watch" not "act".
- Force a "kill list": for every adopted trend, name one current GTM/pricing assumption you stop. Trend memos without subtractions are theatre.
- Separate "consumer trends" (slow, demographic) from "platform trends" (fast, technology) into two tables. Mixing them is the most common failure mode in this methodology.
- Date-stamp at the bullet level, not just the document. Future agents diff bullet-dates to detect staleness without re-reading.
- Keep `signals.jsonl` as an audit trail. The diff between this quarter's and last quarter's file is more useful than the polished narrative.
- Cap each trend at 3 sentences in the executive summary. Long entries always indicate weak evidence padded with adjectives.
- Cross-link the product-side sibling: `researcher/product-development-trends` should reference the same signal log. If both methodologies are run, run them on the same `signals.jsonl` and write distinct implication sections.
- For the "AI-augmented ideation" claim specifically: log the human override rate when the trend is acted on. >90% acceptance ⇒ rubber-stamping; <10% ⇒ broken prompt.

## AI-agent gotchas
- LLMs over-index on US/SF sources. Force at least one EU and one APAC primary source per trend or the brief is regionally biased toward the wrong market.
- WebSearch is ranked by SEO, not freshness — sort by `published` date in the scraper before summarizing.
- "Rapid pivots, quarterly cycles" is a default LLM completion regardless of evidence. Treat any unsourced cadence claim as hallucinated.
- Cross-functional team claims usually cite the same 2–3 secondary sources (HBR, McKinsey blog). Three citations to the same article must not inflate confidence.
- Human-in-the-loop checkpoint **before** writing into `.aidocs/product_docs/`: a human accepts the final scored signal table. Without this gate, hallucinated tool/vendor names land in deliverables.
- When the methodology spawns SDD features, route them through `faion-sdd-executor-agent` with explicit acceptance criteria; "act on trend X" is not a feature.
- Token cost: synthesis on `opus` with 50+ raw signals can blow past 100k tokens. Pre-filter with the script above before paying for synthesis.
- Duplicate-content trap: this methodology shares its `README.md` with `researcher/product-development-trends`. Agents must explicitly ask "is the deliverable a market memo or a product memo?" — otherwise both flows produce the same file and one is silently overwritten.

## References
- Teresa Torres, *Continuous Discovery Habits* (Product Talk, 2021) — discipline behind "rapid pivots, quarterly cycles"
- Marty Cagan, *Transformed* (SVPG, 2024) — cross-functional team mechanics with documented failure cases
- Lenny's Newsletter — continuous discovery and trend cadence essays (https://www.lennysnewsletter.com/)
- Gartner Hype Cycles (annual) — taxonomy reference even when individual placements are debatable
- ProductHunt + Hacker News weekly digests — cheap feeds for early-signal triangulation
- Crunchbase / CB Insights funding-round tables — leading indicator of category heat
- Faion knowledge: `pro/research/market-researcher/CLAUDE.md`, `pro/research/researcher/product-development-trends/agent-integration.md` (product-side sibling), `pro/research/market-researcher/trend-analysis/`, `solo/product/product-planning/`
