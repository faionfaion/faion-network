# Agent Integration — Free Trial Optimization

## When to use
- SaaS with time-limited (7-30 day) trial whose trial-to-paid conversion is below ~15%.
- Clear activation metric defined; optimization target is reducing time-to-activation and lifting conversion.
- Building or refactoring the trial email sequence (welcome → quick start → mid-trial → ending → win-back).
- Designing trial extension and rescue mechanics for inactive trials.
- Comparing trial models (opt-in trial, opt-out trial, reverse trial, freemium-to-trial) for a product.

## When NOT to use
- No trial yet exists and product-led signup is not validated; first prove freemium or self-serve before optimizing trial mechanics.
- Sales-led product where the "trial" is really a POC managed by an account team.
- Pre-activation friction is the dominant problem (signup conversion) — fix that first.
- Compliance or contract-required custom trials per customer (enterprise legal); optimization is moot.

## Where it fails / limitations
- Activation metric chosen by intuition rather than data ("they invited a teammate" without proving invite users actually convert).
- Email sequence built without a stop-on-activation rule; sequences keep nagging activated users until they unsubscribe.
- Trial countdowns that create urgency but no path to value; users feel pressured and bounce.
- Hard paywall at trial end without grace period destroys win-back rate; export friction angers users into negative reviews.
- Extension offers given to everyone become entitlement; only inactive trials should get them.
- Behavioral triggers fire from frontend events that misfire (consent banner, ad blockers); silent breakage.
- Trial-to-paid metric measured at day 14 only ignores deferred conversions in day 21-45.

## Agentic workflow
A Claude subagent can: (1) propose activation-metric candidates from a sample of converted vs churned trials; (2) audit the trial email sequence and rewrite each email to single-focus, <150 words, one CTA; (3) draft behavioral triggers (no-login-3-days → email A, completed-onboarding-no-data → email B); (4) read trial cohort data and propose 3-5 rescue interventions ranked by expected lift; (5) generate the trial-end transition copy. Do not let the agent send emails directly to production lists — operator stages and approves.

### Recommended subagents
- `faion-growth-agent` (referenced in README) — sonnet for trial flow analysis and copy; opus for choosing the trial model.
- A `trial-rescue-agent` (suggested) — sonnet for behavioral interventions; haiku for templated win-back emails.
- `faion-content-marketer` — for the email sequence's voice and quality bar.
- `faion-sdd-executor-agent` — model the trial redesign as an SDD task list with quality gates per intervention.

### Prompt pattern
```
Activation metric proposal: from sample <converted_n=300, churned_n=300>,
list 5 candidate activation events with: lift (converted vs churned %),
median time to event, sample-size confidence band. Reject any candidate
where lift is < 2x or p > 0.05.
```

```
Audit current trial email sequence <attached>. For each email: focus
score (1-5), word count, CTA count, on-trigger vs on-time. Rewrite top 3
worst, each ≤150 words, one CTA, in the brand voice. Mark the trigger
event for each.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `customer-io-cli` (community) | Manage Customer.io campaigns + segments | https://customer.io/docs/api/ |
| `posthog-cli` | Query trial funnel + cohorts | https://posthog.com/docs/cli |
| `dbt` | Define activation/conversion models | https://docs.getdbt.com/ |
| `growthbook` | A/B test trial variants | https://www.growthbook.io/ |
| `stripe` CLI | Inspect billing / subscription events | https://stripe.com/docs/stripe-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Customer.io | SaaS | Yes (API) | Behavior-triggered trial email engine |
| Loops | SaaS | Yes (API) | Modern lifecycle email with events |
| Intercom | SaaS | Yes (API) | In-app messages + email + Inbox |
| Drip | SaaS | Yes (API) | Lifecycle email automation |
| HubSpot | SaaS | Yes (API) | Marketing + CRM if sales-assist needed |
| Appcues / Userflow / Userpilot | SaaS | Yes (API) | In-app trial guidance + checklists |
| Chargebee | SaaS | Yes (API) | Trial management, extensions, dunning |
| Stripe | SaaS | Yes (API) | Trial billing + grace + win-back coupons |
| ProfitWell (Paddle) | SaaS | Yes (API) | Subscription analytics, churn diagnostics |
| Amplitude / Mixpanel / PostHog | SaaS / OSS | Yes (API) | Activation metric + cohort tracking |
| Hotjar / FullStory | SaaS | Yes (API) | Watch trial sessions to find friction |

## Templates & scripts
See `templates.md` for welcome / mid-trial / trial-ending email templates. Inline simple at-risk flagger:

```python
# at_risk.py — flag trials likely to churn before conversion.
# Inputs: trial_user dict from warehouse mart_trial_users.
def at_risk(u: dict) -> list[str]:
    flags = []
    if u["days_since_login"] >= 3: flags.append("inactive_3d")
    if not u["onboarding_complete"]: flags.append("stuck_onboarding")
    if u["features_used"] <= 1: flags.append("low_breadth")
    if u["team_invites_sent"] == 0: flags.append("solo_in_team_product")
    return flags
# Route flags to specific Customer.io segments via tags.
```

## Best practices
- Anchor the entire optimization on one activation metric; do not chase multi-metric scoreboards in a 14-day window.
- Welcome email arrives within 60 seconds of signup with one action; later emails diverge.
- Stop-on-activation is a hard rule; every campaign must subscribe to the activation event and exit on fire.
- Mid-trial check-in (day 7 of a 14-day trial) outperforms more frequent earlier emails — protect quiet space.
- Trial-end transition must be seamless: same data, same login, no re-entry of payment info if possible.
- Offer extensions only to genuinely inactive trials with a credible reason; broad extensions train users to procrastinate.
- Track trial-to-paid at day 30 and day 60, not just day 14; deferred converters are real.
- For PLG, expose pricing during trial — hidden pricing breaks trust and lowers conversion.

## AI-agent gotchas
- LLMs over-personalize emails with shallow tokens ("Hi {first_name}, hope your week is going well"). Cut tokens to 1-2 substantive ones (last action, days remaining).
- Behavioral trigger logic from the agent often runs OR where AND is needed. Validate the trigger predicate manually.
- "Best-practice" countdown urgency is overused; brand-voice constraints must override defaults.
- Agents conflate trial and freemium dynamics; force the prompt to specify trial type and gating model.
- Win-back copy generated by the agent leans pushy; require empathy + opt-out as constraints.
- Activation metric proposals based on small samples overfit; require sample size and confidence band on every proposal.
- Privacy: per-user behavior used for triggers must be aggregated/anonymized when sent to LLMs; do not leak subscriber emails into prompts.

## References
- ProfitWell, "Free trial best practices" — https://www.profitwell.com/recur/all/free-trial-conversion-rate
- Amplitude, "Activation metrics guide" — https://amplitude.com/blog/product-activation-metrics
- ChartMogul, "Trial-to-paid conversion" — https://chartmogul.com/blog/trial-to-paid-conversion/
- Customer.io, "Onboarding email playbook" — https://customer.io/blog/onboarding-email-best-practices/
- Baremetrics, "Trial extension strategies" — https://baremetrics.com/blog/trial-extension-strategies
- Wes Bush, *Product-Led Growth* (book), 2019.
- Reforge, "Trial vs freemium" — https://www.reforge.com/
