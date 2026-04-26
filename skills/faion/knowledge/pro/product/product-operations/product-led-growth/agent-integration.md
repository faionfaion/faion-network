# Agent Integration — Product-Led Growth (PLG)

## When to use
- SaaS / dev tools / API products where users can self-onboard without sales (Linear, Vercel, Posthog-style).
- ACV under ~$25k where sales-led economics break down; freemium → paid conversion is the growth lever.
- The product produces measurable in-app events (signup, activation step, feature use) that can drive PQL scoring.
- Bottom-up motion targeting individual contributors who later expand to teams (Slack, Notion, Figma pattern).
- Existing product with traffic but flat activation — clear room for funnel instrumentation and onboarding redesign.

## When NOT to use
- Highly regulated, procurement-heavy enterprise sales (defense, banking core systems) — buyer is not the user.
- Products requiring data integration, on-prem deploy, or contracts before any value can be shown.
- Average contract value > $100k where one closed deal pays for many SDRs; sales-led ROI dominates.
- Pre-PMF: PLG amplifies a working loop; on a broken product it just industrialises churn.
- Network products without single-player value — agents will optimise activation that has no payoff if the user lands alone.

## Where it fails / limitations
- "Freemium tax": free tier consumes infra cost but converts <2% — common when no usage-gated upgrade trigger exists.
- TTV measured by clicks, not value: vanity activation rates that don't predict retention.
- One-size onboarding for distinct personas → low activation across all of them; segmentation is the unlock.
- Sales-assist gap: PQLs surface but no human follow-up motion → expansion revenue stalls at SMB ceiling.
- AI-onboarding personalisation breaks when the model has no behavioural signal yet (cold start in first 60 seconds).
- Privacy regimes (GDPR, India DPDP) restrict event tracking that PLG analytics depend on; consent-mode gaps distort funnels.

## Agentic workflow
PLG is an instrumentation-and-iteration loop, which maps cleanly to subagent orchestration. Use a `researcher`-style agent to inventory the current funnel (events, drop-offs, persona splits), a planner agent to propose an activation hypothesis with one metric to move, and an executor agent to ship the smallest in-product change (tour copy, default state, gate placement). Pair this with `faion-sdd-execution` so each PLG experiment ships through the same SDD quality gates as code, and use `faion-brainstorm` for diverging activation hypotheses before converging on the one to test. Keep humans in the loop for pricing/packaging changes — those are not safe to automate.

### Recommended subagents
- `faion-sdd-executor-agent` — drives an activation experiment as an SDD task: spec (hypothesis, metric, guardrail) → design (event schema, variant) → impl → test-plan (SRM check, MDE).
- `faion-brainstorm` — diverge/converge on activation hypotheses and TTV interventions before committing to a test.
- `faion-improver` — session loop to audit funnel telemetry, find leak with biggest delta, file improvement task.
- Repo-local `agents/` (none PLG-specific yet) — use `faion` to load `pro/product/product-manager`, `pro/marketing/growth-marketer`, `pro/marketing/conversion-optimizer` content as context for whichever agent runs.

### Prompt pattern
```
You are a PLG growth analyst. Given this funnel snapshot
(<events JSON>) and persona segment (<segment>), identify the
single largest drop-off where lift > MDE 3pp is plausible in 14d.
Output: hypothesis, metric, guardrail metric, smallest-change variant.
No copy that requires legal review. Return strict JSON.
```
```
You are an onboarding editor. Rewrite step <N> tooltip so that
TTV for persona <P> drops below 5 minutes. Constraints: <=14 words,
no marketing language, must reference the action the user just
took. Output 3 variants + rationale per variant.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| PostHog CLI / API | Self-host product analytics, funnels, session replay, feature flags, A/B | https://posthog.com/docs/api |
| GrowthBook CLI | OSS feature flagging + experimentation, Bayesian stats | https://docs.growthbook.io/tools/cli |
| Statsig CLI | Feature gates, holdouts, exposure logs, PQL scoring | https://docs.statsig.com/sdks/cli |
| Amplitude API | Funnels, cohorts, export raw events for offline PQL scoring | https://www.docs.developers.amplitude.com |
| Mixpanel API | Funnels + JQL for custom PQL queries | https://developer.mixpanel.com |
| Segment / RudderStack CLI | Event pipeline, ID resolution, downstream fanout | https://www.rudderstack.com/docs/cli |
| Stripe CLI | Subscription lifecycle, usage records, webhook listeners for upgrade events | https://docs.stripe.com/stripe-cli |
| dbt | Transform raw events → activation/PQL/NRR models in warehouse | https://docs.getdbt.com |
| Cube.dev | Semantic layer for PLG metrics (activation, TTV, NRR) shared across stack | https://cube.dev/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | OSS + Cloud | Yes (full REST + webhooks) | Best default for agent-driven PLG; replays + flags + experiments in one. |
| GrowthBook | OSS + Cloud | Yes (REST, SDKs) | Cleanest experimentation API; pairs with any analytics warehouse. |
| Statsig | SaaS | Yes (REST) | Strong holdout + sequential testing; PQL scoring built in. |
| Amplitude | SaaS | Partial (export-heavy) | Rich charts but agent ergonomics worse than PostHog. |
| Mixpanel | SaaS | Partial | JQL good for ad-hoc PQL queries; less native experimentation. |
| Pendo / Appcues / Userflow | SaaS | Partial | In-app tours; webhooks decent, code-as-source weak — risky for agent edits. |
| Frigade | SaaS | Yes (React + API) | Onboarding flows as code → agent can PR a tour. |
| Endgame / Pocus / Correlated | SaaS | Yes (signal export) | PQL signal layer; feeds reverse ETL into CRM for sales-assist. |
| Hightouch / Census | SaaS | Yes | Reverse ETL warehouse → Salesforce/HubSpot for PQL handoff. |
| ProfitWell / ChartMogul | SaaS | Yes | NRR, expansion, churn — the financial counterpart to activation metrics. |
| Stripe Billing | SaaS | Yes (CLI + API) | Usage-based billing, the engine behind expansion revenue. |

## Templates & scripts
See `templates.md` for the PLG metric definitions table. The script below is a minimal PostHog → PQL scorer an agent can run as a scheduled job; it weights events into a score and writes back as a person property so flags / sales-assist routing can consume it.

```python
# pql_score.py — minimal PostHog PQL scorer
# Run: PH_HOST=... PH_KEY=... python pql_score.py
import os, time, requests
HOST = os.environ["PH_HOST"].rstrip("/")
KEY  = os.environ["PH_KEY"]
WEIGHTS = {                      # tune per product
    "workspace_created":   3,
    "second_user_invited": 5,
    "integration_added":   4,
    "report_exported":     2,
    "limit_warning_seen":  6,    # buying signal
}
SINCE = int(time.time()) - 14 * 86400

def hog(path, **q):
    r = requests.get(f"{HOST}{path}",
                     headers={"Authorization": f"Bearer {KEY}"},
                     params=q, timeout=30)
    r.raise_for_status(); return r.json()

scores = {}
for evt, w in WEIGHTS.items():
    page = hog("/api/event/", event=evt, after=SINCE)
    for e in page.get("results", []):
        did = e.get("distinct_id")
        if did: scores[did] = scores.get(did, 0) + w

for did, score in scores.items():
    requests.post(f"{HOST}/api/projects/@current/persons/",
                  headers={"Authorization": f"Bearer {KEY}"},
                  json={"distinct_id": did,
                        "properties": {"pql_score": score,
                                       "pql_tier": "hot" if score >= 12 else
                                                   "warm" if score >= 6 else "cold"}},
                  timeout=30)
print(f"scored {len(scores)} users")
```

## Best practices
- Define activation as the smallest event sequence that predicts D30 retention; back-test before locking the metric.
- Instrument before you optimise — agents producing variants on uninstrumented funnels will hill-climb noise.
- Keep one north-star metric (activation rate, NRR, or PQL→paid) per quarter; rotate hypotheses, not metrics.
- Gate experimentation behind SRM (sample-ratio mismatch) and pre-registered MDE; both catch most "lift" mirages.
- Bake usage limits into the free tier from day one; without a friction edge there is no upgrade trigger.
- Pair PLG with sales-assist above $X MRR — PLG ceilings are real; the question is when to add humans, not whether.
- Persona-segment onboarding — single-tour designs lose to 3-tour designs almost every time, and AI personalisation works best layered on top of segments.
- Treat copy and defaults as code: PR-reviewed, versioned, behind flags. Lets agents safely contribute.

## AI-agent gotchas
- Agents will happily over-fit on small samples. Enforce minimum exposure (≥1k users/variant) and minimum runtime (≥7d) before agents are allowed to call a winner.
- LLMs invent metrics ("engagement score 0–100") that have no source event. Constrain output to a known event vocabulary loaded from the analytics schema.
- Agents miss the difference between activation rate and retention — winning variants on activation can cannibalise D30. Always require a retention guardrail.
- Tour-builder agents tend to add steps; PLG wins usually come from removing steps. Prompt with "subtract first" and a step-count budget.
- Cold-start personalisation: agents will write personalised copy citing data the system does not yet have on a new user. Enforce a "no behavioural reference before event N" rule.
- Pricing/packaging changes are not safe for autonomous agents — revenue regression risk is non-recoverable. Human approval required.
- Don't let agents touch consent / cookie banner logic; one mis-step breaks all downstream PLG telemetry.
- PQL scoring drifts: the model an agent ships today decays as the product changes. Schedule a quarterly recalibration task instead of trusting a static threshold.

## References
- Wes Bush — *Product-Led Growth* (book) and ProductLed Institute frameworks.
- OpenView Partners — *2024/2025 Product Benchmarks* (activation, NRR, PQL data).
- Reforge — Growth Loops & PLG curricula (Brian Balfour, Elena Verna).
- Lenny Rachitsky — interviews with Linear, Notion, Figma, Loom, Posthog growth leads.
- PostHog Handbook — https://posthog.com/handbook (PLG instrumentation patterns).
- GrowthBook docs — https://docs.growthbook.io (experimentation methodology).
- Bain & Co. — *NPS / NRR* benchmarks for PLG vs sales-led SaaS.
