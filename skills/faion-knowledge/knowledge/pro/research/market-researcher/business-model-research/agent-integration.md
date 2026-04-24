# Agent Integration — Business Model Research (Market-Researcher Lens)

> Sibling at `../../researcher/business-model-research/agent-integration.md` covers the founder/SDD lens.
> This file focuses on the **market-researcher** angle: peer benchmarking, industry revenue archetypes, and comparable-company analysis. Read both; do not duplicate.

## When to use
- Pre-spec **market-side** answer to "what model do peers in this category actually use?" — output is a benchmark table, not a single canvas.
- Investor/board memo: produce an industry revenue-model distribution (e.g. "67% subscription, 22% transaction, 11% hybrid in dev-tools <$50M ARR").
- Pricing committee input: pull P25/P50/P75 ARPU, gross margin, net revenue retention, and rule-of-40 from a public-comp set.
- Category entry decision: rank 5–15 candidate categories by median LTV:CAC and CAC payback; reject categories where the comp median fails.
- M&A scoping: build a comparable-companies (comps) table for a revenue multiple, mapping target's model to nearest public proxy.
- Trend monitoring: quarterly delta on take-rate compression, usage-based adoption, freemium conversion floors, ad CPM by vertical.
- Cross-checking a `researcher`-mode canvas — verify the founder's chosen archetype against industry base rates before SOM is locked.

## When NOT to use
- Single-product canvas + unit economics design — that is the `researcher` sibling's scope; do not duplicate it here.
- Markets with <3 public or well-documented private comparables — the benchmark table is statistically meaningless; switch to `expert-interviews` or `analogous-markets`.
- Hyper-local services (regional plumbing software, single-city marketplaces) — public comps don't transfer; use `local-market-survey` instead.
- Pre-revenue categories with no precedent (frontier AI, novel hardware) — peer benchmarking is misleading; use `analogous-markets` or `first-principles-pricing`.
- Internal pricing experiments where the answer must come from your own data, not industry medians.
- Regulated verticals (healthtech reimbursement, fintech BaaS) where revenue model is dictated by law, not chosen — research the regulation, not the comps.

## Where it fails / limitations
- **Survivorship bias**: comp set is built from listed/funded companies; failed peers are invisible, so medians look healthier than reality. Force inclusion of acquihires + shutdowns.
- **Definition drift across filings**: "ARR", "subscription revenue", "recurring revenue" are not the same line item in every 10-K. Median ARPU comparisons silently mix three different denominators.
- **Aged data**: SaaS benchmark reports lag 12–18 months; in 2024–2026 usage-based pricing share moved fast and any pre-2024 median is stale.
- **Private vs public premium**: public SaaS comps run higher gross margin (78–82%) than venture-stage privates (60–70%) because of scale; do not transplant the median onto a $2M ARR target.
- **Geographic blending**: US-listed comps dominate; EU/APAC/LATAM peers price 30–50% lower for the same value. Cohort by region or the median lies.
- **Take-rate fantasy in marketplaces**: surface take-rate (Etsy 6.5%) ignores ads + payments + subscription "all-in" revenue; the real take is 13–18%. Always compute all-in.
- **Freemium conversion claims**: companies cite "20% conversion" by counting only activated users; system-wide it's 1–4%. Always normalize on signups, not "qualified" users.
- **Net dollar retention is a vanity metric**: NDR > 110% can hide gross logo churn > 25%. Pair NDR with gross retention or reject the row.
- **Ad CPM extrapolation**: programmatic display CPMs are vertical- and audience-specific; "industry average $5 CPM" is meaningless at the comp level.
- **Currency normalization**: pricing pages mix USD/EUR/GBP/local; non-USD comps must be converted at the **filing-period** FX rate, not today's.

## Agentic workflow
The market-researcher agent treats this methodology as a **benchmarking pipeline**, not a canvas exercise. The founder's product is one data point in a comp set; output is the **distribution**, not a verdict on the founder's idea (the `researcher` sibling owns that). The pipeline runs: (1) define comp universe, (2) classify each comp into 1 of 5 archetypes (subscription/one-time/transaction/advertising/marketplace) plus hybrid flag, (3) extract revenue & retention metrics from filings/pricing pages, (4) emit a benchmark table with P25/P50/P75 per archetype, (5) flag the founder's plan against the distribution and call out where it's >1σ from the median.

Concrete pipeline:
1. **Universe definition** — 8–15 comparables per category, mixing public (filings), late-stage private (Crunchbase + press), acquired (M&A press), and dead (Crunchbase "Closed"). Reject set <8 or survivorship-skewed.
2. **Archetype classification** — agent labels each comp with its **dominant** revenue stream (>60% of revenue) plus secondary streams. Hybrid models (e.g. Shopify subs + payments take) are tagged with split.
3. **Metric harvest** — pull from S-1/10-K/proxy: ARPU/ARR-per-customer, gross margin, gross logo retention, net dollar retention, CAC payback, rule-of-40, take-rate (if marketplace), ad CPM × inventory fill (if ad). Use Wayback for snapshot pricing pages on the filing date.
4. **Normalization** — convert to USD at filing-period FX, annualize monthly numbers, strip one-time line items, separate subscription from services revenue.
5. **Distribution build** — P25/P50/P75 per archetype × per stage (seed/series-B/listed). Output a table, never a single number.
6. **Anomaly tagging** — comps >2σ from median get a footnote (e.g. Snowflake gross margin = 70% vs SaaS median 78% because of compute COGS).
7. **Founder overlay** — the founder's planned ARPU/margin/CAC overlaid on the distribution; cells flagged green (within P25–P75), yellow (P10–P25 / P75–P90), red (outside P10–P90).
8. **Trend annotation** — last 4–8 quarters delta per metric (e.g. "usage-based share moved from 20% → 38% of new ARR in dev-tools cohort 2022–2025").
9. **Hand-off** — output `.aidocs/product_docs/business-model-benchmarks.md` + `business-model-comps.csv`. Sibling `researcher/business-model-research` consumes the table to constrain canvas assumptions.

### Recommended subagents
- `faion-market-researcher-agent` — primary; declared in README front-matter.
- `faion-research-agent` — orchestrator (mode `business-model` for benchmarking subset).
- `faion-competitive-intel-agent` — provides the comp list from `competitor-analysis` outputs.
- `faion-pricing-research-agent` — consumes the ARPU/tier benchmarks for `pricing-research`.
- `web-research` / `WebSearch` subagent — pulls S-1/10-K, IR decks, press releases, Wayback pricing snapshots.
- `data-cleaner` (project-local) — normalizes currency, period, line-item definitions across filings.
- Sibling under `researcher/`: `business-model-research` (canvas + verdict).
- Sibling here under `market-researcher/`: `pricing-research`, `competitor-analysis`, `market-research-tam-sam-som`, `trend-analysis`.

### Prompt pattern
```
You are a market-research analyst. Build a business-model benchmark table for
the <category> at the <stage> tier (e.g. "vertical SaaS, $5–50M ARR").
Steps: (1) assemble 8–15 comparables (≥2 dead/acquihired), (2) classify each
into 1 of 5 archetypes + hybrid flag, (3) harvest ARPU, gross margin, gross
logo retention, NDR, CAC payback, rule-of-40 from S-1/10-K/IR (cite URL +
filing period), (4) normalize to USD at filing-period FX, (5) emit P25/P50/
P75 per archetype, (6) flag comps >2σ with cause (e.g. compute COGS).
Refuse to publish if comp set < 8 or all comps are listed (survivorship).
Output: markdown table + companion CSV.
```
```
Overlay this product plan on the benchmark: ARPU=$<X>, gross-margin=<Y>%,
gross-retention=<Z>%, CAC-payback=<N> months. Mark each cell green/yellow/
red against the P25/P50/P75 in the comp distribution. List the 3 cells most
out-of-band and the source of the discrepancy (model choice vs stage vs
geography). Do not rewrite the founder's plan; emit a delta only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `sec-edgar-downloader` | Bulk-pull S-1/10-K/10-Q for comp set | github.com/jadchaar/sec-edgar-downloader |
| `edgar-tools` (`uv add edgar`) | Parse XBRL line items into pandas | github.com/dgunning/edgartools |
| `simfin` | Pre-parsed financials CSV (free tier) | simfin.com/data/access/api |
| `yfinance` | Market cap, revenue multiples, comp ratios | github.com/ranaroussi/yfinance |
| `crunchbase-api` | Private comps (funding, headcount, status) | data.crunchbase.com/docs |
| `pitchbook` (paid) | Late-stage private + acquihires | pitchbook.com/data |
| `waybackpack` | Snapshot competitor pricing pages on filing date | github.com/jsvine/waybackpack |
| `playwright` | Scrape live pricing tiers, plan limits, usage caps | playwright.dev |
| `currencylayer` / `exchangerate.host` | FX normalization at filing period | exchangerate.host |
| `pandas` + `numpy-financial` | Distribution stats, IRR, payback | pandas.pydata.org |
| `csvkit` + `pandoc` | Comps CSV → markdown report | csvkit.rtfd.io |
| `gh` (GitHub CLI) | Pull OSS comps' GitHub stars/forks as adoption proxy | cli.github.com |
| `whois` / `dnstwist` | Domain age + brand-protection signal for comp set | github.com/elceef/dnstwist |
| `claude` (Anthropic CLI) | Run benchmark prompts in batch over the comp list | docs.anthropic.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| SEC EDGAR | Public filings | Yes — free API, no key | Gold-standard ARR, GM, NDR, CAC payback |
| Crunchbase | Private comp DB | Yes — REST API, key required | Use for stage, funding, status (closed/acquired) |
| PitchBook | Private market + M&A | Partial — enterprise API | Better than Crunchbase post-Series-B |
| CB Insights | Trends + comp lists | Partial — paid | Use for category-level adoption curves |
| Tracxn | Private comp DB | Yes — REST API | Cheaper than PitchBook for emerging-market comps |
| Capital IQ / FactSet | Comps + M&A | Enterprise only | Investment-banker grade comp tables |
| ChartMogul Benchmarks | SaaS metrics medians | Yes — REST + public charts | Free benchmark dataset by ARPU band |
| Baremetrics Open Benchmarks | SaaS medians | Yes — public dataset | MRR/churn medians |
| ProfitWell / Paddle Benchmarks | SaaS medians | Yes — public + REST | Industry medians by ARPU band |
| OpenView SaaS Benchmarks Report | Annual + bi-annual | No — PDF | Cite for usage-based share |
| Bessemer Cloud Index | Listed-cloud comp basket | Yes — public | Multiples + rule-of-40 medians |
| Meritech Public Comps | Listed-cloud comp basket | Yes — public web | Live valuation comps |
| Battery Open OPEX | OPEX benchmarks | Public PDF | Cost-structure side of canvas |
| OPEXEngine | OPEX benchmarks | Paid | More granular than Battery |
| App Annie / data.ai | Mobile revenue comps | Paid REST API | Consumer apps + freemium conversion |
| Sensor Tower | Mobile revenue + LTV | Paid REST API | Same as data.ai with different methodology |
| Apptopia | Mobile revenue | Paid REST API | Triangulate with Sensor Tower |
| Stripe Atlas Index | Aggregated SaaS data | Partial — public posts | Take-rate, payment-mix baselines |
| Marketplace 100 (a16z) | Marketplace comps | Yes — public | Take-rate evolution by category |
| StatShot / SaaStr | Conference benchmark talks | Public videos/decks | Cite for qualitative trend signals |

## Templates & scripts
See README sections for the canvas + per-comp unit-economics template. Keep this folder's deliverable as a **comps table + distribution table**. Inline benchmark-distribution helper:

```bash
#!/usr/bin/env bash
# bm-distribution.sh — emit P25/P50/P75 per archetype from comps.csv
# usage: ./bm-distribution.sh comps.csv
# csv columns: name,archetype,arpu_usd,gross_margin,gross_retention,ndr,cac_payback_mo
set -euo pipefail
csv=${1:?path to comps.csv}
python3 - <<PY
import pandas as pd
df = pd.read_csv("$csv")
metrics = ["arpu_usd","gross_margin","gross_retention","ndr","cac_payback_mo"]
out = (df.groupby("archetype")[metrics]
         .quantile([0.25,0.5,0.75])
         .unstack(level=-1).round(2))
out.columns = [f"{m}_{int(q*100)}" for m,q in out.columns]
print(out.to_markdown())
n = df.groupby("archetype").size().to_dict()
print("\nN per archetype:", n)
small = [k for k,v in n.items() if v < 3]
if small: print("WARNING: archetype N<3 (unreliable):", small)
PY
```

Companion: persist the comp list as `.aidocs/product_docs/business-model-comps.csv` with columns `name,archetype,stage,geo,arpu_usd,gross_margin,gross_retention,ndr,cac_payback_mo,source_url,filing_period,fx_rate,status`. `git diff` of this file across quarters shows trend drift — feed it to `trend-analysis`.

## Best practices
- Build the comp set **before** classifying the founder's idea — anchoring on the founder's preferred archetype biases the universe selection.
- Always include 2+ failed/acquihired peers; without them medians overstate viability by 20–40%.
- Tag every metric with `source_url` + `filing_period` (YYYY-Qn); benchmarks without provenance are unreviewable.
- Quote distribution (P25/P50/P75), never single medians — single numbers create false precision.
- Cohort by stage (seed/B/listed) and geo (US/EU/RoW) before computing medians; cross-stage averages are noise.
- Compute **all-in take-rate** for marketplaces (subscription + payments + ads), not just commission — cheats the headline by 5–10 points.
- Normalize ARR vs ARPU vs ACV explicitly in a glossary at the top of the report; agents (and humans) confuse the three.
- Convert non-USD at filing-period FX, not today's; year-old EUR comps compared at today's rate distort 5–15%.
- Cap any single comp's weight at 1/N — 1 dominant peer in a 5-comp set is no longer a benchmark, it's a copy.
- For freemium conversion: report on **signups**, not on "qualified leads" — comp self-reporting inflates conversion 3–10x.
- Re-run the benchmark every 2 quarters; flag any P50 metric that shifts >10% as a "regime change" warrant for `trend-analysis`.
- When the comp set is <8, downgrade output from "benchmark" to "case studies" — a 3-comp table is anecdote, not data.

## Integration with faion-net SDD
- Output lives at `.aidocs/product_docs/business-model-benchmarks.md` (table) + `business-model-comps.csv` (raw comp data).
- Feeds `pricing-research` (ARPU bands), `competitor-analysis` (archetype map), `market-research.md` (revenue ceiling cross-check).
- Sibling `researcher/business-model-research/` consumes the benchmark table; founder's canvas cells are validated against P25–P75.
- Hand-off contract: this methodology produces **distributions**; the `researcher` sibling produces a **single canvas**. Never invert.
- `roadmap.md` ARR targets: must reference a benchmark version + filing-period cohort (so "$10M ARR by Y3" is judged against medians of the right stage).
- Tier gating: this methodology is `pro/`; abort if calling tier is `free`/`solo` instead of approximating.

## AI-agent gotchas
- **Survivorship bias auto-pilot**: agents default to public-listed comps because filings are easiest to scrape; force ≥20% private + ≥10% dead in the universe.
- **ARR / ARPU / ACV mix-up**: agent reads "annualized recurring revenue" as ARPU; LTV explodes 50–500x. Require a glossary block before any number.
- **Filing-period drift**: comp A reports FY24, comp B reports calendar Q3 2025; medians mix periods silently. Force same-period cohorting or annotate the lag.
- **Currency at report-time, not filing-time**: FX move in 2022–2024 distorts EUR/GBP comps; normalize at filing-period FX, not today's.
- **One-time line items in the ARR**: agent counts professional-services revenue as recurring; subscription mix overstated by 10–25%.
- **Hybrid model squashing**: agent forces Shopify into "subscription" but >60% of its revenue is payments + ads; tag hybrid + split, never collapse.
- **Take-rate misread**: agent reports headline commission but comp also charges seller subscriptions + payment fees; report all-in.
- **NDR cherry-pick**: agent quotes NDR without gross logo retention; small-base NDR is noise. Always pair.
- **Stage blending**: agent averages a seed-stage Crunchbase pricing page with a listed 10-K; cohort by stage or reject.
- **Single-comp dominance**: 80% of the median is driven by one giant comp (e.g. Salesforce in horizontal SaaS); cap weight or the median is that one comp.
- **Wayback miss**: pricing pages change between filings; agent quotes a page newer than the filing period. Pin via Wayback to the filing month.
- **Trend extrapolation**: 2-point trend ("usage-based went 20%→38%, will hit 60%") is fantasy at <8 quarters of data.
- **Definition mismatch with the `researcher` sibling**: agent here writes a verdict; that's out of scope. Distributions in / canvas out at the sibling.

## References
- Sibling: `../../researcher/business-model-research/agent-integration.md` — canvas + unit economics lens (founder-side).
- Related in this skill: `pricing-research`, `competitor-analysis`, `market-research-tam-sam-som`, `trend-analysis`, `niche-evaluation`.
- SEC EDGAR full-text search — efts.sec.gov/LATEST/search-index
- Bessemer Cloud Index — bvp.com/cloud-index
- Meritech Public Comps — meritechcapital.com/public-comparables
- ChartMogul SaaS Benchmarks — chartmogul.com/benchmarks
- Baremetrics Open Benchmarks — baremetrics.com/open-benchmarks
- ProfitWell / Paddle Benchmarks — paddle.com/resources/saas-benchmarks
- OpenView SaaS Benchmarks Report — openviewpartners.com
- a16z Marketplace 100 — a16z.com/marketplace-100
- Bill Gurley, "All Markets Are Not Created Equal" — abovethecrowd.com
- David Skok, "SaaS Metrics 2.0" — forentrepreneurs.com/saas-metrics-2
- Tomasz Tunguz SaaS benchmarks — tomtunguz.com
- Battery Ventures OPEX Benchmarks — battery.com/oppex
- Andreessen Horowitz "16 Startup Metrics" — a16z.com/2015/08/21/16-metrics
