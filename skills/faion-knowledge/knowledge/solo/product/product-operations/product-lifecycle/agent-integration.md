# Agent Integration — Product Lifecycle Management

## When to use
- Annual planning: assess each product/SKU stage, reallocate investment.
- Multi-product portfolio (3+ products): one founder/PM can't intuit each stage; agent normalizes assessment.
- Pre-sunset decision: building a defensible "stage = decline" case before EOL announcement.
- Spinning out a product line: confirm growth-stage signals warrant independent team.
- Acquisition due diligence (target product): independent stage assessment vs. seller's claim.

## When NOT to use
- Single-product solo founder still hunting product-market fit — entire roadmap is "Introduction"; lifecycle framing adds no signal.
- Quarter-by-quarter operations — lifecycle changes on multi-quarter horizons; tactical decisions don't need this lens.
- Heavily-regulated products with mandated lifecycles (medical devices) — formal regulatory framework supersedes.

## Where it fails / limitations
- Stage assessment from short data windows is unreliable — 1-quarter dip ≠ Decline. Force ≥3 quarters of data.
- Adam Smith / Dean / Vernon-style classic curve fits physical goods better than digital subscription products with re-acceleration loops (PLG, AI-feature refresh).
- "Maturity" detection biased toward growth-rate deceleration; misses cases where TAM expanded silently.
- LLMs anchor on framework's defaults (20% YoY = growth, etc.) — your category may have different baselines (consumer apps: 100%+; B2B vertical: 30%).
- Sunset/decline often political: agents miss founder/team attachment that distorts data interpretation.

## Agentic workflow
Annual rhythm: (1) `lifecycle-assessor` agent ingests 8 quarters of metrics (revenue, growth, profitability, churn, NPS, market share if known) per product, computes stage with confidence band. (2) `strategy-fitter` agent maps current investments and activities to stage; flags mismatches (e.g. growth tactics on declining product). (3) `transition-planner` agent — when stage transition predicted, drafts capability changes needed (team, infra, metrics). (4) Quarterly: lighter `delta-checker` agent confirms or revises stage call from prior assessment. Critical: stage transition decisions are leadership; agent output is decision-support, not decision.

### Recommended subagents
- `lifecycle-assessor` — opus, judgment-heavy stage classification with explicit confidence + dissenting view.
- `strategy-fitter` — sonnet, current activities → stage-appropriate-or-not table.
- `transition-planner` — opus, strategic capability mapping for upcoming stage.
- `delta-checker` — haiku, quarterly diff against prior assessment.
- `mlp-impl-planner-agent` (existing in repo) — mid-life-product implementation planning.

### Prompt pattern
```
Product: {name}
Metrics (last 8 quarters):
  revenue: [...]
  growth_rate_yoy: [...]
  gross_margin: [...]
  net_revenue_retention: [...]
  new_logos: [...]
  churn: [...]
Category baselines (provided): growth_typical=X%, mature_typical=Y%
Output:
- assessed_stage: introduction/growth/maturity/decline
- confidence: high/medium/low + reasons
- alt_hypothesis: stage that would also fit + what would distinguish
- transition_signals: what would move us to next stage in 2-4 quarters
Refuse if data window <6 quarters.
```

```
Stage: {assessed_stage}
Current activities: {feature roadmap, marketing budget split, team count by function}
Output:
- aligned: [activities that match stage]
- misaligned: [activities better suited to other stage] with rationale
- missing: [activities the stage demands that aren't happening]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `chartjs-cli` / `vegacli` | Render lifecycle curves from CSV | npm |
| `metabase` / `evidence-dev` | Quarterly metric snapshots | OSS |
| `dbt` | Modeled metric layer (NRR, MRR cohorts) | `pip install dbt-core` |
| `claude` Skill tool | Drive sub-agents | https://docs.anthropic.com/en/docs/claude-code |
| `pandoc` + `mermaid-cli` | Generate annual lifecycle review report | system + npm |
| `csvkit` / `duckdb` | Multi-product cohort joins | system |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ProfitWell / Stripe Sigma | SaaS | Yes | MRR cohorts, churn, expansion — feed agent. |
| ChartMogul / Baremetrics | SaaS | Yes (REST) | Subscription-revenue metrics; lifecycle-friendly KPIs. |
| Metabase / Superset / Lightdash | OSS BI | Yes | Self-host dashboards agent reads via API. |
| Tableau / Looker | SaaS | Yes | Enterprise BI; semantic layers help agent consistency. |
| Crunchbase / PitchBook | SaaS | Limited | Competitor stage / funding signals. |
| Statista / IBIS | SaaS | WebFetch | Category baselines for "is 20% growth normal here?". |
| OpenView SaaS Benchmarks | Free annual | Read-only | Stage thresholds for SaaS subcategories. |
| Notion / Confluence | Doc tool | Yes | Persist lifecycle reviews + ADRs. |
| Roadmunk / ProductPlan | SaaS | Limited | Roadmap-by-stage; mostly UI-driven. |
| Reforge growth content | Paid | Read-only | Growth-loop frameworks beyond classic curve. |

## Templates & scripts
See `templates.md` for Lifecycle Assessment, Stage Strategy Guide. Multi-product runner:

```bash
#!/usr/bin/env bash
# annual-lifecycle.sh — one row per product, stage + strategy
set -euo pipefail
PRODUCTS=${1:?products.csv required}
OUT=~/lifecycle/$(date +%Y)
mkdir -p "$OUT"

while IFS=, read -r name dbt_model; do
  # 1. Pull 8q of metrics
  dbt run --select "$dbt_model" --vars "{quarters: 8}"
  duckdb -c ".read $dbt_model.sql; COPY (SELECT * FROM metrics)
             TO '$OUT/$name.json' (FORMAT JSON);"

  # 2. Stage assessment
  claude -p "$(cat ~/prompts/lifecycle-assess.txt)" \
    --input-file "$OUT/$name.json" > "$OUT/$name.stage.md"

  # 3. Strategy fit
  claude -p "$(cat ~/prompts/lifecycle-strategy.txt)" \
    --input-file "$OUT/$name.stage.md" > "$OUT/$name.strategy.md"
done < "$PRODUCTS"

# Portfolio rollup
cat "$OUT"/*.stage.md > "$OUT/portfolio.md"
```

## Best practices
- **Use ≥6 quarters of data** for stage calls; less is noise.
- **Pair classic curve with modern growth-loop framing** — Reforge's "growth loops" and "engagement curves" replace some lifecycle thinking for digital products.
- **Stage-appropriate KPIs**: Introduction → activation/NPS; Growth → CAC/LTV/growth-rate; Maturity → margin/NRR/churn; Decline → cash flow / migration rate.
- **Transition-planning starts a quarter before transition** — capability gaps (team mix, infra) take time to fill.
- **Sunset is a feature**: clear migration path + grace period > silent EOL. Plan customer comms.
- **Cross-product portfolio view**: don't optimize products in isolation; killing a maturity-stage product to fund a growth bet is sometimes right.
- **Stage call has alt-hypothesis discipline** — agent must articulate "what would I expect if I'm wrong about this stage?".
- **Re-evaluate after major external shift** (regulatory, platform, AI disruption) — normal rhythm is annual.

## AI-agent gotchas
- LLMs use round-number thresholds (20% / 10% / 0%) rigidly; your category baselines differ. Inject baselines explicitly.
- "Decline" is emotionally loaded — agents soften it ("plateau", "transition", "consolidation"). Force literal stage label.
- Re-acceleration after AI/PLG feature drop reads as "back to growth" — could be one-quarter blip; require sustained 2+ quarters.
- Multi-product agents conflate company stage with product stage; specify scope in prompt.
- Confidence calibration is poor — "High confidence" on 6q decline is real; "High confidence" on 2q dip is fiction. Mandate data-window in confidence reasoning.
- **Human-in-loop checkpoint**: actual stage-transition decision (kill, sunset, double-down) is leadership. Agent output never auto-publishes.
- Industry-normalization data is often paywalled (OpenView, ICONIQ); agent fabricates plausible benchmarks if not provided.
- Agents conflate market maturity with product maturity — your product can be in Introduction in a Mature market.

## References
- Theodore Levitt (1965) — "Exploit the Product Life Cycle" (HBR origin)
- Geoffrey Moore — "Crossing the Chasm" (introduction → growth boundary)
- Reforge — "Growth Loops" (modern alternative framing)
- Andrew Chen — "The Cold Start Problem"
- Lenny Rachitsky podcast — sunset case studies
- OpenView SaaS Benchmarks Report — annual category baselines
- "Inside the Tornado" — Geoffrey Moore (mainstream-to-mature transition)
