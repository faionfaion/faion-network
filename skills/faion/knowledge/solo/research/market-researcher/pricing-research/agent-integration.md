# Agent Integration — Pricing Research

## When to use
- Pre-launch: validating tier structure and price points before publishing pricing page.
- Quarterly pricing review: re-running competitor matrix + customer interviews after market shift.
- Pivoting model (one-time → subscription, or freemium → paid trial).
- Setting enterprise/custom price floor for first sales call.

## When NOT to use
- You have <50 paying customers — go talk to them directly, not run an agent.
- B2B enterprise contract negotiation — pricing here is relationship/procurement-driven, not formula-driven.
- Heavily regulated pricing (insurance, prescription, utility) — agent will not know jurisdiction-specific rules.
- Marketplace/two-sided pricing — supply-and-demand dynamics that need real telemetry, not survey output.

## Where it fails / limitations
- Van Westendorp requires real respondents. Agents simulating "what customers would say" produce confabulated price points centered on training-data anchors ($29, $49, $99, $299).
- Competitor pricing scraping is brittle — pricing pages are often gated behind "Contact us" or A/B tested. WebFetch sees public list price, not effective price.
- LLMs anchor heavily on the first competitor mentioned; randomize order or instruct "treat each competitor independently before synthesizing".
- Capture-rate heuristic (10-20%) is a folk number; for low-touch SaaS it's closer to 1-3% of value delivered.
- Currency / regional purchasing-power adjustments are routinely missed.

## Agentic workflow
Three-stage pipeline: (1) `competitor-scraper` agent collects 8-12 competitor pricing tables via WebFetch, returns normalized matrix. (2) `value-modeler` agent computes value-based price ceiling from interview transcripts + usage data. (3) `tier-designer` agent proposes 3-tier structure with feature distribution, justifies each price-jump. Human reviews — pricing is final-call human territory. Re-run on a 90-day cadence and diff against prior output to catch market drift.

### Recommended subagents
- `competitor-scraper` — sonnet + WebFetch, single-purpose: URL list → normalized pricing matrix JSON.
- `value-modeler` — sonnet, takes interview quotes + savings claims, returns value/month per persona.
- `tier-designer` — opus (this is strategy, not pattern-matching), proposes tiers with explicit psych anchors.
- Avoid letting one agent do all three; pricing logic compounds errors.

### Prompt pattern
```
URLs: [list of 10 competitor pricing pages]
For each, extract: tier_name, monthly_price, annual_price, included_features,
limits, free_tier_exists. Return JSON. If a page hides price behind contact
form, mark price=null and note "sales-led". Do not estimate.
```

```
Interviews (N=12): {transcripts}
Estimated time-saved per persona, monetized at persona's hourly rate.
Return: per-persona value/month, capture-rate floor (1%) and ceiling (15%),
and which Van Westendorp question each quote answers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` + `pup` | Scrape pricing tables | `brew install pup` |
| `playwright` (Python/Node) | Render JS-heavy pricing pages | `pip install playwright && playwright install` |
| `crawl4ai` | LLM-friendly scrape with markdown output | `pip install crawl4ai` |
| `vw-pricing` (R, OSS) | Van Westendorp analysis | CRAN: `pricesensitivitymeter` |
| `claude` | Drive sub-agents, WebFetch | https://docs.anthropic.com/en/docs/claude-code |
| `csvkit` | Diff competitor matrices over time | `pip install csvkit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Pricing Tables | SaaS | Yes (API) | Programmatic price object; A/B test via test mode. |
| Paddle / Lemon Squeezy | SaaS | Yes | Merchant-of-record; supports tier experiments. |
| ProfitWell (Paddle) | SaaS | Yes | Free tier benchmarks SaaS pricing distributions. |
| OpenView SaaS Benchmarks | Report | Read-only | Annual pricing benchmark report; cite for board. |
| Wayback Machine | Free | Yes | Track competitor price history; agents can fetch dated snapshots. |
| Capterra / G2 | SaaS | Limited | Pricing fields in product pages; many "contact for pricing" — agent must mark unknown. |
| Maxio (Chargify) | SaaS | Yes | Usage-based billing experiments; rate-card SDK. |
| Userpilot / Pendo | SaaS | Yes (API) | Run pricing-page A/B with cohort splits. |

## Templates & scripts
See `templates.md` for Pricing Research Report and Quick Pricing Check. Minimal competitor-matrix script:

```bash
#!/usr/bin/env bash
# competitor-pricing.sh — run weekly, diff vs. last week
set -euo pipefail
URLS_FILE=${1:?urls.txt required}
OUT=~/pricing/$(date +%F).json
mkdir -p ~/pricing

# Fetch each URL with WebFetch via Claude, normalize to schema
claude -p "$(cat ~/prompts/competitor-extract.txt)" \
  --input-file "$URLS_FILE" \
  > "$OUT"

# Diff vs. previous run
PREV=$(ls -t ~/pricing/*.json | sed -n 2p)
if [ -n "$PREV" ]; then
  jq -s '.[1] as $new | .[0] as $old |
    [$new[] | . as $n | $old[] | select(.name == $n.name) |
     {name, old_price: .price, new_price: $n.price,
      delta: ($n.price - .price)} | select(.delta != 0)]' \
    "$PREV" "$OUT" > ~/pricing/changes-$(date +%F).json
fi
```

## Best practices
- **Anchor high, discount down**: launch at the upper band; raising prices later costs customer trust.
- **Annual = 2 months free, not 20%**: simpler messaging, identical math, higher take-up.
- **Decoy tier engineering**: middle tier should have 70-80% of pro features at 40-50% price; this is where most users land. Design backwards from desired ARPU.
- **Re-price grandfathering**: explicit policy ("we honor your price for 12 months") builds trust; silent grandfather forever destroys margins.
- **Currency localization**: serve EUR/INR/BRL prices that aren't 1:1 USD — use PPP-adjusted bands. Agents routinely forget this.
- **Don't run Van Westendorp on cold leads**: they low-ball. Run on engaged trial users who hit the upgrade modal.
- **Sales-led "contact us" tier is a discount-control mechanism**, not a price — agents should mark it `negotiated` and exclude from median calcs.

## AI-agent gotchas
- Agents fabricate Van Westendorp distributions when given <30 real responses. Hard rule: refuse synthesis below N=30, return raw quotes only.
- Capture-rate suggestions cluster at 10-15% regardless of input. Override with category-specific priors (devtools 1-3%, productivity 5-10%, vertical SaaS 15-25%).
- Annual-discount math errors: agents will compute "12 × monthly × 0.83" instead of "10 × monthly". Force the formula in the prompt.
- LLMs default to 3-tier structure even when 2 or 5 fits better. Prompt: "consider 1, 2, 3, 4, and 5 tier alternatives; defend choice".
- **Human-in-loop checkpoint**: actual price commit is human. Agent output is "recommended bands"; pressing the button on Stripe is not delegated.
- Competitor extraction agents hallucinate features they expect to be in a tier. Always require `source_quote` per feature row.
- Currency, billing period, and seat-vs-flat pricing collapse into single-number outputs unless explicitly schema-constrained.

## References
- Patrick Campbell — "Pricing for Profit" (ProfitWell, free)
- Van Westendorp (1976) — "NSS Price Sensitivity Meter"
- Madhavan Ramanujam — "Monetizing Innovation"
- Tomasz Tunguz blog — SaaS pricing benchmarks
- OpenView — Annual SaaS Benchmarks Report
- Anthropic Claude Code WebFetch docs — https://docs.anthropic.com/en/docs/claude-code
