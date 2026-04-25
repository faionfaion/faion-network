# Agent Integration — Funnel Optimization Examples & Benchmarks

## When to use
- Anchoring "is our X% conversion good?" against industry benchmarks (SaaS / Ecom / Mobile / B2B / Email).
- Pattern-matching a current funnel shape to one of the README's five worked examples and lifting the proven optimization sequence.
- Producing executive narratives that contextualize current rates against the "Good" and "Great" bands per stage.
- Briefing a new agent or analyst with shape-of-funnel context before diagnosis work begins.

## When NOT to use
- Process or framework decisions (route to `funnel-basics-framework`).
- Tactics shopping (route to `funnel-tactics-basics` or `-advanced`).
- PLG strategy (route to `plg-basics`).
- Single-product, low-traffic situations where benchmarks are statistically meaningless.

## Where it fails / limitations
- Benchmarks are aggregate; subverticals and ICPs deviate substantially. SaaS "Visitor → Signup 2–5%" can be 0.5% (enterprise self-serve) or 15% (consumer SaaS).
- The five worked examples are illustrative — agents must NOT copy the optimization sequence verbatim; root cause varies.
- Numeric percentages (e.g., "+25% signup rate") are point estimates from past tests; they have wide confidence intervals.
- Benchmarks predate any platform-specific shifts (iOS privacy changes, AI-search traffic dilution); some categories (mobile install → open) shift > 10% YoY.
- Email benchmarks are global averages; deliverability + segmentation effects dominate the listed bands.

## Agentic workflow
A benchmarks agent is a read-only retriever. Orchestrator passes (industry, stage, current rate, ICP optional). The subagent matches the industry table, returns Good/Great/current bucket, and surfaces the closest worked example with its proven optimization sequence as a starting hypothesis (NOT a prescription). A `gap-narrative-writer` produces a single-paragraph executive summary. A `pattern-matcher` scores similarity between current funnel shape and the five examples; if similarity < threshold, it refuses to recommend.

### Recommended subagents
- `benchmark-lookup` — input: industry + stage + current rate; output: { bucket: poor|good|great, gap_to_great, table_row }.
- `pattern-matcher` — input: current funnel + observed drops; output: { matched_example, similarity_score, optimization_sequence }.
- `gap-narrative-writer` — produces an executive paragraph contextualizing performance against benchmarks.
- Hand-off to `funnel-basics-framework` (diagnosis) and `funnel-tactics-*` (action).

### Prompt pattern
```
You are benchmark-lookup. Read knowledge/pro/marketing/conversion-optimizer/funnel-basics-examples/README.md.
Input: { industry: "saas|ecom|mobile|b2b|email", stage, current_rate }.
Output JSON: { matched_row, good_band, great_band, current_bucket: "below_good|good|great",
gap_to_great_pct, related_example_id }.
Refuse if industry/stage not in tables.
```

```
You are pattern-matcher. Compare the current funnel (steps + rates) to the 5 README examples.
Output: { ranked: [{ example_id, similarity: 0..1, key_match_signals[], divergences[] }],
top_match: <id>, recommend_copy_sequence: bool (true only if similarity > 0.7) }.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mixpanel` / `amplitude` / `posthog` | Compute current funnel rates to compare with benchmarks | https://posthog.com/docs/api |
| `unbounce`-CRO-benchmark report | External anchor source | https://unbounce.com/conversion-rate-optimization/conversion-benchmark-report/ |
| `baymard-institute` reports | Ecommerce checkout-step benchmarks | https://baymard.com/checkout-usability |
| `littledata` benchmarks API | Shopify-specific funnel benchmarks | https://www.littledata.io/benchmarks |
| `appcues` mobile-onboarding report | Mobile onboarding-step benchmarks | https://www.appcues.com/blog/mobile-app-onboarding-benchmarks |
| `dbt` + warehouse | Standardize benchmark joins for repeatable reports | https://docs.getdbt.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Unbounce CRO Benchmark | SaaS report | Read-only | Annual industry CR benchmarks |
| OpenView SaaS Benchmarks | SaaS report | Read-only | Best for SaaS tier-by-tier conversion |
| Baymard Institute | Subscription | Read-only | Gold standard for ecommerce checkout |
| Littledata | SaaS | Yes — API | Shopify benchmark cohorts |
| HubSpot Marketing Statistics | Source | Read-only | B2B lead-gen averages |
| Adjust / AppsFlyer | SaaS | Yes | Mobile install-to-active benchmarks |

## Templates & scripts
Inline benchmark gap calculator agents can call:

```python
# benchmark_gap.py — compare current rate to README good/great bands
def gap(current: float, good: tuple[float, float], great: tuple[float, float]) -> dict:
    if current >= great[0]: bucket = "great"
    elif current >= good[0]: bucket = "good"
    else: bucket = "below_good"
    return {
        "current": current,
        "good_band": good,
        "great_band": great,
        "bucket": bucket,
        "gap_to_great_low": max(great[0] - current, 0.0),
        "headroom_pct": round((great[1] / max(current, 1e-9) - 1) * 100, 1),
    }

# Example: gap(0.012, (0.02, 0.05), (0.05, 0.10))  -> SaaS Visitor->Signup at 1.2%, "below_good"
```

The README itself is the source of truth — agents only read; they do not invent benchmarks.

## Best practices
- Always report the bucket (below_good / good / great) AND the gap to great — single-number lookups invite over-reaction.
- Pair benchmark with confidence band (sample size, lookback) of the operator's own data; don't compare last-week noise to industry averages.
- Use the five worked examples as hypothesis triggers, not playbooks — the README's tests succeeded in their context, not yours.
- For ecommerce, prefer Baymard's checkout-step bands over the README's averages when available; they are higher-resolution.
- For mobile install→open, segment by paid vs organic — the bands diverge significantly post-iOS-14.
- For B2B, replace "Demo → Customer 20–30%" with sales-cycle-aware bands; this README's number is stale for long enterprise cycles.
- Refresh benchmarks annually; flag any benchmark older than ~18 months as stale.

## AI-agent gotchas
- Agents will report a single benchmark number with false precision. Force band output (low–high), not point estimate.
- Pattern-matcher will hallucinate similarity to a worked example; require similarity > 0.7 AND ≥3 matched signals before recommending the example's sequence.
- Benchmarks measure the past; agents must NOT use them as forecasts. Frame outputs as "context", not "target".
- The Mobile App example "+180%" lift came from collapsing 3 onboarding screens to 1 — replicating without segment analysis can hurt activation when complex products genuinely need education.
- Email benchmarks are highly inflated by good list hygiene; agents recommending email tactics must add a "deliverability check" prerequisite.
- Don't blend B2B + B2C benchmarks when reporting; agents should refuse mixed-ICP comparisons.
- Subscription example assumes credit-card pre-auth at trial start; agents must check legal/CMP feasibility before recommending.

## References
- `README.md` (this directory)
- Unbounce CRO benchmark report — https://unbounce.com/conversion-rate-optimization/conversion-benchmark-report/
- OpenView SaaS conversion benchmarks — https://openviewpartners.com/blog/saas-conversion-rate-benchmarks/
- Baymard Institute checkout usability — https://baymard.com/checkout-usability
- Appcues mobile onboarding benchmarks — https://www.appcues.com/blog/mobile-app-onboarding-benchmarks
- HubSpot Marketing Statistics — https://www.hubspot.com/marketing-statistics
