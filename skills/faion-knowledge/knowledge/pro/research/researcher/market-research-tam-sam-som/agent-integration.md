# Agent Integration — Market Research (TAM/SAM/SOM)

## When to use
- Pre-spec phase: founder needs a sanity check on whether a niche clears a revenue floor (e.g. SOM > $1M ARR in 3 years).
- Pitch decks, investor memos, grant applications that demand a numerical market frame.
- Pricing or positioning decisions where segment economics matter (SAM × ARPU sets the realistic envelope).
- Comparing two adjacent niches before committing to MVP scope.
- Annual roadmap review: re-sizing as the segment shifts (new geography, new tier, post-funding).

## When NOT to use
- Hobby projects, internal tools, free OSS — sizing adds zero signal.
- Replacement for actual customer interviews; TAM/SAM/SOM is not problem validation.
- Already-shipping products with real ARR — extrapolate from cohorts, not market reports.
- Two-sided marketplaces in pre-launch — supply/demand dynamics dominate raw market size.
- Deep-tech with a 10-year horizon — market category may not exist yet.
- Regulated markets pre-license (medical, fintech) where addressable share depends on regulator decisions, not buyer count.

## Where it fails / limitations
- Garbage-in: agents pull a Statista headline number from a paywalled snippet and treat it as ground truth.
- Compounding error: TAM × 2% × 50% × 0.5% creates four-decimal precision from four guesses.
- Stale data: most "market size" reports cited online are 2-3 years old; CAGR projections diverge fast.
- Survivor bias in competitor-based sizing: only public/funded competitors are visible; long tail is invisible.
- "LinkedIn × $200K/employee" is a rule of thumb that breaks for high-margin SaaS and low-margin services.
- SOM is the most-faked number in startup decks; LLMs tend to anchor on whatever the user hints at.

## Agentic workflow
The agent runs three parallel sizing methods (top-down, bottom-up, competitor-based), records every source URL and assumption, then triangulates. Each method must produce an independent number; if they diverge by more than 2x, the agent flags the spread and asks for a tie-breaker rather than averaging silently. Output is written to `.aidocs/product_docs/market-research.md` using the README template, with a confidence column per row.

Concrete pipeline:
1. ICP lock — agent restates the ICP in one sentence and waits for explicit confirmation before any number is fetched.
2. Top-down fetch — `WebSearch` for "<industry> market size <year>", capture top 3 sources, prefer government/Statista/Gartner; archive each via Wayback.
3. Bottom-up build — count target companies via Census/Eurostat/Apollo, multiply by realistic ARPU.
4. Competitor sweep — pull Crunchbase + SimilarWeb for top 5 competitors, sum + extrapolate the long tail (typically 1.5x of named players).
5. Triangulate — run `tam-triangulate.sh`, write median to report only when spread ≤ 2x.
6. Confidence tagging — every cell gets H/M/L based on source primacy and recency (≤ 12 months = H).
7. Validation pass — secondary agent re-reads the report against `checklist.md` and returns a delta list.

### Recommended subagents
- `faion-research-agent` — orchestrator, 9 modes, dispatches `mode=market` for TAM/SAM/SOM runs.
- `faion-market-researcher-agent` — methodology-aware sizing agent (declared in README front-matter).
- `faion-domain-checker-agent` — pairs naturally for naming/availability when the sizing concludes "go".
- General `web-research` / `WebSearch` subagent — pulls Statista, Gartner, Crunchbase, SimilarWeb snippets.
- Sibling methodologies in `../../market-researcher/`: `competitor-analysis`, `business-model-research`, `trend-analysis` — chain after sizing.

### Prompt pattern
```
You are a market sizer. Compute TAM, SAM, SOM for: <niche>.
Constraints: <geo, segment, ICP>. Horizon: 3 years.
Run THREE methods (top-down, bottom-up, competitor) IN PARALLEL.
For every number cite the source URL + retrieval date.
If methods diverge >2x, do NOT average — return both and flag.
Output: markdown matching templates.md "Market Sizing Report".
```
```
Validate this sizing: <paste numbers + assumptions>.
Check: (1) does TAM cite a primary source? (2) is SAM constraint stack independent?
(3) is SOM share within Year-N table from README? Return a delta list, not a rewrite.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Pull competitor repos, stars, contributor counts as a proxy for traction | `brew install gh` / cli.github.com |
| `crunchbase-api` (REST) | Funding, headcount, founded-year for competitor sizing | data.crunchbase.com/docs |
| `similarweb-api` | Traffic, engagement, top countries — feeds bottom-up reach math | developers.similarweb.com |
| `linkedin-api` (unofficial Python lib) | ICP count via Sales Nav search; respect ToS, prefer official | pypi.org/project/linkedin-api |
| `census-bureau-api` (US, free) | Establishment counts by NAICS for ground-truth top-down | api.census.gov |
| `eurostat-api` (EU, free) | Same for EU establishments by NACE | ec.europa.eu/eurostat/api |
| `statista` (no public API) | Paid; scrape via authenticated session, cite report ID | statista.com |
| `wayback-machine` (`waybackpack`) | Pin a market-report URL to a retrieval date for reproducibility | github.com/jsvine/waybackpack |
| `pandoc` + `csvkit` | Convert pulled tables into the report template | csvkit.rtfd.io |
| `claude` (Anthropic CLI) | Run the agent prompts above in batch | docs.anthropic.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Statista | Paid market reports | Partial — HTML scrape, no open API | Best single source for TAM headline numbers |
| Gartner / Forrester | Paid analyst reports | No — PDFs behind enterprise paywall | Cite second-hand via press releases |
| IBISWorld | Industry reports | Partial — login scrape | Strong for US/AU verticals |
| Crunchbase | Funding/competitor DB | Yes — REST API, key required | Ground truth for "how big is competitor X" |
| PitchBook | Private market data | Partial — enterprise API | Better than Crunchbase for late-stage |
| SimilarWeb | Traffic estimates | Yes — REST API, paid | Bottom-up reach proxy |
| Semrush / Ahrefs | SEO traffic | Yes — REST API | Search-demand proxy for SOM |
| LinkedIn Sales Navigator | ICP counting | Hostile — ToS blocks scraping | Use for one-off counts, not pipelines |
| Google Trends | Demand signal | Yes — `pytrends` | Cheap CAGR sanity check |
| US Census BDS, Eurostat, OECD | Government stats | Yes — free APIs | Most reliable bottom-up anchor |
| Apollo.io / Clearbit | B2B contact DB | Yes — REST API | Count companies matching firmographics |
| Product Hunt | Launch traction | Yes — GraphQL API | Cheap competitor-discovery layer |
| G2 / Capterra | Software reviews | Partial — scrape | Competitor revenue proxy via review counts |

## Templates & scripts
See `templates.md` for the full Market Sizing Report. Inline triangulation helper:

```bash
#!/usr/bin/env bash
# tam-triangulate.sh — flags divergence across three sizing methods
# usage: ./tam-triangulate.sh <topdown> <bottomup> <competitor>
set -euo pipefail
td=$1; bu=$2; cp=$3
min=$(printf '%s\n' "$td" "$bu" "$cp" | sort -g | head -1)
max=$(printf '%s\n' "$td" "$bu" "$cp" | sort -g | tail -1)
ratio=$(awk -v a="$max" -v b="$min" 'BEGIN{printf "%.2f", a/b}')
median=$(printf '%s\n' "$td" "$bu" "$cp" | sort -g | awk 'NR==2')
echo "top-down=$td  bottom-up=$bu  competitor=$cp"
echo "median=$median  spread=${ratio}x"
awk -v r="$ratio" 'BEGIN{ exit !(r > 2.0) }' \
  && echo "FLAG: spread > 2x — do not average, investigate" \
  || echo "OK: within 2x, median is defensible"
```

## Best practices
- Lock the ICP definition in one sentence before any number is computed; "all SMBs" is not an ICP.
- Always run bottom-up second, after top-down — it forces the agent to reconcile, not to anchor.
- Cite source + retrieval date on every line; archive paywalled pages via Wayback before quoting.
- Round aggressively: $8.3B is fake precision, $8B is honest. Two significant figures max for TAM/SAM.
- Express SOM as a customer count first, dollars second: "1,000 customers × $50/mo" beats "$600K".
- Keep an assumptions ledger at the bottom of the report — every multiplier on its own row, swappable.
- Re-run the sizing every 6 months; diff the assumptions, not the headline number.
- For B2B, use government establishment data (Census/Eurostat) as the top-down anchor — it is free and primary.
- Cross-check competitor revenue with two independent signals (e.g. Crunchbase ARR + SimilarWeb traffic) before trusting a number.
- Tag every multiplier as Hard (sourced) or Soft (estimate); refuse to publish if Soft multipliers compound more than 3 deep.
- Capture the report as a git commit under `.aidocs/product_docs/` so future sizings can `git diff` against the baseline.

## Integration with faion-net SDD
- Sizing output lives in `.aidocs/product_docs/market-research.md`; downstream `spec.md` references SOM as the revenue ceiling.
- `faion-research-agent` writes the file; `faion-product-manager-agent` reads it to set MRR targets in `roadmap.md`.
- For the workspace `pro` tier, this methodology is the canonical TAM/SAM/SOM source — there are two parallel copies (`researcher/` and `market-researcher/`); keep them in sync via the `researcher` orchestrator only.
- When run inside `/faion-net` mode `market`, the agent appends a "Market Sizing" section to `executive-summary.md` automatically.

## AI-agent gotchas
- LLMs hallucinate market-size numbers fluently; require a URL for every figure or reject the line.
- Confirmation bias: if the user hints "this should be a $1B market", the agent will reverse-engineer to $1B. Pre-commit the methodology before sharing the hypothesis.
- Currency drift: agents mix USD, EUR, GBP within one report. Normalize to USD with a dated FX rate.
- Stale training data: the model "knows" 2023 market sizes; force a fresh web fetch for any post-2024 number.
- Multiplication of fractions: `0.6 × 0.5 × 0.5 × 0.01` generates false precision. Round each multiplier to one significant figure.
- Confusing GMV with revenue: marketplaces report GMV; SaaS reports ARR; do not add them.
- Ignoring growth: a static $5B TAM today may be $9B at a 12% CAGR in 5 years; SOM horizon must match TAM horizon.
- "LinkedIn employee count × $200K" rule undercounts services and overcounts seed-stage SaaS — disable for any company under 20 people.
- Tier gating: this methodology lives in `pro/`; if the calling agent has only `free`/`solo` tier access, abort instead of approximating.
- Output drift: the agent rewrites the template on each run; lock to the headings in `templates.md` and only fill cells.

## References
- README, checklist, templates, examples, llm-prompts (this directory).
- Sibling: `../../market-researcher/market-research-tam-sam-som/` (parallel copy under `market-researcher` skill).
- Related methodologies in this skill: `competitor-analysis`, `pricing-research`, `niche-evaluation`, `mvp-scoping`, `roadmap-design`.
- Steve Blank, "Market Size: TAM, SAM, SOM" — steveblank.com
- a16z, "16 Startup Metrics" — a16z.com/2015/08/21/16-metrics
- CB Insights "State of Venture" — cbinsights.com/research
- US Census BDS — census.gov/programs-surveys/bds
- Eurostat structural business statistics — ec.europa.eu/eurostat
- Crunchbase API docs — data.crunchbase.com/docs
- SimilarWeb API — developers.similarweb.com
