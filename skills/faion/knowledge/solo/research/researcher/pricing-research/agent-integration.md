# Agent Integration — Pricing Research

## When to use
- Pre-launch: setting initial price for a SaaS, course, template pack, or service.
- Re-pricing: revenue-per-customer is below the value capture (10-20% of value delivered).
- Designing a new tier (Pro / Enterprise) on top of an existing plan.
- Choosing between subscription, usage-based, one-time, or hybrid models for a new product.

## When NOT to use
- Your product has <10 paying customers — you don't have enough signal; price by intuition / competitor anchor and iterate.
- Highly bespoke enterprise sales — pricing is negotiated per deal; this methodology applies only to the published rate card.
- Marketplace / two-sided platforms — pricing must consider take-rate dynamics and supply-demand elasticity, not just willingness-to-pay.
- Regulated pricing (healthcare, energy, telecom) — compliance dominates research; use industry-specific frameworks.

## Where it fails / limitations
- Van Westendorp requires N ≥ 30 same-segment respondents to be statistically meaningful. Agents quote "Optimal price = $X" from N=5 interviews — that's noise, not signal.
- "10-20% of value delivered" capture rate is industry-folklore, not a calibrated number. Anchoring there can leave 50%+ on the table for high-leverage tools.
- Competitor pricing pages are increasingly opaque ("Contact us") or A/B tested per visitor. Agents that scrape once get a stale snapshot.
- The README's "2-3x price jump between tiers" rule fails for low-priced solopreneur SaaS (e.g., $9 → $19 → $39 outperforms $9 → $27 → $81).
- Annual discount math (~17% for "2 months free") cannibalizes monthly cohort if billing is not gated behind a clear upgrade event.
- Pricing-page A/B tests have huge variance; agents conclude "price X wins" from non-significant lifts.

## Agentic workflow
Run as a 4-stage pipeline. Stage 1 (haiku): scrape the pricing matrix for ≥5 competitors (entry/mid/pro) plus their feature gating. Stage 2 (sonnet): compute value-capture math from the founder's value claims; flag if capture > 25% (probably overpriced) or < 5% (underpriced). Stage 3 (sonnet): design 3 candidate tier structures and label psychology (anchor, decoy, growth-path). Stage 4 (opus): write a Pricing Research Report with confidence level + a validation plan (A/B test, pricing-page intent, customer-development calls). Founder picks the launch price.

### Recommended subagents
- `faion-pricing-researcher-agent` — canonical agent named in the README.
- A custom `pricing-page-scraper` (haiku) — strict JSON, fetches Contact-us-or-not flag and feature gating per tier.
- A custom `van-westendorp-analyzer` (sonnet) — takes 4 columns of survey data, returns intersection points + confidence interval.
- A custom `tier-designer` (sonnet) — proposes 3 tier structures with explicit psychology rationale.
- `faion-brainstorm` — diverge over pricing-model options before converging on subscription/usage/hybrid.

### Prompt pattern
```
Read skills/faion/knowledge/solo/research/researcher/pricing-research/README.md.
Build a competitor matrix for <category>, ≥5 competitors. Per row: {competitor, free_tier,
entry_price, entry_features[], pro_price, pro_features[], enterprise:bool, annual_discount_pct,
url, scraped_at}. Flag any "Contact us" pricing.
```

```
Given value claims [<list>] and competitor matrix, compute value-capture range. Recommend
3 candidate tier structures with feature gating (free/starter/pro/enterprise). Output JSON.
Include rationale per tier (anchor / volume / upsell).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `apify` CLI | Pricing-page scraping at scale | https://docs.apify.com/cli |
| `playwright` | Render JS-heavy pricing pages | `npx playwright install` · https://playwright.dev |
| `pandas` / `polars` | Van Westendorp curves from CSV survey | https://pola.rs |
| `r-survey` (R) | Stats-grade conjoint analysis | https://cran.r-project.org/package=conjoint |
| `posthog` CLI | Pricing-page experiment results | https://posthog.com/docs/api |
| `stripe` CLI | Test pricing changes against live mode | https://docs.stripe.com/stripe-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Billing | SaaS | Yes | Programmatic price/tier/coupon creation; agents drive via API. |
| Paddle / LemonSqueezy | SaaS | Yes | Merchant-of-record; pricing changes via API. |
| Profitwell / ChartMogul | SaaS | Yes | Pricing experiment metrics (ARR, churn-by-plan). |
| PostHog / Statsig | SaaS / OSS | Yes | Pricing-page A/B tests with stat-significance built in. |
| Wynter | SaaS | Partial | B2B copy-pricing testing with pre-vetted ICPs (human respondents). |
| Maze / Sprig | SaaS | Yes | Run Van Westendorp surveys with auto-analysis. |
| Typeform / Tally | SaaS | Yes | Cheap survey delivery; agent-callable webhooks. |
| Pricing.com / Competera | SaaS | Yes (paid) | Continuous competitor price monitoring (e-commerce mostly). |

## Templates & scripts
See `templates.md` and the README's "Pricing Research Report" + "Quick Pricing Check". Inline Van Westendorp intersection (Python ≤30 lines):

```python
import pandas as pd, sys
df = pd.read_csv(sys.stdin)  # cols: too_cheap, cheap, expensive, too_expensive
prices = sorted(set(df.values.ravel()))
def cum(col, op):
    return [sum(op(df[col], p)) / len(df) for p in prices]
tc = cum("too_cheap", lambda c, p: c >= p)
ch = cum("cheap", lambda c, p: c >= p)
ex = cum("expensive", lambda c, p: c <= p)
te = cum("too_expensive", lambda c, p: c <= p)
def cross(a, b):
    for i in range(1, len(prices)):
        if (a[i-1]-b[i-1]) * (a[i]-b[i]) <= 0:
            return prices[i]
    return None
print({"OPP": cross(tc, te), "IDP": cross(ch, ex)})  # Optimal/Indifference
```

## Best practices
- Anchor on value before competitors. Competitor-anchored pricing is a race to the bottom in commodity categories.
- Charge in the currency / units that scale with the customer's value (per-seat for collaboration, per-event for analytics, per-GB for storage).
- Always offer annual at ~16-20% discount — it improves cash flow and halves churn on average.
- Three tiers is the sweet spot: anchor (decoy at top), main (where you want most customers), entry (low-friction acquisition).
- Don't include the 4th "Custom" tier on the public page if you have no enterprise customers yet — it signals scale you don't have.
- Re-validate every 6 months. Markets shift; AI-augmented competitors compress prices fast.
- Grandfather existing customers when raising prices. Public goodwill > marginal revenue from churn.
- Test pricing-page copy more than the price itself — value framing typically moves conversion more than the dollar number within ±20%.

## AI-agent gotchas
- LLMs trained on 2022 data quote stale competitor prices. Always pass freshly-scraped HTML into the analyzer agent.
- Agents will happily compute Van Westendorp on N=4 responses and quote a 4-decimal-place "optimal price". Reject results below N=30 with explicit error.
- Capture-rate of "10-20%" is repeated as if it's a law. It's not — high-leverage tools (revenue-generators) capture 30-50%+ in practice.
- LLM-generated tier features tend to be vague ("priority support", "advanced analytics"). Force a specific feature list with measurable units.
- "Decoy" tiers should be designed deliberately, not as an afterthought. Agents pad the top tier with random features; require explicit rationale.
- Annual-discount math: agents say "12 months for the price of 10 = 17% off" but charge 16.7% — bias toward the cleaner 20%.
- Human checkpoint: any price change > 15% should be reviewed before publishing — automated reprice can cause customer-trust damage that survey data won't predict.
- Currency / locale: agents default to USD. International pricing requires PPP adjustment and local-tax handling (VAT, GST) — flag explicitly.

## References
- https://www.priceintelligently.com/blog
- https://www.profitwell.com/recur/all/pricing-strategy
- https://en.wikipedia.org/wiki/Van_Westendorp%27s_Price_Sensitivity_Meter
- https://hbr.org/2018/06/a-quick-guide-to-value-based-pricing
- https://stripe.com/guides/atlas/pricing
- https://docs.posthog.com/experiments/manual
- https://www.openviewpartners.com/expansion-saas-benchmarks/
