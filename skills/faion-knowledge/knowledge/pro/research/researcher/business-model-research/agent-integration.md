# Agent Integration — Business Model Research

## When to use
- Pre-spec phase: founder has a product idea but no defended monetization story; need to choose between SaaS / one-time / transaction / ad / marketplace before scoping the MVP.
- Pricing decision under uncertainty: ARPU, gross-margin, churn assumptions need to be modeled before a price page is shipped.
- Pivot review: existing product is missing LTV:CAC ≥ 3:1 and the founder must decide whether the model itself (not just the price) is broken.
- Investor memo / seed deck: section "How we make money" requires a Business Model Canvas + unit-economics page with stress tests.
- Multi-revenue-stream design: subscription + usage + marketplace fee blends — need a single Canvas that explains how streams interact and which dominates.
- Scenario planning before raising prices, opening a free tier, or adding usage caps.

## When NOT to use
- Internal tools, OSS side-projects, hobby apps with no intent to monetize.
- Already-shipping products with 12+ months of real ARR data — use cohort analysis (`aarrr-pirate-metrics`) instead of model speculation.
- Pure infrastructure libraries where revenue is a downstream consequence (the parent SaaS owns the model).
- Government/grant-funded work where the "customer" is a budget line, not a paying user.
- Two-sided marketplace pre-launch with zero supply — supply economics dominate; do `network-effects` and `marketplace-liquidity` first.
- Hardware/regulated products where margin is dictated by BOM + compliance, not chosen.

## Where it fails / limitations
- Garbage-in churn: agents accept a 1%/month churn assumption from a blog post; LTV explodes 5x and the model looks viable when it is not.
- Single-point estimates: ARPU $29, churn 3%, CAC $50 hides ranges. Without P10/P50/P90 the LTV:CAC is theatre.
- Reverse engineering: if the founder mentions "we want a $1B exit", the LLM reverse-fits margins and segment sizes to make the canvas close.
- Missing variable cost layer: gross margin treated as 80% by default (SaaS folklore) even when the product has 30% COGS (AI inference, payments, fulfillment).
- Ad model self-deception: $5 CPM × 100k DAU rarely materializes for niche content; agents skip the inventory-fill assumption.
- Marketplace take-rate fantasy: 20% take is assumed; real successful marketplaces sit at 5–15% (Etsy 6.5%, Airbnb 14%, Upwork 10%).
- Currency / billing drift: monthly vs annual ARPU mixed silently; LTV inflated by 12x.
- Static churn: assumed flat across the lifecycle; in reality month-1 churn is 3–10x month-12 churn.

## Agentic workflow
The agent loads README, locks the value chain, then runs three independent passes — Canvas fill, Revenue-model selection, Unit economics — in that order. Every assumption is tagged Hard (sourced from a comparable public company filing or pricing page) or Soft (founder estimate). The unit-economics block must be re-run with three scenarios (P10 pessimistic, P50 base, P90 optimistic) before any verdict line is written. Output is appended to `.aidocs/product_docs/business-model.md` and cross-referenced from `market-research.md` (TAM/SAM/SOM provides the SOM ceiling that revenue must respect).

Concrete pipeline:
1. Value chain map — agent diagrams `Suppliers → Product → Customers` with cost arrows; founder confirms before any price is named.
2. Revenue-model shortlist — pick 2 of the 5 archetypes (subscription, one-time, transaction, advertising, marketplace) that fit the value chain; reject the others on record.
3. Comparable harvesting — `WebSearch` 3–5 public competitors per shortlisted model; pull pricing pages, S-1/10-K if listed, churn/CAC from earnings calls.
4. Canvas fill — populate all 9 blocks from README template; mark each cell Hard/Soft.
5. Unit economics block — compute CAC, LTV, LTV:CAC, payback in P10/P50/P90.
6. Stress test — run the 5 tests from README (scale, competition, churn, CAC, time-to-profit); the model passes only if it survives all five at P50.
7. Verdict — one of {viable, viable-with-fixes, not-viable}; if not-viable, agent must propose 2 alternative models and re-loop step 2.
8. Validation pass — sibling `faion-product-manager-agent` re-reads against `checklist.md` and returns a delta list.

### Recommended subagents
- `faion-research-agent` — orchestrator, mode `business-model` dispatches this methodology.
- `faion-market-researcher-agent` — declared in README front-matter; methodology-aware Canvas + unit-economics agent.
- `faion-product-manager-agent` — validates the verdict against product roadmap and pricing decisions.
- `faion-domain-checker-agent` — pairs once a name + model are chosen, before any price page is built.
- General `web-research` / `WebSearch` subagent — pulls competitor pricing pages, S-1 filings, earnings calls.
- Sibling methodologies in `../`: `market-research-tam-sam-som`, `pricing-research`, `mvp-scoping`, `competitor-analysis`, `aarrr-pirate-metrics`.

### Prompt pattern
```
You are a business-model analyst. Build a Business Model Canvas + unit
economics for: <product idea>. Constraints: <ICP, geo, stage>.
Steps: (1) map value chain, (2) shortlist 2 of 5 revenue archetypes,
(3) pull 3 public comparables per archetype, (4) fill Canvas with
H/S tags per cell, (5) compute CAC/LTV/payback in P10/P50/P90,
(6) run all 5 stress tests, (7) emit verdict.
Refuse to average ranges. Cite source URL + retrieval date for every
Hard cell. Output: markdown matching templates.md sections.
```
```
Validate this business model: <paste canvas + unit economics>.
Check: (1) is gross margin sourced or assumed? (2) does churn vary by
cohort age? (3) does LTV:CAC survive at P10? (4) are revenue streams
additive or substitutive? (5) is payback < 12 months at P50?
Return delta list, not rewrite.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Pull competitor open-source repos for traction signal | `brew install gh` / cli.github.com |
| `crunchbase-api` | Funding stage, headcount, founded year for comparables | data.crunchbase.com/docs |
| `sec-edgar` (`python-sec-edgar`) | Public-company S-1/10-K — gold-standard ARPU, churn, CAC | github.com/jadchaar/sec-edgar-downloader |
| `simfin` | Financial filings as parsed CSV (free tier) | simfin.com |
| `yfinance` | Public market cap, revenue multiples for comparables | github.com/ranaroussi/yfinance |
| `pricing-page-scraper` (Playwright recipe) | Snapshot competitor pricing tiers | playwright.dev |
| `wayback-machine` (`waybackpack`) | Pin a pricing page on a specific date | github.com/jsvine/waybackpack |
| `numpy-financial` | NPV, IRR, payback period calculators | pypi.org/project/numpy-financial |
| `csvkit` + `pandoc` | Convert competitor pricing tables into the report template | csvkit.rtfd.io |
| `claude` (Anthropic CLI) | Run agent prompts above in batch | docs.anthropic.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| SEC EDGAR | Public filings | Yes — free API | Gold-standard for SaaS ARR, gross margin, churn |
| Crunchbase | Funding/competitor DB | Yes — REST API, key required | Stage + headcount for comps |
| PitchBook | Private market data | Partial — enterprise API | Better than Crunchbase for late-stage |
| ChartMogul | SaaS metrics SaaS | Yes — REST API | Plug-in for own data; benchmark API exists |
| ProfitWell / Paddle | Subscription metrics | Yes — REST API | Industry benchmark medians (free tier) |
| Stripe Atlas | Incorporation + payments | N/A | Reference pricing for transactional model fees |
| Baremetrics Open Benchmarks | SaaS benchmarks | Yes — public dataset | MRR/churn medians by ARPU band |
| OpenView SaaS Benchmarks | Annual report | No — PDF | Cite for usage-based pricing share |
| OPEXEngine | OPEX benchmarks | Paid | Cost-structure side of canvas |
| Apptopia / data.ai | Mobile app revenue | Paid REST API | Consumer-app revenue estimates |
| App Annie / Sensor Tower | Same | Paid | Use for one-time and freemium consumer apps |
| Strategyzer | Canvas tooling SaaS | Partial — no public API | Reference template only |
| Stripe Sigma / Atlas data | Aggregated SaaS data | Partial — login | Take-rate baselines for transactional models |
| Google Sheets / Notion | Canvas + math host | Yes — APIs | Where the agent writes the editable copy |

## Templates & scripts
See README sections "Business Model Canvas" and "Unit Economics Calculator" for the full templates. Inline LTV:CAC scenario helper:

```bash
#!/usr/bin/env bash
# unit-econ-scenarios.sh — emit P10 / P50 / P90 LTV:CAC and payback
# usage: ./unit-econ-scenarios.sh <arpu> <margin> <churn> <cac>
set -euo pipefail
arpu=$1; margin=$2; churn=$3; cac=$4
python3 - <<PY
arpu, margin, churn, cac = $arpu, $margin, $churn, $cac
def ltv(a, m, c): return a * m / c
def payback(c, a, m): return c / (a * m)
for label, mult in (("P10", 0.7), ("P50", 1.0), ("P90", 1.3)):
    a = arpu * mult
    c = churn * (2 - mult)        # worse churn in pessimistic
    cc = cac * (2 - mult)         # worse CAC in pessimistic
    L = ltv(a, margin, c)
    pb = payback(cc, a, margin)
    print(f"{label}: ARPU={a:.0f} churn={c:.3f} CAC={cc:.0f} "
          f"LTV={L:.0f} LTV:CAC={L/cc:.1f}:1 payback={pb:.1f}mo")
PY
```

Companion: keep the assumptions ledger as a CSV at `.aidocs/product_docs/business-model-assumptions.csv` with columns `cell,value,hard_soft,source_url,retrieval_date` so future re-runs can `git diff` and explain why the verdict moved.

## Best practices
- Lock the value chain in one diagram before any price is named — agents skip this step and produce numbers without context.
- Refuse to compute LTV with monthly churn under 1% unless backed by a public 10-K — sub-1% churn is a unicorn claim.
- Always compute LTV with a churn floor (e.g. cap lifetime at 60 months) — the formula `1/churn` explodes at low churn.
- Run unit economics in P10/P50/P90, not a single point — the verdict at P10 is the only one that matters for runway.
- Use gross margin from the comparable's 10-K, not "80% because SaaS" — AI-heavy products often run 30–50% due to inference cost.
- Distinguish CAC blended (all spend / all customers) from paid CAC (paid spend / paid customers); LTV:CAC must use paid CAC.
- For transactional models, model take-rate decay: marketplaces compress 1–2 points/year as suppliers gain leverage.
- For freemium, model conversion-rate floor at 2% (consumer) / 5% (B2B) — claims of 15% require evidence.
- Diversify revenue only if streams are non-substitutive (a community upsell on top of a course is good; two separate subscription tiers is one stream).
- Re-run the model every quarter against actuals; the assumption ledger surfaces which Soft cells are aging.
- Tag the model file as `version: vN` in front-matter and commit; pricing decisions reference the version, not the date.
- Cap Soft-cell compounding at 3 deep — `0.5 × 0.4 × 0.3 × 0.2 = 1.2%` is a fantasy, not a forecast.

## Integration with faion-net SDD
- Output lives at `.aidocs/product_docs/business-model.md`; assumption ledger at `.aidocs/product_docs/business-model-assumptions.csv`.
- Reads SOM from `market-research.md` as the revenue ceiling; refuses to publish if forecast revenue at year 3 > SOM.
- `roadmap.md` MRR/ARR targets must reference a Canvas version; bumps require a new model run and a delta entry.
- `pricing.md` (from `pricing-research`) inherits ARPU range from this methodology — keep the two in sync via the `researcher` orchestrator.
- `spec.md` lists revenue-affecting requirements (e.g. metering for usage-based) traced to a Canvas cell — `Key Activities` or `Revenue Streams`.
- When run via `/faion-net` mode `business-model`, agent appends a 1-page "Business Model" block to `executive-summary.md`.
- Tier gating: methodology is `pro/`; abort if the calling tier is `free`/`solo` instead of approximating with a simpler canvas.

## AI-agent gotchas
- LLMs default to SaaS subscription whenever the product is digital — force the agent to justify rejecting the other 4 archetypes, on record.
- Churn hallucination: model invents 2%/month "industry standard" without source — require a 10-K citation or a Baremetrics/ChartMogul benchmark URL.
- ARPU vs ARR confusion: agent mixes monthly and annual numbers within the same LTV calc; LTV is off by 12x and goes unnoticed.
- Currency mixing: USD pricing pages, EUR comps, GBP local — normalize at retrieval, not at report time.
- Compounding fractions: `freemium 5% × paid 80% retention × upgrade 20%` produces false precision; round each to one sig fig.
- Take-rate fantasy: agent assumes 30% take on a marketplace because the founder hinted at high margin; cap at 15% unless there is a moat.
- "We will charge what competitors charge": agent copies competitor pricing without checking unit economics; rerun with own COGS + CAC.
- Confirmation bias: founder mentions "we want $10M ARR by year 3" → agent reverse-engineers customer count and price to hit it; pre-commit Canvas before sharing the target.
- Static churn assumption: agent uses one churn number for all 36 months; cohort decay is 3–10x in month-1 vs month-12.
- Margin laziness: agent uses revenue as if it were profit; explicitly require a Cost Structure block before any LTV cell renders.
- Output drift: each rerun rewrites the entire Canvas; lock headings to README template, only fill cells, version the file.
- Tier-mismatch: agent tries to load `business-model-research` from `solo/` but it lives in `pro/` — fail loudly, do not approximate with a smaller canvas.

## References
- README (this directory) — primary canvas + unit economics templates.
- Sibling: `../../market-researcher/business-model-research/` (parallel copy under `market-researcher` skill); keep in sync via the `researcher` orchestrator.
- Related methodologies in this skill: `market-research-tam-sam-som`, `pricing-research`, `mvp-scoping`, `gtm-strategy`, `aarrr-pirate-metrics`, `competitor-analysis`.
- Strategyzer "Business Model Generation", Osterwalder & Pigneur — strategyzer.com/canvas
- a16z, "16 Startup Metrics" — a16z.com/2015/08/21/16-metrics
- David Skok, "SaaS Metrics 2.0" — forentrepreneurs.com/saas-metrics-2
- Tomasz Tunguz, SaaS benchmarks blog — tomtunguz.com
- ChartMogul SaaS Benchmarks — chartmogul.com/benchmarks
- ProfitWell / Paddle Studies — paddle.com/resources/saas-benchmarks
- OpenView SaaS Benchmarks Report — openviewpartners.com
- Baremetrics Open Benchmarks — baremetrics.com/open-benchmarks
- SEC EDGAR full-text — efts.sec.gov/LATEST/search-index
- Bill Gurley, "All Markets Are Not Created Equal" — abovethecrowd.com
- Andreessen Horowitz Marketplace 100 — a16z.com/marketplace-100
