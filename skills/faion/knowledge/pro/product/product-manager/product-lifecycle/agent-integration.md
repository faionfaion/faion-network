# Agent Integration — Product Lifecycle Management

## When to use
- Quarterly portfolio review where the PM/CPO must decide investment level for each shipped product (faion-net portfolio: nero, neromedia, pashtelka, longlife, ender, mediamanager, scanmecard, eulaguard) and explicitly stop spending growth budget on maturity / decline assets.
- A product hits a metrics inflection — growth slows from 30% YoY to 8%, churn jumps, or a new technology shift threatens the core — and leadership needs a structured stage reassessment, not a gut call.
- Pre-roadmap step: tag every product in the portfolio with its stage (Intro / Growth / Maturity / Decline) before sequencing the year, so resource allocation matches the stage rubric (Intro = lean MVP, Growth = scale, Maturity = optimize, Decline = harvest / sunset).
- End-of-life decision: a product has been declining ≥ 3 quarters and the org needs an explicit sunset plan with migration timeline, support budget taper, and customer communication schedule.
- Investor / board update: defending why a maturity-stage product gets retention budget instead of new features, or why a decline-stage product is being wound down rather than re-platformed.
- Stage transitions: explicit checkpoint when an Intro product hits PMF and must shift from "learn fast" tooling to "scale" tooling — failing this transition is the #1 reason post-PMF SaaS startups stall.

## When NOT to use
- Pre-PMF startup with one product still hunting for fit — there is no "lifecycle" yet, only a discovery loop. Use `continuous-discovery` and `opportunity-solution-trees` instead.
- Sub-feature decisions inside one product (which feature to build next) — RICE / WSJF / MoSCoW are sharper at that grain. PLC is a portfolio-level lens, not a backlog-item lens.
- Pure B2B services / agency revenue where there is no productized asset to age — lifecycle math is undefined.
- Internal tools / platforms with no external customers — they have a usefulness curve, not a revenue curve. Use technical-debt-management instead.
- Crisis weeks (P0 outage, security incident, regulator letter) — survival comes first, restore lifecycle planning after.

## Where it fails / limitations
- The classic 4-stage curve is a 1960s consumer-goods abstraction. SaaS / agentic-AI products do not follow a smooth bell — they often plateau, dip, recover, plateau again. Treating the curve as deterministic produces premature sunsets.
- Stage labels are political: nobody wants to admit their product is in Decline; teams lobby for "late Maturity" indefinitely. Without a neutral arbiter and an evidence rubric, classifications drift toward optimism.
- Single-metric staging (revenue YoY only) misclassifies network-effect products (low revenue but high engagement = still Growth) and bundling products (revenue stable, but value is in a different SKU).
- "Decline" is often a category-decline misread: the underlying need is shifting (e.g. desktop → mobile, on-prem → cloud, search → agentic). The product can be revived by re-platforming, but the lifecycle frame says "harvest" — wrong call.
- LLMs over-classify products as Growth because product copy and roadmaps emphasize new features. They under-classify Maturity because "stable" sounds boring. Counter with a numeric rubric tied to actual MRR / churn / cohort data.
- Stage transitions are *not* one-way. A Maturity product can re-enter Growth via a new segment, new pricing tier, or a 10x feature unlock. Pure stage models miss this; treat transitions as bidirectional.
- The framework gives no guidance on how long a stage "should" last — agents will hallucinate timelines. Real durations vary 10x across categories (consumer apps: 1–3y per stage; enterprise infra: 5–15y).

## Agentic workflow
Drive PLC in three passes. **Pass 1 — assess**: a sonnet-class agent ingests last 4–8 quarters of metrics per product (MRR, growth rate, gross margin, NPS, churn, market share if available) and outputs a structured stage classification with confidence and rationale. **Pass 2 — strategy fit**: an opus-class agent compares actual investment mix (% eng cost on acquisition vs. retention vs. optimization vs. sunset) against the stage-appropriate strategy from the rubric, and emits a list of misalignments ("growth-tactic-applied-to-decline" or "maturity-investment-in-intro-product"). **Pass 3 — transition planning**: for any product near a stage boundary, run `faion-brainstorm` with stakeholders to surface trigger metrics and pre-commit decisions ("if churn > 7% for 2 quarters, declare Decline and start sunset"). All three passes must produce structured JSON so a human reviewer (or the `faion-sdd-executor-agent`) can audit and act, not prose.

### Recommended subagents
- `faion-mlp-impl-planner-agent` — referenced in this methodology's metadata; use it during the Intro→Growth transition to plan the post-MVP scope expansion (MLP = Minimum Lovable Product).
- `faion-sdd-executor-agent` — once a stage strategy is approved, drive the resulting initiatives through SDD (Growth: full SDD per feature; Decline: lightweight maintenance specs only).
- `faion-brainstorm` — diverge / converge on what triggers a stage transition, or on revival options for a product trending toward Decline (re-platform vs. sunset vs. spin-out).
- `faion-improver` — quarterly review loop: read last quarter's stage assessments, compare predicted vs. actual transitions, log mistakes (e.g. "called nero Growth, was actually late Intro"), feed into next quarter's rubric.
- A custom `lifecycle-classifier` subagent (worth creating, ~30 lines): input = `{product_id, mrr_series, growth_rate, churn, gross_margin, competitor_count}`, output = `{stage, confidence, rationale, transition_risk}`. Stateless, cheap, runs on every product weekly.

### Prompt pattern
```
You are a product lifecycle classifier. Output JSON only.
Schema: {stage: "intro"|"growth"|"maturity"|"decline",
         confidence: 0-1, rationale: <=200 chars,
         transition_signal: null | "intro->growth" | "growth->maturity" | "maturity->decline" | "decline->sunset"}
Rubric (require evidence; default to maturity if signals conflict):
  intro    = MRR < $10k OR growth > 50% YoY AND profitability negative AND <12mo since launch
  growth   = growth >= 20% YoY for 2+ quarters AND profitability improving AND competition increasing
  maturity = growth < 15% YoY AND profitability peak AND saturated market signals
  decline  = growth < 0 for 2+ quarters AND customer migration evidence
Inputs: <paste product metrics block>
```

```
You are a stage-strategy auditor. Given {stage} and {investment_mix:
acquisition_pct, retention_pct, optimization_pct, sunset_pct}, compare against
the rubric:
  intro    -> 70%+ on iteration/PMF, 0% sunset
  growth   -> 60%+ acquisition, <20% optimization, 0% sunset
  maturity -> 50%+ retention+optimization, <30% acquisition
  decline  -> 60%+ optimization+sunset, 0% new acquisition
Output JSON: {misaligned: bool, flags: [str], recommended_shift: {area, delta_pp}}
Do not invent metrics; if a field is missing, return misaligned=true with reason="insufficient_data".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stripe` CLI + Sigma SQL | Pull MRR / churn / cohort retention per product to feed the classifier | https://stripe.com/docs/stripe-cli |
| `chargebee` / `recurly` CLI / API | Same data for non-Stripe billing stacks | https://apidocs.chargebee.com |
| `posthog` (`posthog-cli`, REST) | Engagement and retention metrics for free / freemium tiers where Stripe is empty | https://posthog.com/docs/api |
| `mixpanel` Query API | Cohort retention and stage-graduation funnels | https://developer.mixpanel.com |
| `linear` / `productboard` API | Read backlog tags per product to compute investment-mix percentages | https://developers.linear.app |
| `gh` (GitHub CLI) | `gh repo list` + commit volume per repo as a proxy for active investment per product | https://cli.github.com |
| `pandas` + `matplotlib` / `plotly` | Local lifecycle curve plot from a CSV of quarterly MRR | `pip install pandas plotly` |
| `claude` CLI (Claude Code) | Drive the classifier subagent on a JSON metrics file, emit JSON to stdout | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ChartMogul | SaaS | Yes (REST) | Best-in-class SaaS metrics; native MRR, churn, LTV per product/segment |
| Baremetrics | SaaS | Yes (REST) | Cheaper alternative; strong cohort + retention views agents can pull |
| ProfitWell / Paddle Billing | SaaS | Yes (REST) | Free MRR analytics tier; pricing-tier moves often coincide with stage transitions |
| Productboard | SaaS | Yes (REST + webhooks) | Roadmap items tagged by stage; good source for investment-mix audit |
| Aha! Roadmaps | SaaS | Partial (REST, rate-limited) | Strong portfolio + lifecycle module; bulk writes slow |
| Mixpanel / Amplitude | SaaS | Yes (REST + SQL) | Engagement-based stage signals (DAU/MAU plateau = maturity hint) |
| Pendo | SaaS | Yes (REST) | Adoption metrics for B2B SaaS; good for late-Growth / Maturity boundary |
| Looker / Metabase / Cube | SaaS / OSS | Yes (SQL) | Self-hosted dashboards if metrics live in your warehouse |
| `dbt` + Postgres / DuckDB | OSS | Yes (file + SQL) | Reproducible quarterly snapshot pipeline; agents read parquet output |

## Templates & scripts

See `templates.md` for the Lifecycle Assessment and Stage Strategy Guide markdown forms. Inline below: a script that consumes a quarterly MRR CSV per product and emits a draft stage classification (rule-based, no LLM) so the classifier subagent only handles ambiguous cases.

```bash
#!/usr/bin/env bash
# stage-suggest.sh — first-pass lifecycle stage from MRR CSV
# Usage: ./stage-suggest.sh products.csv
# CSV cols: product_id,quarter,mrr_usd,churn_pct,gross_margin_pct
set -euo pipefail
CSV="${1:?products.csv required}"
python3 - "$CSV" <<'PY'
import csv, sys, collections, statistics
rows = list(csv.DictReader(open(sys.argv[1])))
by = collections.defaultdict(list)
for r in rows:
    by[r["product_id"]].append(r)
for pid, series in by.items():
    series.sort(key=lambda r: r["quarter"])
    if len(series) < 4:
        print(f"{pid}\tintro\t0.5\tinsufficient_history"); continue
    mrr = [float(r["mrr_usd"]) for r in series]
    churn = statistics.mean(float(r["churn_pct"]) for r in series[-2:])
    yoy = (mrr[-1] - mrr[-5]) / mrr[-5] * 100 if len(mrr) >= 5 and mrr[-5] > 0 else None
    last_q_growth = (mrr[-1] - mrr[-2]) / mrr[-2] * 100 if mrr[-2] > 0 else 0
    if mrr[-1] < 10000 and yoy is None:
        stage, conf, why = "intro", 0.7, "low_mrr_short_history"
    elif yoy is not None and yoy >= 20 and last_q_growth > 0:
        stage, conf, why = "growth", 0.8, f"yoy={yoy:.0f}%"
    elif yoy is not None and 0 <= yoy < 15 and churn < 5:
        stage, conf, why = "maturity", 0.7, f"yoy={yoy:.0f}% churn={churn:.1f}%"
    elif yoy is not None and yoy < 0:
        stage, conf, why = "decline", 0.8, f"yoy={yoy:.0f}%"
    else:
        stage, conf, why = "maturity", 0.4, "ambiguous_send_to_llm"
    print(f"{pid}\t{stage}\t{conf}\t{why}")
PY
```

Pipe ambiguous rows (`conf < 0.5`) into the classifier prompt above for an LLM second opinion.

## Best practices
- Anchor every stage label to **at least two evidence sources** (e.g. MRR series + cohort retention, or growth rate + competitor count). Single-metric staging is the #1 cause of misclassification.
- Re-classify quarterly. SaaS stage transitions can happen in 2 quarters; annual reviews miss them and you spend a year applying the wrong strategy.
- Track investment by **engineering cost in $ or person-weeks per area** (acquisition / retention / optimization / sunset), not by ticket count. A 1-line retention fix and a 6-month new-acquisition feature both count as "1 ticket" and that destroys the audit.
- Pre-commit **kill / sunset thresholds** when entering Maturity, not when entering Decline. By the time Decline is obvious, you have already over-invested. Example: "if MRR YoY < 0 for 3 consecutive quarters, automatic sunset review."
- Use a separate revival vs. sunset decision tree on Decline products. Default-to-sunset is expensive when the underlying need still exists — sometimes a re-platform recovers a Maturity-equivalent for 20% of new-product cost.
- Distinguish **product Decline** from **category Decline**. A product can decline because the category shifts (desktop email clients) or because a competitor leapfrogged (Slack vs. HipChat). The strategic response differs: re-platform vs. fast sunset.
- Pair lifecycle review with **technical-debt-management**. Maturity-stage products with high tech debt are 3x more likely to false-Decline because feature velocity drops to zero before customers leave.
- Document stage transitions in a portfolio decisions log (`.product/decisions/`). The history is the single most useful input to next year's classifier.

## AI-agent gotchas
- LLMs anchor heavily on roadmap copy and recent feature announcements; they will tag any actively-developed product as Growth even when MRR is flat. Force the classifier to require numeric MRR series; refuse if missing.
- Without an explicit `gross_margin` and `churn` field, agents conflate Growth and late Intro. Validate input schema before classifying.
- The "Decline" label is reputationally costly internally — agents tuned on internal docs will systematically avoid it. Counter with an unambiguous numeric rubric (`yoy < 0 for 2+ quarters AND churn > 7%` → decline) and an instruction to ignore prose framing.
- Stage transitions tagged by an agent are NOT decisions — they are recommendations. Always require human sign-off before changing investment mix, especially before declaring Decline (which triggers customer-facing communication and team-morale impact).
- Quarterly drift detection is mechanical — automate it (cron + the script above) and only escalate when a product's stage classification flips OR when investment mix drifts > 10pp from the stage rubric.
- Sunset plans must NOT be agent-authored end-to-end. Customers, contracts, regulatory disclosure, and team transitions all require human judgment. Use the agent for the metric trigger and the draft timeline only.
- When metrics sources disagree (Stripe says churn=4%, ChartMogul says churn=7%), trust the system that defines the canonical revenue contract (usually Stripe / billing), not the analytics overlay.
- The 4-stage rubric is a heuristic, not a law. Allow the classifier to return `stage="ambiguous"` with reasons; do not force every product into a bucket. Forcing produces wrong strategy 100% of the time on hybrid products (e.g. a Maturity core + a Growth add-on SKU).

## References
- Theodore Levitt, "Exploit the Product Life Cycle" (HBR, 1965) — original 4-stage model.
- Geoffrey Moore, "Crossing the Chasm" (3rd ed., 2014) — Intro→Growth transition mechanics for tech products.
- Marty Cagan, "Empowered" (2020) — chapters on portfolio and product strategy across stages.
- Reforge, "Product Lifecycle for SaaS" essays (2022–2024) — modern critique of the classic curve.
- Ben Horowitz, "The Hard Thing About Hard Things" — Decline / sunset chapters.
- ChartMogul — "SaaS Metrics Refresher" docs: https://chartmogul.com/blog/saas-metrics-refresher
- Stripe Atlas guides on cohort retention and stage signals: https://stripe.com/atlas/guides
- Productboard, "Portfolio Management" docs: https://www.productboard.com/glossary
