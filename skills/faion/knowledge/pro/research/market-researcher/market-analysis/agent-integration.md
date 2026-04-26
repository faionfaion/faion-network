# Agent Integration — Market Analysis

Covers four sub-methodologies in this folder: TAM/SAM/SOM sizing, trend
analysis, competitor analysis, and competitive intelligence (feature-gap
matrix). All four are ranged together because in agent runs they share the same
data sources, the same scraping/search tooling, and the same output artefacts.

## When to use

- Before writing a `spec.md` for a new product idea — produces the SAM number
  and competitive whitespace that justify the build.
- When the GTM strategist or product manager asks for a quantified opportunity
  ($X M SAM, Y% CAGR, Z named direct competitors).
- Quarterly competitor refresh: re-scrape pricing pages, changelogs, and review
  sites to spot pricing/positioning moves.
- Pre-fundraise: investor decks need a defensible TAM and a feature matrix.
- Niche viability scoring inside `niche-evaluation` flows — feeds the 5-criteria
  rubric with hard numbers instead of guesses.

## When NOT to use

- Single-customer custom builds (no market, just one buyer).
- Pure technical/architecture research — wrong skill, route to
  `pro/dev/software-architect` instead.
- Ideas <2 weeks from launch where research will not change the decision —
  ship and learn from real usage.
- Highly regulated B2B niches (defense, medical devices) where public data is
  scarce; you need primary expert interviews, not desk research.
- When the user already has a working business — switch to
  `growth-marketer` / `conversion-optimizer` instead of re-sizing the market.

## Where it fails / limitations

- **TAM theatre**: top-down numbers from Gartner/Statista PDFs are routinely
  inflated 3-10x. LLMs happily parrot them. Always demand a bottom-up
  cross-check.
- **Hallucinated competitors**: web-search agents invent product names that do
  not exist or merge two products into one. Require URL + screenshot evidence.
- **Stale pricing**: cached pages on Bing/Google often lag 6-18 months behind
  actual SaaS pricing pages. Always re-fetch the live URL.
- **Feature matrix drift**: competitors ship weekly; a matrix older than 90
  days is decorative.
- **Adoption-curve guessing**: "Early Majority" labels are subjective and
  unfalsifiable; force the agent to cite revenue, user count, or category
  spend instead.
- **Geography blind spots**: most LLM training data is US/EU heavy. SAM
  estimates for LATAM / SEA / Africa are often missing entire local players.

## Agentic workflow

Drive market analysis as a four-step pipeline: (1) a sizing pass produces TAM/
SAM/SOM with both top-down and bottom-up checks, (2) a trend pass classifies
macro/industry/micro drivers and timing, (3) a competitor-discovery pass
returns 15-20 named players with URLs, (4) a feature-matrix pass extracts a
gap table from the top 5. Each pass is a separate subagent invocation so
context windows stay small and outputs are JSON-validated. The market-research
skill is a sub-skill of `faion-researcher`; the orchestrator calls it for the
"market" mode while delegating "user" mode to `user-researcher`.

### Recommended subagents

- `faion-research-agent` (mode: `market`) — primary executor referenced in this
  folder's README; performs sizing, trend, competitor, and intelligence
  passes.
- `faion-research-agent` (mode: `competitors`) — narrower invocation for
  competitor-only and feature-matrix work.
- `faion-sdd-executor-agent` — picks up an SDD task that wraps the four
  passes, commits the resulting `market-analysis.md` artefact under the
  feature folder.
- `faion-brainstorm` — useful before sizing to diverge on "who else could be a
  competitor" (substitute / potential categories that desk research misses).

### Prompt pattern

Sizing pass (bottom-up enforced):

```
Mode: market. Topic: <product idea>. Geography: <region>.
Produce TAM, SAM, SOM. SAM must include BOTH top-down (industry report cited
with URL + year) AND bottom-up (count_of_potential_customers * avg_ARPU).
If the two diverge >2x, flag and explain. Output JSON only:
{tam_usd, sam_usd, som_usd_year1, top_down_source, bottom_up_count, bottom_up_arpu, divergence_note}.
```

Competitor discovery pass:

```
List 15-20 competitors for <product>. For each: name, url, founded_year,
funding_usd, pricing_tier_low, pricing_tier_high, primary_differentiator,
type (direct|indirect|substitute|potential). Reject any entry without a
working URL. Output JSON array.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `searxng` (self-hosted) | Anonymous meta-search; primary search backend in NERO at port 8888. Avoids Google captchas during agent runs. | `~/workspace/tools/searxng` |
| `firecrawl` | LLM-friendly scrape/crawl of competitor sites and pricing pages, returns clean markdown. | `npm i -g firecrawl-cli` · firecrawl.dev |
| `crawl4ai` | OSS scraping framework optimized for agent pipelines, handles JS-rendered SaaS pages. | `pip install crawl4ai` |
| `trafilatura` | Extracts main text from competitor blog/landing pages, faster than headless browsers. | `pip install trafilatura` |
| `gh` (GitHub CLI) | Pull star counts, contributor counts, last-release date for OSS competitors. | `apt install gh` |
| `pytrends` | Unofficial Google Trends API, used for trend-analysis timing. | `pip install pytrends` |
| `yfinance` | Public-company revenue/market-cap for substitute or incumbent competitors. | `pip install yfinance` |
| `jq` | Required to parse the JSON outputs above into matrix tables. | `apt install jq` |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Crunchbase | SaaS | Partial (paid API) | Funding, founded date, employee count for direct competitors. Free tier is rate-limited. |
| SimilarWeb | SaaS | Yes (paid API) | Traffic estimates → bottom-up SOM cross-check. |
| Statista | SaaS | No | PDF reports, top-down TAM. Cite as source, do not let agent download whole PDFs. |
| G2 / Capterra | SaaS | Partial (scrape) | Review counts, feature ratings; primary input for the feature-matrix gap pass. |
| Product Hunt | SaaS | Yes (free API) | Discover new entrants in the last 30/90 days. |
| BuiltWith | SaaS | Yes (paid) | Tech-stack fingerprinting of competitors. |
| Wayback Machine | OSS/free | Yes | Historical pricing pages → confirm price moves over time. |
| Sensor Tower / data.ai | SaaS | No (expensive) | Mobile-app revenue; only for app-market analysis. |
| Pitchbook | SaaS | No | Enterprise-only; out of reach for solopreneur agents. |
| OpenCorporates | OSS | Yes | Company-registry data, useful for non-US competitors. |
| Perplexity / Exa.ai | SaaS | Yes (API) | Citation-first search; agent-grade source quality for trend pass. |

## Templates & scripts

See `templates.md` for the TAM/SAM/SOM, trend, competitive landscape, and
feature-matrix Markdown blocks. The script below freezes a competitor URL set
into a dated snapshot folder so the matrix is reproducible:

```bash
#!/usr/bin/env bash
# competitors_snapshot.sh — freeze a competitor list as Markdown via firecrawl
# usage: competitors_snapshot.sh urls.txt out_dir
set -euo pipefail
urls="${1:?urls.txt required}"
out="${2:?out_dir required}"
stamp="$(date -u +%Y%m%d)"
mkdir -p "$out/$stamp"
while IFS= read -r url; do
  [[ -z "$url" || "$url" =~ ^# ]] && continue
  slug="$(printf '%s' "$url" | sed 's|https\?://||;s|/.*||;s|\.|_|g')"
  echo "scrape: $url -> $out/$stamp/$slug.md"
  firecrawl scrape "$url" --format markdown \
    --only-main-content --timeout 30000 \
    > "$out/$stamp/$slug.md" || echo "FAIL $url" >> "$out/$stamp/_errors.log"
done < "$urls"
jq -n --arg stamp "$stamp" --arg src "$urls" \
  '{snapshot:$stamp, source:$src, files:input_filename}' \
  > "$out/$stamp/_manifest.json" 2>/dev/null || true
echo "snapshot ready: $out/$stamp"
```

Output feeds directly into a feature-matrix LLM pass: each `*.md` is a
competitor; the agent reads them in parallel and emits the matrix as JSON.

## Best practices

- Force every TAM number to carry `(source, year, geography)` triple in the
  same line; reject standalone dollar figures.
- Always run sizing top-down AND bottom-up; flag divergence >2x as a research
  gap, not a number to average.
- Cap the competitor list at 20 named entries with URLs; longer lists are
  hallucination magnets and nobody reads them.
- Snapshot competitor sites (`competitors_snapshot.sh`) before running the
  matrix — the data layer must be reproducible 6 months later.
- Make whitespace claims falsifiable: link to the specific competitor pricing
  pages and changelogs that confirm the gap exists.
- Re-run the trend pass quarterly; macro trends move slower than agents'
  patience but micro trends invalidate fast.
- Store outputs as JSON first, render to Markdown after — trivial to diff
  across quarters.
- Cite review-site evidence (G2, Capterra, Reddit threads) for every
  identified gap, with at least 5 corroborating reviews.

## AI-agent gotchas

- Agents conflate "market size" (revenue) with "user count"; always demand
  units. SAM in $ vs SAM in seats are different artefacts.
- LLMs invent CAGR percentages with two decimals; treat anything more
  precise than the nearest 5% as fabricated unless cited.
- Web-fetch tools silently truncate pricing tables on long landing pages —
  pass `--only-main-content` and verify line count.
- Subagents will gladly cite paywalled Gartner/Forrester reports they cannot
  read; require a public URL or "(source unverified)" tag.
- Trend timing ("Early Majority") is subjective; require quantitative anchor:
  category spend, named buyer logos, or revenue at top 3 players.
- Feature-matrix passes in long context degrade after ~10 competitors; chunk
  to 5 per call and merge the JSON.
- Substitute and potential competitors are routinely missed; add a
  brainstorm step (faion-brainstorm) explicitly named "what else solves this
  job?" before locking the list.
- Human-in-the-loop checkpoints: (1) before locking SAM number, (2) before
  shipping competitor list to stakeholders, (3) before declaring whitespace
  "validated" (someone with domain experience must confirm).

## References

- Christensen, Cook, Hall — "Marketing Malpractice: The Cause and the Cure"
  (HBR 2005) — jobs-to-be-done framing for substitutes.
- a16z — "16 Startup Metrics" (2015) — bottom-up SAM construction.
- "Crossing the Chasm" — Geoffrey Moore — adoption-curve framework used in
  trend analysis.
- Firecrawl docs: https://docs.firecrawl.dev
- SearXNG: https://docs.searxng.org
- G2 review-mining for competitive gaps:
  https://documentation.g2.com/docs/research-api
- `pro/research/researcher/competitor-analysis/agent-integration.md` (sister
  methodology focused on the discovery pass alone).
