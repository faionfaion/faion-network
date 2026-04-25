# Agent Integration — PLG Basics & Models

## When to use
- Choosing a PLG model (freemium / free trial / open core / usage-based) for a new product or a new pricing tier on an existing one.
- Auditing whether a current sales-led or marketing-led GTM should adopt or hybridize with PLG (the "Is PLG Right for You?" matrix is the test).
- Onboarding new founders / PMs / agents who need a shared vocabulary (Aha moment, TTV, PLG flywheel) before deeper PLG work.
- Producing strategic memos and pricing-model RFCs that need a defensible model classification with examples.

## When NOT to use
- Tactical optimization questions ("which form fields, which copy") — route to `plg-optimization-tactics` instead.
- Implementation steps (Aha definition, PQL scoring, playbooks) — route to `plg-implementation-guide`.
- Metric definitions and tracking — route to `plg-metrics`.
- Deep enterprise procurement, six-figure sales-cycle products — methodology explicitly flags these as "Poor Fit" (>$50K/year, training-heavy).

## Where it fails / limitations
- Comparison matrix is directional, not predictive: a "Good Fit" product can still fail PLG if onboarding is broken; the methodology underweights team capability.
- The PLG-vs-Sales-Led table flattens hybrid PLS (product-led-sales) reality — most modern PLG ($1K–$50K ACV) needs a sales-assist motion the README only briefly mentions.
- CAC bands ("$10–$100 PLG") are aggregate and reflect category leaders; B2B PLG typically lands $200–$800.
- Examples (Slack, Zoom, Notion) are survivor-biased mega-cases. Agents must avoid extrapolating "X did Y, therefore we should" without checking distribution dynamics, network effects, and viral coefficient.

## Agentic workflow
This is the foundational/strategy layer of the PLG knowledge cluster. A single Claude subagent typically reads this README to produce a model-fit memo: it ingests product fundamentals (price, ICP, complexity, decision-maker, TTV target), maps them to the four models, and outputs a recommendation with rationale. For execution, the orchestrator then chains to `plg-implementation-guide` (steps), `plg-optimization-tactics` (tactics), and `plg-metrics` (instrumentation). Output stays advisory; no autonomous mutations.

### Recommended subagents
- `plg-model-advisor` — reads this README, takes product fundamentals as input, returns a ranked model recommendation with rationale.
- `plg-fit-scorer` — scores a product against the "Is PLG Right for You?" matrix, returning a 0–6 fit score and gap list.
- Hand-off to `faion-growth-agent` (named in README's Agent Selection) for downstream tactical work.

### Prompt pattern
```
You are plg-model-advisor. Read knowledge/pro/marketing/conversion-optimizer/plg-basics/README.md.
Input: { product_name, target_acv, icp, time_to_value_now, complexity_score, decision_maker, market_size }.
Output JSON: {
  recommended_model: "freemium|free_trial|open_core|usage_based|hybrid_pls",
  rationale: "<one paragraph citing README sections>",
  fit_score: 0-6,
  gaps: [],
  next_methodology: "plg-implementation-guide" | "plg-optimization-tactics" | "plg-metrics"
}
```

```
You are plg-fit-scorer. Score the product against the 6 factors in the "Is PLG Right for You?"
table (complexity, decision maker, price, TTV, trial feasibility, market size).
Return per-factor 0/1 plus total. If total < 4, recommend hybrid PLG + Sales.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` / `mixpanel` / `amplitude` | Measure baseline TTV and activation rate to validate model choice | https://posthog.com/docs/api |
| `stripe` CLI | Inspect existing pricing model, prototype new tiers in test mode | `brew install stripe/stripe-cli/stripe` |
| `chargebee` / `paddle` API | Multi-tier subscription experiments, freemium-to-paid metering | https://apidocs.chargebee.com/docs/api |
| `lago` (OSS metering) | Open-source usage-based billing engine for Model 4 | https://getlago.com/docs |
| `openllmetry` | Trace LLM-driven onboarding flows and TTV instrumentation | https://github.com/traceloop/openllmetry |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Billing | SaaS | Yes — full API | Required for any of the four models |
| Paddle | SaaS | Yes | Merchant of record; better for global SaaS PLG |
| Chargebee | SaaS | Yes | Strong for hybrid (PLG + sales-assist) tiering |
| Lago | OSS | Yes | Usage-based metering with self-hosted control |
| OpenView Insights | Source | Read-only | Best benchmark provider; agent should cite, not invent |
| Reforge / Lenny's Newsletter | Source | Read-only | Strategy reference; quality > recency varies |

## Templates & scripts
Inline model-fit scorer agents can call:

```python
# plg_fit.py — score product fit against the README matrix
from dataclasses import dataclass

@dataclass
class ProductFit:
    complexity_simple: bool        # intuitive (1) vs requires-training (0)
    end_user_decides: bool         # end user (1) vs C-level/procurement (0)
    price_under_50k: bool          # < $50K/year (1) vs above (0)
    ttv_minutes_to_hours: bool     # minutes-hours (1) vs days-weeks (0)
    trial_feasible: bool           # easy to try (1) vs requires implementation (0)
    market_large: bool             # large TAM (1) vs niche (0)

    @property
    def score(self) -> int:
        return sum([self.complexity_simple, self.end_user_decides,
                    self.price_under_50k, self.ttv_minutes_to_hours,
                    self.trial_feasible, self.market_large])

    @property
    def recommendation(self) -> str:
        if self.score >= 5: return "pure_plg"
        if self.score >= 3: return "hybrid_plg_sales"
        return "sales_led_with_plg_signals"
```

See `examples.md` for the four canonical model studies (Slack, Zoom, Notion, Calendly) and `templates.md` for the model-comparison worksheet.

## Best practices
- Always derive Aha moment from cohort data of converted users, not from product team intuition (the README's "interview converted users + cohort analysis" rule).
- Use this README as a strategy anchor only — do not recommend a model without explicit TTV, ACV, and ICP inputs from the operator.
- For hybrid recommendations, make the ACV cutoff explicit ($1K/mo per README); below = self-serve, above = sales-assist.
- When recommending freemium, force the agent to also propose the upgrade trigger (limit, feature gate, time, collaboration) and the corresponding metric to track.
- Pair every model recommendation with a "PLG kill criteria" — if activation rate after 90 days < X% or freemium → paid < Y%, switch model.
- Treat the four mega-examples as anchor points only; replace with peer comps in the actual recommendation.

## AI-agent gotchas
- LLMs will default to recommending "freemium" for almost any SaaS — pin the prompt to require the fit matrix walk-through before the recommendation.
- The README does not deeply cover product-led-sales (PLS) — agents will under-recommend the hybrid motion. Add explicit PLS branch in the advisor prompt for ACV $1K–$10K/mo.
- Open-source / Open Core advice underweights ToS, license-shift risk (BSL, SSPL); agents must NOT recommend open-core without a license-strategy callout.
- Usage-based pricing requires a clean value metric — agent should refuse the recommendation if the input cannot identify one quantitative unit of value.
- The "PLG Flywheel" diagram is a mental model, not a measurement framework; agents should never present it as a metric pipeline. Route to `plg-metrics` for actual instrumentation.
- Don't generate marketing copy from this file — it's strategic taxonomy. Route to `growth-conversion-optimization` or `growth-landing-page-design`.

## References
- `README.md` (this directory)
- Wes Bush, "Product-Led Growth" — https://productled.com/book/
- OpenView, PLG Index + Benchmarks — https://openviewpartners.com/product-led-growth/
- Elena Verna on PLG — https://www.elenaverna.com/plg
- Kyle Poyar, Growth Unhinged — https://kylepoyar.substack.com/
- Lenny's Newsletter on PLG companies — https://www.lennysnewsletter.com/p/how-the-best-product-led-growth-companies
