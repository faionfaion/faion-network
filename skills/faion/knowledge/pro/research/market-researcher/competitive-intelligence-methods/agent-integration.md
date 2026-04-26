# Agent Integration — Competitive Intelligence Methods

This bundle covers two sub-methodologies that ship together:
- **competitor-analysis** — landscape mapping (direct / indirect / substitute / potential), 2x2 positioning matrix, whitespace.
- **competitive-intelligence** — feature inventory, feature matrix, gap identification, gap validation.

Treat them as a single agent pipeline: landscape first, then per-cell feature drill-down.

## When to use
- Pre-MVP wedge selection: you have a candidate niche and need the 2x2 + gap list before the spec is written.
- Quarterly competitive review: deltas in funding, pricing, positioning, hiring across the top 15-20 competitors.
- New-feature go/no-go: deciding whether feature X is table-stakes, opportunity, or moat-building based on a feature matrix across top 5.
- Pricing repositioning: anchoring our price tier on a fresh per-competitor pricing scrape.
- Pitch deck / investor update: defensible "competitive landscape" slide with sourced rows.
- Reverse-engineering an incumbent before a head-on launch (their changelog, hiring, support footprint).

## When NOT to use
- Sub-week tactical decisions (single ad copy, single landing-page test) — the matrices are too coarse.
- True greenfield categories with <3 competitors — the feature matrix collapses to a 1-column table; use jobs-to-be-done instead.
- Highly-regulated B2B (defense, banking core) where competitor data is private and any public pull is misleading.
- Late-stage scaling where customer-success and retention data dominate; a feature matrix here just produces feature-bloat backlog.
- After product-market fit: optimizing on the feature matrix is how startups become "Salesforce-but-cheaper" forever.

## Where it fails / limitations
- **Direct-only blindness.** Teams default to the 3-5 obvious head-on competitors and miss substitutes (spreadsheets, email, "do nothing") which are the actual churn cause.
- **Static snapshots.** A one-time matrix decays in 3-6 months; without a re-run cadence the decisions made off it become stale anchors.
- **Feature-checkbox theater.** "Has Y/Partial/No" hides quality differences (their search is checkbox-Yes but unusable; ours is Yes and great). Force a 0-3 quality column or N-day-old screenshot link per cell.
- **Whitespace fallacy.** An empty 2x2 cell is empty for a reason 80% of the time (no demand, hard to build, regulated, unprofitable). Whitespace MUST be paired with a demand-validation step.
- **Pricing pages lie.** Listed prices ≠ negotiated prices for B2B; agent-only pulls under-report enterprise discounts and over-report SMB ACV.
- **LLM source-bias.** Agents cite the company's own marketing site as evidence of "feature: Yes" — needs cross-source rule (review site + community thread + screenshot).
- **Competitor list survivorship.** G2/Capterra rank by paid placement, not adoption. Crunchbase indexes funded only — bootstrapped competitors disappear.
- **Substitutes are unsearchable.** "Slack vs Email" rarely surfaces from a Google query; must come from user-interview transcripts.

## Agentic workflow
Run as a fan-out / fan-in pipeline keyed on the `competitors` research mode. An orchestrator (`faion-research-agent --mode=competitors`) emits a frontier list of 15-20 candidates from seed sources (G2, Capterra, Product Hunt category, Crunchbase, "{category} alternatives" SERPs, "vs {seed}" SERPs). Per-competitor collectors hydrate a structured row (founded, funding, team, pricing, positioning, top features). A separate feature-matrix agent fans out across the top-5 cell-by-cell, fills the Y/P/N grid plus a 0-3 quality score and a per-cell evidence URL. A gap-validation critic interrogates every candidate gap with three questions (intentional? wanted? buildable better?) and rejects ≥40% of them by default to counter pursuit-bias. All output goes to `.aidocs/product_docs/competitive-analysis.md` keyed by run-date so deltas stay diffable.

### Recommended subagents
- `faion-research-agent` (mode: `competitors`) — primary orchestrator; owns competitor list, 2x2 matrix, whitespace.
- `faion-market-researcher-agent` — hosts the methodology rubric and final report synthesis.
- `competitor-row-hydrator` (haiku) — cheap per-competitor pull: founded, funding, headcount, pricing, top-3 features, positioning sentence.
- `feature-matrix-filler` (sonnet) — cell-by-cell Y/P/N + 0-3 quality score with evidence_url; returns one row per feature.
- `gap-validator-critic` (sonnet) — adversarial: forced "skip" budget on any gap that fails the three-question test.
- `pricing-scraper` (haiku) — pulls pricing pages, normalizes to per-seat / per-tier / per-feature; returns JSON only.
- `review-mining-agent` (sonnet) — G2/Capterra/Reddit review scrape → top-5 complaints per competitor (input to gap validation).
- `faion-domain-checker-agent` — verifies whitespace candidate names + domains before they reach the report.

### Prompt pattern
```
You are the competitor-orchestrator. Seed: "{CATEGORY}".
Step 1: Produce 15-20 competitors covering Direct/Indirect/Substitute/Potential.
Step 2: For each, output ONLY this row:
{
  "name":"", "type":"direct|indirect|substitute|potential",
  "founded":"", "funding_usd":0, "team_size":0,
  "pricing":{"model":"", "entry_usd":0, "url":""},
  "positioning":"<=140 chars",
  "top_features":["",""],
  "evidence_urls":["","",""]
}
Rules: every numeric or claim cites a URL. Unknown -> "unknown". No marketing copy verbatim.
```

```
You are the feature-matrix-filler. Features list: {LIST}. Competitors: {LIST}.
For each (feature, competitor) cell return:
{"feature":"", "competitor":"", "status":"Y|P|N",
 "quality":0-3, "evidence_url":"", "notes":"<=80 chars"}
"Y" requires evidence_url; if no evidence, write "N" and add note "no public proof".
```

```
You are the gap-validator-critic. Candidate gap: "{GAP}".
Answer (with sources):
1. Why does no competitor have it? (technical / regulatory / unprofitable / unaware)
2. Do customers actually want it? (review quotes, forum links, search volume)
3. Can we build it materially better? (our advantage, in one sentence)
Verdict: pursue | investigate | skip. Default = skip when any answer is weak.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh search repos / users` | OSS competitor proxy: stars, forks, contributors | `gh` CLI |
| `crunchbase-cli` (community) | Funding, founders, headcount | github community wrappers, needs CB API key |
| `similarweb-cli` (community) | Traffic / engagement / referrers | needs Similarweb key |
| `builtwith-cli` (community) | Tech-stack adoption per competitor domain | needs BuiltWith key |
| `producthunt-graphql` (curl) | Category leaderboards, alternatives | api.producthunt.com/v2/api/graphql |
| `g2-scraper` / `capterra-scraper` | Review pulls — pair with rotating proxy | community libs; respect ToS |
| `trustpilot-scraper` | Review-mining for substitute/indirect | community libs |
| `praw` | Reddit subreddit + thread search | `pip install praw` |
| `playwright` / `playwright-mcp` | Screenshot pricing pages, archive into evidence/ | `npx playwright install` |
| `single-file-cli` | Save a competitor page as a single HTML for archive | `npm i -g single-file-cli` |
| `whoxy-cli` / `whois` | Founding signal, domain lineage | `apt install whois` |
| `wayback-machine-downloader` | Pricing/positioning history (delta) | `gem install wayback_machine_downloader` |
| `searxng` | Self-hosted federated search for `"{seed}" alternatives` queries | docs.searxng.org |
| `WebSearch` / `WebFetch` (Claude Code) | Built-in agent web access for ad-hoc rows | Claude Code native |
| `pandoc` + `csvkit` | Convert competitive matrix between md / csv / xlsx | `pip install csvkit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Crunchbase | SaaS | Yes (paid API) | Funding, headcount, founders. SMB blind spot. |
| PitchBook | SaaS (enterprise) | Yes ($$$) | Late-stage / private accuracy. |
| CB Insights | SaaS (enterprise) | Reports only | Quarterly state-of-X reports — slow but high-signal. |
| G2 | SaaS | Limited API; scraping risky | Review counts, category leaders, "alternatives to X". |
| Capterra | SaaS | Limited | Same as G2; SMB-skewed. |
| TrustRadius | SaaS | Reports | Mid-market depth. |
| Product Hunt | Free GraphQL | Yes | Alternatives + launch dates. |
| BuiltWith | SaaS | Yes (paid) | Tech adoption per domain — proxy for product weight. |
| Wappalyzer | Free + SaaS | Yes (CLI/extension) | Lighter alternative to BuiltWith. |
| Similarweb | SaaS | Yes (paid) | Traffic momentum, referral mix. |
| Semrush / Ahrefs | SaaS | Yes (paid) | Keyword overlap, ad spend, content gap reports. |
| Owler | SaaS | Yes (limited free) | Headcount, funding, news aggregation. |
| Apollo / ZoomInfo | SaaS | Yes (paid) | Headcount-by-department signal (eng vs sales mix). |
| LinkedIn Sales Navigator | SaaS | Scraper-only | Hiring velocity per competitor. |
| Glassdoor | SaaS | Limited | Internal sentiment / culture proxy. |
| Glimpse | SaaS / extension | Limited API | Augments Google Trends with absolute volume. |
| Klue | SaaS (CI platform) | Yes (paid) | Battlecards, win/loss — for CI teams already running this in-house. |
| Crayon | SaaS (CI platform) | Yes (paid) | Page-change tracking; great for delta runs. |
| Kompyte | SaaS | Yes (paid) | Automated competitive monitoring. |
| Visualping | SaaS | Yes (paid) | Cheap page-change pings on pricing/changelog/blog. |
| Wayback Machine (Internet Archive) | Free | Yes | Pricing/positioning lineage. Critical for delta credibility. |
| Reddit | Free API | Yes (PRAW) | Substitute discovery + complaint mining. |
| Hacker News (Algolia) | Free | Yes | Launch coverage, technical critique. |
| Perplexity / Tavily / Exa | SaaS (LLM-search) | Yes | Cited evidence rows for the matrix. |

## Templates & scripts
See `templates.md` and `examples.md` in this folder for the landscape table, feature matrix, and gap-validation block. Inline collector skeleton:

```python
# competitor_signals.py — minimal multi-source per-competitor row, ~45 lines
import json, sys, datetime as dt, requests
from urllib.parse import quote_plus

def hn(name: str) -> dict:
    r = requests.get("https://hn.algolia.com/api/v1/search",
                     params={"query": name, "tags": "story"}).json()
    return {"hn_hits": r.get("nbHits", 0), "source": "hacker_news"}

def gh(name: str) -> dict:
    r = requests.get("https://api.github.com/search/repositories",
                     params={"q": name, "sort": "stars"}).json()
    items = r.get("items") or []
    return {"gh_top_stars": items[0]["stargazers_count"] if items else 0,
            "gh_top_url": items[0]["html_url"] if items else "",
            "source": "github"}

def ph(name: str) -> dict:
    # Public PH search via web; agent-friendly seed only
    return {"ph_search_url": f"https://www.producthunt.com/search?q={quote_plus(name)}",
            "source": "product_hunt"}

def wayback(domain: str) -> dict:
    r = requests.get(f"http://archive.org/wayback/available?url={domain}/pricing").json()
    snap = (r.get("archived_snapshots") or {}).get("closest", {})
    return {"wayback_pricing_url": snap.get("url", ""), "source": "wayback"}

def collect(name: str, domain: str) -> dict:
    return {"competitor": name, "domain": domain,
            "ts": dt.datetime.utcnow().isoformat(),
            "signals": [hn(name), gh(name), ph(name), wayback(domain)]}

if __name__ == "__main__":
    print(json.dumps(collect(sys.argv[1], sys.argv[2]), indent=2))
```

Run on the 15-20 competitor list, pipe into the orchestrator as the evidence layer for the structured row schema above.

## Best practices
- **Force the four types.** Reject any competitor list missing substitute and indirect rows — that is where churn lives.
- **Evidence URL per cell, not per row.** A feature-matrix cell without `evidence_url` is implicitly "N". This single rule kills 80% of the hallucination class.
- **Quality column, not just Y/P/N.** Add `0-3` per cell so "feature exists but unusable" stops looking like parity.
- **Diff-friendly snapshots.** Date every report; store as `competitive-analysis-YYYY-MM-DD.md`. The deltas (price changed, feature shipped, headcount jumped) are the actual decision input on rerun.
- **Pair feature-gap with review-mining.** A gap nobody complains about in G2/Reddit is rarely a real gap — auto-pull complaints first, derive feature gaps second.
- **Visualping the pricing page.** A weekly diff on top-5 pricing pages is a free 80% of "competitive monitoring".
- **Keep a kill-list.** Gaps marked "skip" with a reason persist across sessions; the orchestrator must not re-recommend them.
- **Personal-fit / strategic-fit filter before whitespace shipping.** A real gap that does not match our distribution / skill / brand is still a skip.
- **2-week sanity gap on whitespace.** Never act on a "whitespace cell" found this session — log it, validate against demand signals, decide next run.
- **Anchor pricing pulls with a screenshot.** Playwright/single-file the pricing page to evidence/ — protects against "their site changed before review".

## AI-agent gotchas
- **Marketing-page parroting.** LLMs paraphrase the competitor's homepage tagline as "positioning" and call the matrix done. Force `evidence_urls` length ≥ 2 with at least one third-party source.
- **Numeric hallucination.** Funding totals, ARR, headcount get invented. Reject any numeric field without `source_url`.
- **Stale training data.** Without WebSearch, agents report a 2023 funding round as current. Always wire WebSearch / WebFetch and check returned URLs against `current_date`.
- **Optimistic gap recommendations.** Default LLM tone is helpful; the gap-validator critic + a forced "skip ≥40%" budget is non-negotiable.
- **Substitute-blindness.** Asking "find competitors of X" rarely returns spreadsheets / email / do-nothing. Prompt explicitly for each of the four types and reject the list if a category is empty without justification.
- **Feature-name drift.** "AI search" vs "semantic search" vs "natural-language search" splits a single capability across rows. Synonym-merge before the matrix fills.
- **Cell-stuffing.** Agents fill 100% of cells even when no public proof exists. Allow `"unknown"` as a valid status; require ≥80% known cells to ship the report.
- **Pricing-page truthiness for B2B.** Listed prices on enterprise tiers are anchors, not ACVs. Tag pricing rows with `"confidence": "low"` for "Talk to Sales" tiers.
- **Token blowup on review dumps.** Never paste full G2 review HTML into the matrix-filler. The review-miner must distill to top-5 complaints per competitor first.
- **2x2 axis ambiguity.** "Features simple → complex" gets scored differently every run. Anchor each axis with 3 named exemplars (e.g., "simple = Notion-shaped", "complex = Salesforce-shaped").
- **Whitespace mirage.** Empty cells get reported as opportunities without the demand-side check. Block report shipping until each whitespace candidate has a demand bullet from review-mining or interview transcripts.
- **Human-in-the-loop checkpoint.** Before the gap list becomes spec input, founder reviews the kill-list rationale for the rejected gaps — agents under-skip, founders over-skip, the diff is the real shortlist.

## References
- Michael Porter — "How Competitive Forces Shape Strategy" (HBR 1979) and the Five Forces framework. https://hbr.org/1979/03/how-competitive-forces-shape-strategy
- Adam Brandenburger / Barry Nalebuff — "Co-opetition" (1996) — substitutes/complementors framing.
- Strategyzer — Value Proposition Canvas (gap mapping). https://www.strategyzer.com/canvas/value-proposition-canvas
- a16z — "Market Sizing for Startups". https://a16z.com/
- Crunchbase API docs. https://data.crunchbase.com/docs
- G2 API + research methodology. https://documentation.g2.com/
- BuiltWith API. https://api.builtwith.com/
- Similarweb API. https://developers.similarweb.com/
- Klue / Crayon / Kompyte — CI platforms (vendor docs).
- Internet Archive Wayback Machine — programmatic access. https://archive.org/help/wayback_api.php
- Product Hunt API. https://api.producthunt.com/v2/api/graphql
- Hacker News (Algolia) API. https://hn.algolia.com/api
