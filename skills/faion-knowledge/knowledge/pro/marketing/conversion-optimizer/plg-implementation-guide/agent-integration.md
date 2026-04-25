# Agent Integration — PLG Implementation Guide

## When to use
- Operationalizing a PLG model after `plg-basics` advisor selected one — turning the strategy into Aha definition, TTV measurement, free-tier limits, upgrade triggers, self-serve checkout, and PQL scoring.
- Producing a phased rollout plan (Foundation → Free Tier Design → Activation → Monetization → Expansion) that maps cleanly to engineering tickets.
- Running freemium-to-paid, trial-to-paid, or expansion playbooks as deterministic state machines (Day 0 / Day 2 / Day 5 / Day 7 patterns).
- Selecting the PLG tech stack (analytics, onboarding, billing, PQL scoring) and producing an implementation RFC.

## When NOT to use
- High-level PLG model choice (route to `plg-basics`).
- Stage-specific tactic catalog (route to `plg-optimization-tactics`).
- Detailed metric definitions and PQL math (route to `plg-metrics`).
- Pre-PMF teams without an Aha-moment hypothesis — running this checklist before PMF wastes engineering cycles.

## Agentic workflow
This README maps directly to a multi-agent state machine: an `aha-moment-finder` mines retained-vs-churned cohorts, a `ttv-instrumenter` adds the funnel events from signup to Aha, a `playbook-runner` drives the freemium / trial / expansion playbooks as scheduled jobs (Day 0/2/5/7 etc.), and a `phase-tracker` walks the 5-phase implementation checklist as Linear/Jira issues. Human approval gates: free-tier limit numbers, pricing-page changes, sales-assist handoffs.

### Recommended subagents
- `aha-moment-finder` — pulls cohort behavior data, returns the action most correlated with retention + confidence interval.
- `ttv-instrumenter` — emits a funnel-event spec (event names, properties) and a PR plan to add them.
- `playbook-runner` — schedules the freemium/trial/expansion sequences in Customer.io / Klaviyo / Intercom; renders templates + waits.
- `pql-scorer` — wraps the PQL definition from `plg-metrics` and assigns scores nightly.
- `phase-tracker` — converts the 5-phase implementation checklist into trackable issues, reports completion %.

## When NOT to use
- (covered above)

## Where it fails / limitations
- The 5-phase checklist is a maturity ladder, not a roadmap; agents should not promise sequential delivery without a parallel-tracks variant.
- Aha-moment discovery requires sufficient converted-cohort data (≥ ~200 paid users); below that, statistical correlation is unreliable and human judgment dominates.
- Day-N playbook timings (Day 2/5/7/14) are heuristics from B2B SaaS — B2C, dev tools, and creator-economy products have different windows.
- "Tools & Tech Stack" table mixes free + enterprise tiers; agents must include cost + integration-effort columns before recommending.
- PQL section defers to `plg-metrics` — agents must chain reads, not invent scoring locally.

### Prompt pattern
```
You are aha-moment-finder. Read knowledge/pro/marketing/conversion-optimizer/plg-implementation-guide/README.md.
Input: { event_log: <reference>, paid_cohort_ids, churned_cohort_ids }.
Method: per the README, find action most correlated with D30 retention. Validate with cohort analysis.
Output JSON: { aha_event, lift_vs_baseline, p_value, sample_size, runner_up_events: [] }.
Reject if sample_size < 200 paid users.
```

```
You are playbook-runner. Given user_id, plan, day_in_journey, render the matching playbook
(Freemium / Trial / Expansion) from the README. Output: { channel, template_id, send_at, subject,
body, in_app_payload }. Do NOT send; queue for human approval.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mixpanel` JQL | Aha-moment correlation analysis on cohorts | https://developer.mixpanel.com/reference/jql-overview |
| `amplitude` Behavioral Cohorts API | PQL behavioral cohort sync | https://www.docs.developers.amplitude.com/analytics/apis/behavioral-cohorts-api/ |
| `posthog` cohort + flag API | Run free/trial/paid cohorts and feature flags | https://posthog.com/docs/api |
| `customerio` API | Drive Day-N playbook campaigns programmatically | https://customer.io/docs/api/ |
| `klaviyo` API | Trial-to-paid email sequences with metric triggers | https://developers.klaviyo.com/ |
| `intercom` API | In-app messaging + chat for trial assistance | https://developers.intercom.com/ |
| `madkudu` / `breeze` (HubSpot) | PQL scoring services | https://www.madkudu.com/api |
| `stripe` Billing API | Plan changes, proration, downgrade flows | https://stripe.com/docs/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amplitude / Mixpanel / PostHog | SaaS / OSS | Yes | Aha-moment + TTV instrumentation |
| Appcues / Pendo / Userflow / Chameleon | SaaS | Partial | Onboarding flows, checklists, in-app upgrade triggers |
| Intercom / Drift / Crisp | SaaS | Yes | Chat assistance for trial-day-1 pattern |
| Hotjar / FullStory / Heap | SaaS | Partial | Diagnose where users miss Aha |
| Stripe / Paddle / Chargebee | SaaS | Yes | Self-serve checkout (Step 4 essentials) |
| Customer.io / Autopilot / Klaviyo | SaaS | Yes | Day-N email automation |
| Madkudu / Clearbit Reveal | SaaS | Yes | PQL scoring + lead enrichment |

## Templates & scripts
Inline minimal day-N scheduler agents can call:

```python
# day_n_playbook.py — schedule freemium-to-paid playbook from this README
from datetime import datetime, timedelta, timezone

PLAYBOOK = [
    (0,  "in_app",  "limit_notification"),
    (2,  "email",   "limit_value_email"),
    (5,  "in_app",  "remaining_capacity_reminder"),
    (7,  "email",   "discount_offer_20pct"),
]

def schedule(user_id: str, trigger_ts: datetime) -> list[dict]:
    return [
        {
            "user_id": user_id,
            "send_at": (trigger_ts + timedelta(days=d)).isoformat(),
            "channel": ch,
            "template": tmpl,
            "approved": False,
        }
        for d, ch, tmpl in PLAYBOOK
    ]

# Wire into Customer.io campaigns or PostHog feature flags;
# 'approved' must flip to True via human review before send.
```

See `templates.md` (Aha-moment worksheet, PQL spec) and `examples.md` (full freemium-to-paid example) in this directory.

## Best practices
- Ship Phase 1 (Foundation) end-to-end before starting Phase 2 — the README's order is sequential because each phase depends on the previous instrumentation.
- For Aha-moment work, validate with at least two methods: behavioral correlation + qualitative converted-user interviews.
- TTV target < 5 minutes is aggressive but achievable only with templates/sample data — bake the seeding into onboarding or the metric is theatre.
- Day-N playbook content must reference user behavior ("you've created 4 of 5 projects"), not generic upsell copy.
- PQL handoff to sales triggers ONLY above the model-defined ACV cutoff; below that, automation closes the loop.
- For expansion playbook, watch leading signals (3+ active users, @mentions, external sharing) — not just paid-seat counts.
- Always pair upgrade-trigger UI changes with measurement: track impression, click, dismiss, post-click conversion separately.

## AI-agent gotchas
- LLM-generated playbook copy drifts to "Hi there, hope you're doing well" filler. Force tone-anchor against existing converting messages.
- Day-N playbook must NOT auto-send without human review; agents queue, humans approve. Even with confidence guardrails, mis-sent campaigns are brand-damaging.
- Aha-moment discovery is correlation, not causation — agents will overfit to noisy events. Require ≥30% lift vs random control + p<0.05.
- Free-tier limit changes ripple to revenue forecasting; never let an agent change limits autonomously, even with phase-tracker green-light.
- Self-serve checkout instrumentation must include payment-failure events; agents that skip these miss the largest BoF leak.
- For trial-day-12 urgency emails, the agent should personalize with actual usage stats — generic "your trial ends" emails underperform; require usage-property injection.
- Do NOT auto-trigger sales outreach from PQL signals without an SLA — bad timing kills conversion.

## References
- `README.md` (this directory)
- Wes Bush, "Product-Led Growth" — https://productled.com/book/
- OpenView PLG benchmarks — https://openviewpartners.com/product-led-growth/#benchmarks
- Elena Verna, PLG Playbook — https://www.elenaverna.com/plg-playbook
- Madkudu, PQL definition + scoring — https://www.madkudu.com/blog/what-is-a-product-qualified-lead
- Amplitude, Time-to-Value — https://amplitude.com/blog/time-to-value
