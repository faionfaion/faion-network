# Agent Integration — Competitor Analysis (market-researcher)

This file is the market-researcher angle: SWOT scoring, market-share estimation,
and portfolio benchmarking. For the product-builder / positioning angle (5-step
framework, gap-to-feature mapping, differentiation statement) see the sibling
`pro/research/researcher/competitor-analysis/agent-integration.md`.

## When to use
- Annual strategy review: scoring 8-15 named competitors on a SWOT grid as input to a board / strategy deck.
- Market-share estimation: producing defensible "X holds ~N% of category Y" claims from public proxies (traffic, downloads, employee growth, funding).
- Portfolio benchmarking: comparing one product line against 3-7 incumbents on a fixed scorecard (price index, feature count, NPS proxy, growth rate) for a quarterly portfolio review.
- M&A or partnership shortlist: ranking acquisition targets by SWOT fit + relative position on the strategic-group map.
- Investor due diligence: producing an evidence-backed competitor matrix for a Series A/B deck where every cell is sourced.
- Win-loss debrief input: cross-referencing lost deals with competitor SWOT to identify the recurring "T" (threat) you keep losing to.

## When NOT to use
- Single-feature spec or pricing-page rewrite — that is the `researcher` variant; SWOT/share work is overkill.
- Pre-MVP idea triage where you do not yet have a category or named competitors — use `idea-generation-methods` or `niche-evaluation` first.
- Real-time competitive monitoring — SWOT is a snapshot artifact; for live tracking use Visualping/Klue/Crayon, not a one-shot agent.
- Regulated / enterprise-only categories where market share is locked behind paid analyst reports (Gartner, IDC, Forrester) — agents will fabricate share numbers; buy the report.
- Hyperlocal markets (single city, single B2B niche < 50 buyers) — public proxies do not exist; do customer interviews instead.

## Where it fails / limitations
- **Share estimation is proxy-stacked**: traffic (SimilarWeb) + employees (LinkedIn) + reviews (G2) are correlated, not independent. Agents stack them and report false precision (`23.4%`). Round to 5% buckets and label "estimated".
- **SWOT becomes a tautology**: agents list "strong brand" as a strength because the company is well-known. Force every S/W/O/T to cite an external observation (a review quote, a metric, a job posting), not a vibe.
- **Opportunities/Threats collapse into the same bucket**: an LLM treats "AI disruption" as both. Mitigation: define O = external trend the *competitor* could ride; T = external trend that hurts *us if they ride it*.
- **Portfolio benchmarking drifts**: dimensions chosen in Q1 are not the dimensions that mattered in Q4. Lock the scorecard schema in version control.
- **Public-data ceiling for private companies**: pre-Series-B startups have no reliable share signal; agents will invent ARR. Hard-rule: "if not in Crunchbase or SEC filing, mark TBD".
- **Strategic-group maps are 2D**: the agent will pick the two axes that maximise visual separation, not the two that matter to buyers. Pre-commit to axes (e.g. price vs. feature breadth) before running.
- **SWOT recency bias**: weights the last 90 days of news heavily. Force a 3-year retrospective scan to catch structural threats.

## Agentic workflow
Drive this with the `faion-research-agent` in `mode: competitors` as orchestrator, but configured with the `market-researcher` profile (SWOT + share + portfolio outputs, not differentiation statement). Pipeline runs in three serial phases with intra-phase parallelism: **(1) seed + classify** competitors into strategic groups (single agent call), **(2) per-competitor SWOT + share-proxy collection** fanned out as N parallel `Task` calls so each runs in its own context window, **(3) synthesis** — cross-competitor portfolio scorecard, strategic-group map, share table — in a final orchestrator pass with a devil's-advocate review sub-task. Output to `.aidocs/product_docs/competitive-analysis.md` plus a structured `_competitors.yml` for re-runs and diffing.

### Recommended subagents
- `faion-research-agent (mode: competitors, profile: market-researcher)` — top-level orchestrator. Owns SWOT framework + portfolio scorecard. Model: **opus** (strategic synthesis is where cheap models drift into platitudes).
- `faion-research-agent (mode: pricing)` — chained sub-step for the price-index column of the scorecard. Model: **sonnet**.
- `faion-research-agent (mode: market)` — chained for TAM denominator before share estimation; share is meaningless without a denominator. Model: **sonnet**.
- Per-competitor SWOT fan-out workers — one parallel `Task` per competitor (model: **sonnet** for SWOT extraction from reviews/news; **haiku** is too lossy on weakness language).
- `faion-domain-checker-agent` — only invoked if the SWOT surfaces a name/brand collision worth flagging.
- `faion-sdd-executor-agent` — downstream consumer; reads the strategic-group map when scoping `spec.md` for differentiating features.
- "Devil's advocate" sub-task (general-purpose, opus) — re-runs the SWOT from each competitor's perspective on you; surfaces threats you under-weighted.

### Prompt pattern

Orchestrator entry (market-researcher profile):

```
Task(
  subagent_type="faion-research-agent (mode: competitors)",
  prompt="Profile: market-researcher. Build SWOT + market-share + portfolio
  scorecard for category {category}. Seed competitors: {seed_list}.
  Required outputs: (1) SWOT per competitor with cited evidence per quadrant,
  (2) market-share table in 5% buckets with proxy sources, (3) strategic-group
  map (axes: {axis_x}, {axis_y}) — DO NOT pick axes yourself, (4) portfolio
  scorecard vs. our product on dimensions: price_index, feature_count, nps_proxy,
  growth_proxy. Mark all numbers (est.). Reject any SWOT cell without an
  external citation. Output to .aidocs/product_docs/competitive-analysis.md
  and version the seed list to .aidocs/product_docs/_competitors.yml."
)
```

Per-competitor SWOT fan-out:

```
Task(
  subagent_type="general-purpose",  # sonnet
  prompt="Build SWOT for {competitor}. Sources: G2 reviews (last 90d, both
  5-star and 1-star), HN/Reddit threads, last 4 quarterly LinkedIn employee
  counts, Crunchbase, last 3 changelog/blog posts. Each S/W/O/T cell MUST
  cite a URL + a 1-line evidence quote. Reject 'strong brand' / 'good UX'
  unless backed by a review quote. Threats must be external (market trend,
  regulation, big-tech entry) — not internal weaknesses re-labelled.
  Return YAML matching the SWOT schema in templates.md."
)
```

Devil's-advocate pass (after synthesis):

```
Task(
  subagent_type="general-purpose",  # opus
  prompt="Read competitive-analysis.md. From {top_competitor}'s perspective,
  rebuild OUR SWOT. List the 3 threats they would target us with first.
  Flag any quadrant where our self-rated strength is their rated weakness."
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `similarweb` REST API (`curl + jq`) | Domain traffic per competitor → share-of-traffic proxy | https://docs.similarweb.com (paid) |
| `crunchbase-cli` (community) | Funding, employees, founding date for share-by-funding proxy | `pip install crunchbase` (unofficial) |
| `pup` / `htmlq` | Deterministic scrape of pricing + comparison pages for the scorecard | `apt install pup` / `cargo install htmlq` |
| `playwright` | Render JS-heavy pricing tables (Stripe-pricing-table) | `npm i -D @playwright/test` |
| `gh search repos` + `gh api` | OSS competitors: stars, contributors, release cadence as growth proxy | `gh` CLI |
| `searxng` (self-hosted on faion infra :8888) | Bulk SERP for evidence URLs without API quotas | already deployed |
| `waybackpack` | Pull historical pricing/feature/headcount snapshots for trend lines | `pip install waybackpack` |
| `linkedin-jobs-scraper` | Job-posting count over 12 months as growth/strategy proxy | `pip install linkedin-jobs-scraper` |
| `jq` + `yq` | Filter Product Hunt JSON, manage `_competitors.yml` portfolio schema | `apt install jq yq` |
| `dvc` or plain git | Version the SWOT YAML + scorecard CSV across quarterly re-runs | `pip install dvc` |
| `pandoc` | Render the markdown report into a strategy-deck PDF/PPTX | `apt install pandoc` |
| `csvkit` (`csvstat`, `csvjoin`) | Cross-join scorecard tables across quarters for diffing | `pip install csvkit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SimilarWeb | SaaS | API (paid) | Traffic share — primary proxy for B2C/SMB share estimation |
| Semrush / Ahrefs | SaaS | API (paid) | Organic-search share, paid-search overlap, keyword gap |
| Crunchbase | SaaS | API (paid) | Authoritative funding/employees/founding — required for share confidence |
| PitchBook / CB Insights | SaaS | API (enterprise) | Private-company revenue estimates; expensive but defensible for boards |
| Klue | SaaS | API + webhook | Purpose-built competitive intelligence platform; SWOT battlecards as a service |
| Crayon | SaaS | API + webhook | CI automation, change tracking, SWOT-style cards |
| Kompyte | SaaS | API | CI alerts; cheaper Klue alternative for solopreneurs |
| Owler | SaaS | API (free tier) | Crowdsourced revenue estimates and exec moves |
| G2 / Capterra / TrustRadius | SaaS | Scrape only | Reviews → SWOT W/S evidence; respect rate limits |
| Glassdoor | SaaS | Scrape | Employee reviews → internal-weakness signal (culture, retention) |
| LinkedIn (Sales Navigator API) | SaaS | API (paid) | Headcount trend, hiring velocity = growth proxy |
| Statista / IBISWorld | SaaS | API (paid) | Category-level TAM denominator — required for share % |
| AppFollow / SensorTower / data.ai | SaaS | API (paid) | Mobile downloads + revenue → share for app-category competitors |
| Built With / Wappalyzer | SaaS + OSS | API + CLI | Tech-stack overlap; threat detection (when competitor adopts your differentiator) |
| FireCrawl / Tavily / Exa | SaaS | API | LLM-native crawl + search for evidence URL collection |
| Wayback Machine | Free | API | Historical pricing/headcount/feature snapshots → trend lines |
| Visualping / Distill.io | SaaS | Webhook | Diff competitor pages between quarterly re-runs |

## Templates & scripts

See `templates.md` for the base Competitor Analysis Report and Quick Snapshot. The market-researcher angle adds three artifacts: a SWOT YAML schema, a portfolio scorecard CSV, and a share-estimation worksheet. The scorecard helper below builds a diffable CSV across quarters.

```bash
#!/usr/bin/env bash
# market-share-proxy.sh — assemble share-estimation proxies into one CSV row.
# Usage: ./market-share-proxy.sh <slug> <domain> <crunchbase_uuid>
set -euo pipefail
SLUG="$1"; DOMAIN="$2"; CB_UUID="${3:-}"
Q="$(date +%Y)Q$((($(date +%-m)-1)/3+1))"
OUT="./_portfolio/${Q}.csv"
mkdir -p "$(dirname "$OUT")"
[ -f "$OUT" ] || echo "quarter,slug,domain,traffic_visits,employees,gh_stars,wayback_pricing_changes,funding_usd" > "$OUT"

traffic=$(curl -fsSL "https://api.similarweb.com/v1/website/$DOMAIN/total-traffic-and-engagement/visits?api_key=$SIMILARWEB_KEY&granularity=monthly" \
  | jq -r '[.visits[].visits] | add // "TBD"')
emp=$(curl -fsSL -H "X-cb-user-key: $CRUNCHBASE_KEY" \
  "https://api.crunchbase.com/api/v4/entities/organizations/$CB_UUID?field_ids=num_employees_enum" \
  | jq -r '.properties.num_employees_enum // "TBD"')
stars=$(gh api "search/repositories?q=user:$SLUG" --jq '[.items[].stargazers_count]|add // "TBD"' 2>/dev/null || echo TBD)
funding=$(curl -fsSL -H "X-cb-user-key: $CRUNCHBASE_KEY" \
  "https://api.crunchbase.com/api/v4/entities/organizations/$CB_UUID?field_ids=funding_total" \
  | jq -r '.properties.funding_total.value_usd // "TBD"')
pricing_changes=$(waybackpack -d /tmp/wb "https://$DOMAIN/pricing" --from-date 2023 2>/dev/null \
  | wc -l || echo TBD)

echo "$Q,$SLUG,$DOMAIN,$traffic,$emp,$stars,$pricing_changes,$funding" >> "$OUT"
echo "→ row appended for $SLUG in $OUT"
```

Run per competitor in the seed list; agent then ingests the CSV (small enough to fit in context) and computes share buckets without re-fetching. Diff `2025Q4.csv` vs `2026Q1.csv` to spot moves.

## Best practices
- **Lock the scorecard schema** (`_competitors.yml` + scorecard column headers) in git before the first run; quarterly re-runs must use the same dimensions or the diff is meaningless.
- **Round share to 5% buckets** and always print "(est.)"; precision beyond that is fake. If share < 5%, print "long tail".
- **Force one citation URL per SWOT cell.** Reject the cell otherwise. This single rule eliminates ~80% of LLM SWOT slop.
- **Separate Opportunities (external trends competitor can ride) from Threats (external trends that hurt us if competitor rides them).** Most LLM-generated SWOTs collapse these.
- **Run the devil's-advocate pass on every synthesis.** Self-comparison bias makes agents under-weight competitor strengths against you.
- **Use a denominator before quoting share.** Run `mode: market` (TAM/SAM/SOM) first; share is a fraction, not a count.
- **Triangulate share** with at least two proxies (traffic + employees, or downloads + revenue). One proxy = guess.
- **Cap "future competitors" at 2-3 with a concrete signal.** "Big tech could enter" is not a signal; a job posting, beta launch, or acquisition is.
- **Pre-commit the strategic-group axes.** Do not let the agent pick the axes that maximise visual separation.
- **Diff quarterly with `csvjoin`/`git diff`** on the scorecard; the deltas are the strategy story, not the absolute values.
- **Tag every estimate with confidence** (`high` = official source, `med` = proxy-triangulated, `low` = single proxy or inferred). Strip nothing in synthesis.

## AI-agent gotchas
- **Hallucinated funding / ARR**: without paid Crunchbase/PitchBook access the agent invents plausible figures. Hard rule: "if API key absent, write TBD" and audit the output for any `$N` not in the source CSV.
- **SWOT tautology**: agent writes "strong brand" because the brand is famous. Reject any S/W cell whose evidence is the agent's prior knowledge rather than a fetched URL.
- **Share-precision overconfidence**: agent reports `23.4%`. Force-round to 5% buckets in the prompt and reject any number with a decimal.
- **Strategic-group axis-shopping**: agent picks axes post-hoc to make the picture clean. Pin axes in the prompt; if the data does not separate, that is the finding.
- **Context overflow on 10+ competitors**: do not pass raw scrapes into synthesis. SWOT each competitor to YAML first, then synthesise from the YAMLs only.
- **Recency bias**: SWOT skews to last-90-days news. Force a 3-year retrospective scan ("structural threats since 2023") as a separate sub-task.
- **Geography / segment drift**: agent picks competitors from the wrong geography or wrong customer size. Pin both in the prompt; reject any competitor primarily serving outside scope.
- **Portfolio scorecard column drift**: agent invents new columns each quarter to "improve" the scorecard. Lock the schema and reject extra columns.
- **TAM-less share**: agent reports "X has 30% market share" without naming the denominator. Hard rule: every share % must be paired with a TAM source.
- **OSS-stars as revenue proxy**: agent equates GitHub stars with market share. They correlate weakly with developer mindshare, not with revenue. Use only as a tertiary signal.
- **Human-in-the-loop checkpoints:** (1) sign off on seed list + strategic-group axes before SWOT runs, (2) review per-competitor SWOT YAMLs for cited-URL discipline, (3) approve the share-bucket table and TAM denominator before it lands in board materials, (4) accept or reject devil's-advocate findings before the executive summary.

## References
- Michael Porter, *Competitive Strategy* (1980) — Five Forces and strategic-group maps; foundation of the portfolio-benchmarking angle.
- Albert Humphrey, SWOT framework (Stanford SRI, 1960s) — origin of the 2x2 used here.
- Aaker, *Strategic Market Management* — competitor scorecard and strategic-group methodology.
- Kim & Mauborgne, *Blue Ocean Strategy* — strategy-canvas alternative to the strategic-group map.
- Gartner Magic Quadrant methodology notes — public criteria document for axis discipline.
- `pro/research/researcher/competitor-analysis/agent-integration.md` — sibling product-builder angle.
- `pro/research/market-researcher/market-research-tam-sam-som/` — TAM denominator for share estimation.
- `pro/research/market-researcher/competitive-intelligence/` — adjacent CI workflow (live monitoring vs. snapshot).
- Anthropic, *Building effective agents* (2024) — orchestrator-workers pattern used for per-competitor SWOT fan-out.
- SimilarWeb API: https://docs.similarweb.com
- Crunchbase API: https://data.crunchbase.com/docs
- Klue / Crayon documentation — battlecard schemas referenced in the SWOT YAML template.
