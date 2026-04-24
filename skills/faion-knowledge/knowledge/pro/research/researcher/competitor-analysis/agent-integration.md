# Agent Integration — Competitor Analysis

## When to use
- Pre-MVP idea validation: have 5-10 candidate competitors, need a structured scan before committing engineering time.
- Positioning sprint: landing page or pricing page rewrite where you need a defensible differentiation statement.
- New feature greenlight: comparing how 3-7 incumbents implement a feature you are about to build.
- Quarterly market refresh: re-scoring a known set of competitors on price, feature flags, and traction.
- Pricing tier design: scraping public pricing pages of competitors to anchor your own tier ladder.
- Investor / pitch deck prep: building a credible competitor matrix slide with named gaps.

## When NOT to use
- Deep customer-pain discovery — use `pain-points` or `problem-validation` mode instead; competitors are a proxy, not a substitute for talking to users.
- Pure brainstorming with no candidates yet — run `idea-generation-methods` first; competitor analysis assumes a defined category.
- Regulated/B2B-enterprise procurement intelligence where pricing is hidden behind sales calls — agent will hallucinate numbers; use Gartner/Forrester analysts.
- Real-time monitoring of a single competitor (use a change-tracking service like Visualping, not a one-shot agent run).
- "Should we build this?" gut checks — competitor count alone does not answer that.

## Where it fails / limitations
- Public data ceiling: revenue, employee counts, churn are mostly inferred. Agents will confidently fabricate funding figures unless explicitly told to mark "estimated" or skip.
- Review-site bias: G2/Capterra reviews are skewed toward incentivised reviewers; weaknesses are under-reported.
- Pricing pages lie: shown price often excludes seat minimums, annual lock-in, or "contact us" tiers. Agents miss these footnotes.
- Indirect competitors are hard to enumerate algorithmically — humans must seed them.
- Snapshot rot: a competitor matrix is stale within 60-90 days. Agents do not auto-refresh unless scheduled.
- LLM context limits: a 15-competitor deep-dive overruns context if every pricing/feature page is dumped raw. Summarise per competitor before cross-comparison.

## Agentic workflow
Drive this with the `faion-research-agent` in `mode: competitors` as the orchestrator. It owns the 5-step framework (identify → map → analyse → gap → differentiate). Fan out per-competitor snapshot work to parallel sub-tasks (one Task call per competitor) so each runs in its own context window — this is critical because dumping 10 raw competitor websites into one prompt blows context and degrades the gap analysis. Reconvene results into the matrix and gap analysis in a final synthesis pass. Output goes to `.aidocs/product_docs/competitive-analysis.md`.

### Recommended subagents
- `faion-research-agent (mode: competitors)` — top-level orchestrator; owns framework, writes `competitive-analysis.md`. Model: opus (strategic synthesis).
- `faion-research-agent (mode: pricing)` — invoked as a sub-step for the pricing-tier comparison; produces tier-by-tier matrix. Model: sonnet.
- `faion-research-agent (mode: niche)` — chained after differentiation step to validate the chosen white-space is a real niche, not an empty quadrant for a reason.
- `faion-domain-checker-agent` — invoked if naming/repositioning falls out of differentiation; verifies any new brand candidates are buyable.
- Per-competitor fan-out: spawn N parallel `Task` calls (haiku for snapshot fill, sonnet for weakness extraction from reviews) to parallelise WebFetch I/O.
- `faion-sdd-executor-agent` — downstream consumer; reads `competitive-analysis.md` when scoping `spec.md` for a feature differentiator.

### Prompt pattern

Orchestrator entry:

```
Task(
  subagent_type="faion-research-agent (mode: competitors)",
  prompt="Analyse competitors for {product}. Seed list: {known_competitors}.
  Target: 5-10 direct, 3-5 indirect, 2-3 future. Use the 5-step framework
  in pro/research/researcher/competitor-analysis/README.md. For each
  competitor, spawn a parallel snapshot Task. Output to
  .aidocs/product_docs/competitive-analysis.md with positioning matrix and
  gap analysis. Mark all unverifiable numbers as 'estimated'."
)
```

Per-competitor snapshot fan-out:

```
Task(
  subagent_type="general-purpose",  # or haiku-tier worker
  prompt="Fill the Quick Competitor Snapshot template (see templates.md)
  for {competitor_name}. Sources: {homepage_url}, {pricing_url}, G2 page.
  Use WebFetch only — do not guess. If a field is unknown, write
  'unknown' (not a fabricated number). Return raw markdown only."
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` + `pup` / `htmlq` | Scrape pricing/feature pages deterministically | `apt install pup` / `cargo install htmlq` |
| `lynx -dump` | Strip pricing pages to plain text for LLM ingestion | `apt install lynx` |
| `gh search repos` | Find OSS competitors and read their READMEs | `gh` CLI |
| `wget --spider --recursive` | Map a competitor's sitemap quickly | bundled with wget |
| `playwright` (CLI/script) | Render JS-heavy pricing pages (Stripe-pricing-table style) | `npm i -D @playwright/test` |
| `jq` | Filter Product Hunt / G2 JSON exports | `apt install jq` |
| `whois`, `dig` | Founding date proxy (domain registration), MX records (email stack) | bundled |
| `tldr-bot` / `LinkedIn search via API` | Team size sanity check | LinkedIn API + cookie |
| `archive.org wayback CLI` | See competitor's pricing history | `pip install waybackpack` |
| `searxng` (self-hosted) | Bulk SERP scraping without API quotas | already running on faion infra (port 8888) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SimilarWeb | SaaS | API (paid) | Traffic estimates per domain; useful for "Est. Users" column |
| BuiltWith | SaaS | API (paid) | Tech stack detection; fills the "Technology" dimension |
| Wappalyzer | OSS + SaaS | CLI + API | Free for small batches; same role as BuiltWith |
| Crunchbase | SaaS | API (paid) | Funding, founding date, employees — official source |
| G2 / Capterra | SaaS | Scraping only (no public API) | Reviews + ratings; respect robots.txt and rate limits |
| Product Hunt | SaaS | GraphQL API (free tier) | Discovery, launch dates, upvotes as traction proxy |
| Visualping / Distill.io | SaaS | Webhook | Track competitor pricing/feature page changes; pipe to agent on diff |
| AppFollow / SensorTower | SaaS | API (paid) | Mobile competitor downloads + reviews |
| Reddit (via PRAW) | OSS lib | Python API | "Alternatives to X" threads; weaknesses in the wild |
| Hacker News Algolia | Free API | REST | Sentiment + comparison threads |
| Wayback Machine | Free | API | Historical pricing/messaging changes |
| Linkup / Tavily / Exa | SaaS | API (LLM-native search) | Drop-in WebSearch replacement with cleaner snippets |
| FireCrawl | SaaS + OSS | API | Crawl + markdown-ify a competitor site for LLM ingestion |
| Perplexity API | SaaS | API | Cited summary of "competitors of X" — fast seeding step |

## Templates & scripts

See `templates.md` for the full Competitor Analysis Report and Quick Competitor Snapshot. For agent-driven runs, this lightweight scrape-and-snapshot helper feeds the snapshot template:

```bash
#!/usr/bin/env bash
# scrape-competitor.sh — fetch homepage + pricing + G2 to feed an LLM
# Usage: ./scrape-competitor.sh <name> <homepage_url> <pricing_url>
set -euo pipefail
NAME="$1"; HOME_URL="$2"; PRICE_URL="${3:-$HOME_URL/pricing}"
OUT_DIR="./_competitors/$(echo "$NAME" | tr '[:upper:] ' '[:lower:]-')"
mkdir -p "$OUT_DIR"

fetch() {  # url -> markdown-ish plaintext
  local url="$1" file="$2"
  curl -fsSL -A "Mozilla/5.0 (compatible; faion-research)" "$url" \
    | lynx -stdin -dump -nolist -width=120 \
    > "$OUT_DIR/$file" || echo "FETCH_FAILED $url" > "$OUT_DIR/$file"
}

fetch "$HOME_URL"  "homepage.txt"
fetch "$PRICE_URL" "pricing.txt"
fetch "https://www.g2.com/search?query=${NAME// /+}" "g2.txt"
fetch "https://web.archive.org/web/2024*/$HOME_URL" "wayback.txt"

cat > "$OUT_DIR/_meta.json" <<EOF
{ "name": "$NAME", "home": "$HOME_URL", "pricing": "$PRICE_URL",
  "fetched_at": "$(date -Iseconds)" }
EOF
echo "→ $OUT_DIR ready for snapshot agent"
```

Pipe `_competitors/<slug>/*.txt` into the snapshot prompt; agent fills the Quick Competitor Snapshot template per folder, then the orchestrator merges them.

## Best practices
- Seed the competitor list with humans + customer interviews before agents — agents over-index on Google's first page and miss "what my friend uses".
- Force the agent to cite a URL for every factual cell (price, founding year, employee count); reject any cell without a source.
- Run snapshot agents in parallel (one per competitor), synthesis serially. Cuts wall-clock by 5-8x and isolates per-competitor context.
- Always include "future" competitors (AI startups, big-tech adjacencies) — they are the real threat in 18 months.
- Keep the matrix to ≤8 dimensions; more columns degrade the gap analysis signal.
- Differentiate on weakness, not feature parity: scrape 1-star reviews and turn the top-3 complaints into your messaging.
- Re-run quarterly with the same template; diff the markdown to see which competitors moved.
- Store the seed competitor list in version control (`.aidocs/product_docs/_competitors.yml`) so re-runs are reproducible.
- Mark every estimated number with `~` or `(est.)` and never let the agent strip those hedges in the synthesis pass.

## AI-agent gotchas
- Hallucinated funding/employee numbers: Crunchbase access is paid; without it, agents invent plausible figures. Mitigation: hard rule "if Crunchbase API not available, write 'unknown'".
- Pricing-page footnote blindness: agents ingest the headline price and miss "billed annually", "min 5 seats", "+ 2% transaction fee". Mitigation: explicitly ask "what is the effective monthly price for 1 user, billed monthly?".
- Geography drift: agent may pick competitors from a different region than your target market. Mitigation: pin geography in the prompt and reject any competitor whose primary market is elsewhere.
- "Big tech could pivot here" inflation: agents over-list future competitors (every product becomes "Google could enter"). Cap at 2-3 and require a concrete signal (job posting, acquisition, beta product).
- Stale data: training cutoff means competitors launched in the last 6 months may be missed entirely. Always force a fresh WebSearch pass for "<category> launched 2025-2026".
- Self-comparison bias: when you describe your product, the agent leans toward your strengths in the gap analysis. Have a different agent (or a "devil's advocate" sub-task) re-rank the gaps from the competitor's perspective.
- Over-trusting G2/Capterra ratings: paid placement skews stars. Sanity-check with Reddit + HN sentiment.
- Context overflow on 10+ competitors: never pass all raw scrapes into the synthesis prompt. Pre-summarise to the snapshot template first.
- **Human-in-the-loop checkpoints:** (1) approve the seed competitor list before deep dives, (2) review per-competitor snapshots for hallucinated facts, (3) sign off on the differentiation statement before it lands in marketing copy.

## References
- Michael Porter, *Competitive Strategy* (1980) — Five Forces, the canonical foundation.
- April Dunford, *Obviously Awesome* (2019) — positioning against alternatives, source of the "vs. competitors" framing used in this methodology.
- A. Osterwalder, *Value Proposition Design* — gap analysis as value-map / pain-gain alignment.
- `pro/research/market-researcher/competitor-analysis/README.md` — sibling methodology under the market-researcher skill.
- `pro/research/researcher/agent-invocation/README.md` — `faion-research-agent` invocation reference.
- Anthropic, *Building effective agents* (2024) — orchestrator-workers pattern (used here for per-competitor fan-out).
- Product Hunt API: https://api.producthunt.com/v2/docs
- G2 Crowd review categories: https://www.g2.com/categories
- Wayback Machine API: https://archive.org/help/wayback_api.php
