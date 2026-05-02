---
name: aarrr-funnel
description: Map every AARRR stage to an analytics event, identify the weakest cohort drop-off, and ship one targeted intervention per review cycle.
tier: pro
group: growth-marketing
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live AARRR dashboard (Acquisition → Activation → Retention → Referral → Revenue) wired to real analytics events, a cohort drop-off chart that surfaces your single weakest stage, and a documented process for picking one intervention per monthly review cycle — tested against a B2C SaaS example.

## Prerequisites

- A B2C SaaS product with at least 4 weeks of user sign-up data.
- Analytics platform in place: Mixpanel, Amplitude, or PostHog (self-hosted or cloud). Google Analytics 4 works for Acquisition and basic Activation; Mixpanel/Amplitude/PostHog are required for Retention cohort charts.
- Event tracking already emitting at least `page_view` and `sign_up`. If not, complete basic event instrumentation before this playbook.
- Access to your payment processor data (Stripe recommended) — needed for Revenue stage.
- A shared doc or Notion page where your team logs growth decisions.

## Steps

### Stage 1 — Map AARRR to analytics events

1. **Define one primary event per stage.** Map each AARRR stage to one measurable analytics event. Use the table below as your starting point and adapt column 3 to your product:

   | Stage | Definition | Primary event (adapt to your product) | Secondary check |
   |-------|------------|----------------------------------------|-----------------|
   | Acquisition | User lands for the first time | `page_view` with `utm_source` present | Channel breakdown (organic / paid / referral) |
   | Activation | User experiences the "aha moment" | `project_created` / `first_report_run` / `dashboard_saved` | Time-to-activation (median minutes from sign-up) |
   | Retention | User returns in week 2 and week 4 | `session_start` in cohort week 2 (W2 retention) | D30 retention rate |
   | Referral | User invites another user or shares a link | `invite_sent` / `referral_link_copied` | Viral coefficient k = invites sent × invite-to-signup CVR |
   | Revenue | User converts to paid plan | `subscription_started` (Stripe `customer.subscription.created`) | MRR from cohort, churn rate |

2. **Audit your current event coverage.** In Mixpanel/Amplitude, run `Event Explorer → All Events` sorted by volume. Confirm each stage-1 event from the table fires. Mark gaps as `MISSING`.

3. **Implement missing events.** For each `MISSING` event add tracking in your frontend or backend. Example for PostHog (JavaScript):

   ```js
   // Fire when user creates their first project — Activation event
   posthog.capture('project_created', {
     project_id: project.id,
     user_plan: user.plan,         // 'free' | 'pro'
     minutes_since_signup: Math.round((Date.now() - user.createdAt) / 60000),
   });
   ```

   For Stripe Revenue events, use a Stripe webhook to `POST /analytics/revenue-event` and forward to your analytics platform via server-side SDK.

4. **Tag all acquisition sources with UTM parameters.** Every paid ad, newsletter link, and social post must carry `utm_source`, `utm_medium`, `utm_campaign`. Create a shared UTM builder sheet (copy from `templates/utm-builder.csv` if included with this playbook). Without UTMs, Acquisition is a black box.

### Stage 2 — Build the cohort drop-off chart

5. **Create a Funnel report.** In Mixpanel or Amplitude, create a Funnel with these steps in order:
   - Step 1: `sign_up`
   - Step 2: `[your activation event]` (e.g., `project_created`)
   - Step 3: Retention proxy — use a "Retention" report, not a funnel step, for D7/D30 rates
   - Step 4: `subscription_started`

   Set window to `within 30 days`. Group by `signup_week` (cohort week). Export as PNG for your growth doc.

6. **Add a Retention cohort table.** Go to Retention → Cohort Retention. Set:
   - Starting event: `sign_up`
   - Returning event: `session_start`
   - Granularity: weekly
   - Date range: last 8 cohort weeks

   This produces a standard retention triangle. Healthy B2C SaaS benchmarks: W1 ≥40%, W4 ≥20%, W8 ≥15%. Below these = Retention is your weakest stage.

7. **Identify the weakest stage.** Calculate the drop-off percentage between each adjacent pair:

   ```
   Acquisition → Activation drop-off = (1 - activation_rate) × 100
   Activation → Retention drop-off   = (1 - W4_retention_rate) × 100
   Retention → Referral drop-off      = (1 - referral_rate) × 100
   Referral → Revenue drop-off        = (1 - paid_conversion_rate) × 100
   ```

   The stage with the largest drop-off is your constraint. Write it down: `Weakest stage: [X]`.

   **Worked example — "TaskFlow" (B2C project-management SaaS):**

   | Stage | Rate | Drop-off |
   |-------|------|----------|
   | Acquisition → Activation | 18% activate within 24 h | **82% drop-off** ← weakest |
   | Activation → Retention (W4) | 31% of activated users return at W4 | 69% |
   | Retention → Referral | 9% of retained users send invite | 91% |
   | Referral → Revenue | 22% of trial users convert to paid | 78% |

   TaskFlow's constraint: Activation. Only 18 of 100 sign-ups create a first project within 24 hours.

### Stage 3 — Pick one intervention

8. **Generate three candidate interventions for the weakest stage.** Brainstorm in writing — do not skip this step. For each candidate write: hypothesis, change required, success metric, minimum detectable effect (MDE).

   **TaskFlow example (Activation):**

   | # | Hypothesis | Change | Success metric | MDE |
   |---|-----------|--------|----------------|-----|
   | A | Users don't create a project because the empty state is confusing | Replace empty dashboard with a 3-step guided setup wizard | Activation rate W1 | +5 pp (18% → 23%) |
   | B | Users drop off at the template picker (too many options) | Reduce templates from 24 to 3 curated defaults | Median time-to-activation | −20% |
   | C | Users who receive a Day-1 activation email create more projects | Add triggered email at t+1h if no `project_created` event | Activation rate W1 | +3 pp (18% → 21%) |

9. **Pick ONE intervention using ICE score.** Score each candidate on Impact (1–10), Confidence (1–10), Ease (1–10). Average = ICE score.

   ```
   ICE = (Impact + Confidence + Ease) / 3
   ```

   TaskFlow scores: A = (8+7+5)/3 = 6.7 | B = (6+8+8)/3 = 7.3 | C = (5+9+9)/3 = 7.7

   Chosen intervention: **C** (triggered Day-1 email). Highest ICE; can be shipped without engineering.

10. **Implement and tag the intervention.** Add a feature flag (LaunchDarkly, PostHog feature flags, or a simple env var) so you can roll back. For email interventions use your ESP (Mailchimp/Loops/Customer.io). Tag the flag in analytics:

    ```js
    // PostHog feature flag check — gate the guided wizard experiment
    if (posthog.isFeatureEnabled('guided-setup-wizard')) {
      renderGuidedWizard();
      posthog.capture('experiment_exposed', { experiment: 'guided-setup-wizard', variant: 'treatment' });
    }
    ```

11. **Set a review cadence.** Schedule a monthly AARRR review on the first Monday of each month. Agenda:
    - Review funnel drop-off chart (regenerate from live data).
    - Check if last month's intervention moved the needle (compare pre/post cohorts).
    - If moved: document the win, pick the next weakest stage.
    - If flat: post-mortem (wrong hypothesis, too short a window, implementation bug?), pick next intervention for the same stage.

## Verify

Run all three checks in sequence after Stage 2 is complete:

**Check 1 — Event coverage:**

```bash
# PostHog: verify events arrive via HTTP API debug endpoint (replace with your project API key)
curl -s "https://app.posthog.com/api/projects/<project_id>/events/?event=project_created&limit=5" \
  -H "Authorization: Bearer <personal_api_key>" | python3 -m json.tool | grep '"event"'
```

Expect 5 lines: `"event": "project_created"`. If zero lines → event is not firing.

**Check 2 — Funnel report integrity:**

In Mixpanel/Amplitude, open the Funnel report and confirm:
- All 3+ steps have non-zero counts.
- The date range covers ≥4 complete weeks (incomplete weeks skew activation rate).
- "Conversion window" is set to 30 days (not session-scoped — session scope deflates rates).

**Check 3 — Weakest stage documented:**

Open your growth decisions doc and confirm the following line exists and is filled in:

```
Weakest stage (YYYY-MM): [Activation | Retention | Referral | Revenue]
Chosen intervention: [one sentence]
ICE score: [X.X]
```

If any check fails, revisit the corresponding step before running the monthly review.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Activation rate looks 100% or 0% | Funnel event order is wrong or event name has a typo | Re-check event names in Mixpanel Event Explorer; copy-paste exact strings into funnel steps |
| Retention cohort triangle is empty for recent weeks | Cohort not yet complete — recent weeks haven't aged to W4 | Use only cohorts that are ≥30 days old; ignore the right diagonal of the triangle |
| All stages have similar drop-off (~60–70%) | You haven't found your "aha moment" event yet | Interview 5 churned users + 5 retained users; identify the one feature that separates them; use that as your Activation event |
| Referral rate is artificially high (>50%) | Invite event fires on page load, not on actual send | Audit the event — it must fire only after the user clicks "Send invite" or copies the referral link |
| ICE scores are all similar | Team is scoring emotionally, not empirically | Require evidence for Confidence: past A/B test data, user interview count, or benchmark comparison before scoring ≥7 |
| Intervention shipped but cohort shows no change after 4 weeks | Sample size too small or MDE too large | Run a power calculation: for a 5 pp lift at 80% power you need ~600 users per variant; check if you hit that |

## Next

- `ltv-cac-attribution` — once Activation and Retention are healthy, wire LTV/CAC attribution per acquisition channel to find your most profitable growth lever.
- `google-ads-first-campaign` — if Acquisition is your weakest stage, add a structured paid channel as a second traffic source alongside organic.
- Run the North Star Metric methodology (`knowledge/pro/marketing/growth-marketer/north-star-metric`) to collapse AARRR into one leading indicator that the whole team tracks.

## References

- [knowledge/pro/marketing/growth-marketer/aarrr-pirate-metrics](../../../knowledge/pro/marketing/growth-marketer/aarrr-pirate-metrics) — primary AARRR framework: defines each stage, drop-off calculation formula, and the stage-prioritisation logic used in Steps 7 and 8.
- [knowledge/pro/marketing/growth-marketer/cohort-basics](../../../knowledge/pro/marketing/growth-marketer/cohort-basics) — cohort construction rules applied in Step 6; explains why incomplete cohorts (right-triangle diagonal) must be excluded from W4 retention comparisons.
- [knowledge/pro/marketing/growth-marketer/activation-framework](../../../knowledge/pro/marketing/growth-marketer/activation-framework) — aha-moment identification method used in the Troubleshooting row "You haven't found your aha moment event yet" and in the TaskFlow activation intervention design.
- [knowledge/pro/marketing/growth-marketer/north-star-metric](../../../knowledge/pro/marketing/growth-marketer/north-star-metric) — NSM selection process referenced in Next; compresses AARRR into one leading metric once funnel stages are instrumented.
