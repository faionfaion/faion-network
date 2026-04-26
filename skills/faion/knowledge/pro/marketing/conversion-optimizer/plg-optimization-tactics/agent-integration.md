# Agent Integration — PLG Optimization Tactics

## When to use
- Running an existing PLG product where activation, free-tier-to-paid, or expansion conversion has plateaued and you need a backlog of tested tactics rather than a strategy rewrite.
- Designing a free tier or self-serve checkout from scratch and want a pre-curated list of friction points to instrument before launch.
- Generating in-product upgrade copy, feature-gate messaging, and pricing-page variants that follow the methodology's "good vs bad" patterns.
- Producing a quarterly A/B test backlog scored against the included onboarding/upgrade/pricing test idea bank.

## When NOT to use
- Pre-product-market-fit teams without measurable activation data — generic tactics will distract from PMF discovery.
- Pure sales-led ACVs above ~$50K where self-serve patterns do not survive procurement; route to sales-led playbooks instead.
- Single-event transactions (one-shot ecommerce, ticketing) where there is no expansion or seat-growth surface to optimize.
- Hard-regulated products (healthcare, banking) where "instant access, no approval" recommendations conflict with compliance.

## Where it fails / limitations
- Lift bands ("+10–25%") are aggregate; agents must not promise them as forecasts. Always reframe as hypotheses with ICE scoring.
- Free-tier limit choices are the single highest-leverage decision but the methodology gives only directional guidance; this requires human judgment + cohort data, not LLM inference.
- Expansion playbooks assume team/seat surface; usage-based products need a different signal model (consumption curves, not invitee count).
- Tactics list is timeless; pricing-page best practices change yearly — verify against current Stripe/ProfitWell/Reforge posts before shipping copy.

## Agentic workflow
Treat this methodology as a tactics catalog that a Claude subagent indexes and queries. The orchestrator first pulls current funnel metrics from the analytics tool, the subagent then maps each weak step to candidate tactics from this README, scores them with ICE, and emits a ranked test backlog plus draft copy variants. A human PMM reviews free-tier-limit and pricing-page changes before they ship; copy variants and A/B test specs can ship via approval-gated PRs.

### Recommended subagents
- `faion-growth-agent` (named in README's "Agent Selection") — primary owner; can be wrapped as a Claude subagent that reads the README and emits structured tactic recommendations.
- A spawned `plg-tactic-mapper` subagent — input: drop-off step + segment, output: 3–5 tactics from this doc with rationale and ICE skeleton.
- `copy-variant-writer` subagent — turns a single feature gate or upgrade prompt into 5 variants following the "Bad/Good Examples" rules in this file.

### Prompt pattern
```
You are plg-tactic-mapper. Read knowledge/pro/marketing/conversion-optimizer/plg-optimization-tactics/README.md.
Input: { stage: "activation|free-to-paid|expansion", weak_step: "<event>", current_rate: 0.XX, segment: "<seg>" }.
Output JSON: [{ tactic, source_section, hypothesis, ice: {impact, confidence, ease}, instrumentation }].
No prose outside the JSON array.
```

```
You are copy-variant-writer. Given { feature_gate, current_copy, plan_target }, produce 5 variants
that follow the README "Good Examples" rules: name a similar customer, quantify the value, name
the plan, and end with a two-button CTA. Reject any variant matching the listed "Bad Examples".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` CLI / API | Pull funnel + activation cohorts; trigger feature flags for A/B tests | `pip install posthog`; https://posthog.com/docs/api |
| `mixpanel` Query API | JQL/Insights for activation funnel and free-to-paid cohorts | https://developer.mixpanel.com/reference/query-api |
| `amplitude` REST API | Cohort + funnel pulls, behavioral cohorts for PQL | https://www.docs.developers.amplitude.com/analytics/apis/ |
| `stripe` CLI | Inspect checkout sessions, pricing tiers, proration logic | `brew install stripe/stripe-cli/stripe` |
| `appcues` API | Programmatically deploy onboarding checklists / progressive flows | https://developer.appcues.com/ |
| `growthbook` / `flagsmith` | OSS feature-flag + A/B test infra agents can drive end-to-end | https://docs.growthbook.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | OSS + SaaS | Yes — full REST + flag API | Best end-to-end (analytics + flags + recordings) for autonomous agents |
| Amplitude | SaaS | Partial — read APIs solid, write requires SDK | Good for PQL behavioral cohorts |
| Mixpanel | SaaS | Yes | JQL flexible; good for ad-hoc tactic-impact queries |
| Stripe Billing | SaaS | Yes | Drive plan changes, proration tests; pricing-page experiments via Pricing Tables API |
| Appcues / Pendo / Userflow | SaaS | Partial — checklist + tour CRUD via API | Use for progressive onboarding tactics from this doc |
| Chameleon | SaaS | Partial | Good for upgrade-prompt placement experiments |
| Reforge / OpenView reports | Source | Read-only | Benchmark anchoring; agent should cite, not invent benchmarks |

## Templates & scripts
Inline ICE scoring helper agents can call:

```python
# ice_score.py — score tactic backlog from this methodology
from dataclasses import dataclass

@dataclass
class Tactic:
    name: str
    impact: int      # 1-10 expected lift on the target metric
    confidence: int  # 1-10 evidence strength (own data > industry > guess)
    ease: int        # 1-10 inverse cost (eng + design weeks)

    @property
    def ice(self) -> int:
        return self.impact + self.confidence + self.ease

    def bucket(self) -> str:
        if self.ice >= 24: return "test_now"
        if self.ice >= 18: return "this_quarter"
        if self.ice >= 12: return "if_capacity"
        return "backlog"

def rank(tactics: list[Tactic]) -> list[Tactic]:
    return sorted(tactics, key=lambda t: t.ice, reverse=True)

# Agents emit Tactic(...) instances per README section, then call rank().
```

See `templates.md` and `examples.md` in this directory for the upgrade-prompt and pricing-page comparison tables the agent should fill in.

## Best practices
- Always pair a tactic with the activation/expansion metric it moves and a current baseline; tactics without baselines are theatre.
- Run the "TOO GENEROUS / TOO RESTRICTIVE / BALANCED" free-tier sketch as an explicit subagent step before recommending any limit change.
- For upgrade prompts, enforce the README rules: name a comparable customer, quantify saved time/value, name the plan; reject "Upgrade Now" and "Premium Plan" copy.
- Trigger PQL-based prompts at 80% of limit (per README), never 100% — agent should hard-code this as a guardrail in generated configs.
- Cap upgrade prompts to one per session and zero during the first session; bake this into any auto-generated Appcues/Pendo flow.
- Keep ≤4 pricing tiers and require an annual-discount field in any pricing-page draft; reject layouts that hide it.

## AI-agent gotchas
- LLMs love to recommend "remove all limits" or "give 30-day trial" — this conflicts with the README's balanced-tier guidance. Pin the system prompt to the specific limit-type matrix in this doc.
- Auto-generated upgrade copy will drift to generic SaaS language ("powerful features", "enterprise-grade"). Add a post-filter that scans for these tokens and rewrites them.
- Agents should never write directly to a paid Stripe price object or live Appcues flow — gate every mutation behind a human-approved PR or ticket.
- Free-tier limit changes must be reviewed with finance + retention data — never let an agent ship a limit change autonomously, even with high ICE.
- PQL scoring weights drift over time; require the agent to re-fit weights against converted cohorts every quarter, not reuse last quarter's coefficients.
- The "Empty State Time < 2 minutes" target requires server-side data seeding; agents producing onboarding flows must explicitly include the seed step or the metric is unreachable.

## References
- `README.md` (this directory) — canonical tactic list and Agent Selection table
- ProfitWell, Freemium Pricing Strategy — https://www.profitwell.com/recur/all/freemium-pricing-strategy
- Stripe, SaaS Checkout Optimization — https://stripe.com/guides/saas-checkout-optimization
- ChartMogul, Expansion Revenue Playbooks — https://chartmogul.com/blog/expansion-revenue/
- Reforge, Feature Gating Strategies — https://www.reforge.com/blog/feature-gating-strategies
- OpenView, PLG Benchmarks — https://openviewpartners.com/product-led-growth/
