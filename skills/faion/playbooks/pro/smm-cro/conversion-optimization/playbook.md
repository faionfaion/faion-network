---
name: conversion-optimization
description: Run a data-driven CRO cycle — heatmaps, funnel drop-off, A/B testing to 95% significance — and ship the winner to production.
tier: pro
group: smm-cro
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have shipped one conversion-rate improvement — backed by behavioral data, a structured hypothesis, and a statistically significant A/B test — with a documented lift in your target metric (e.g., CTA-click rate, sign-up rate, or checkout completion).

## Prerequisites

- A live web page or funnel step with at least 500 monthly unique visitors (below this, tests take too long to reach 95% significance).
- Analytics access: Google Analytics 4 or PostHog with funnel reports enabled.
- A heatmap / session tool: Hotjar, Microsoft Clarity, or PostHog's session recordings.
- An A/B testing platform: Optimizely, VWO, or PostHog feature flags with experiment mode.
- Dev access to deploy a variant (or a no-code editor like Webflow / Unbounce if the page supports it).
- Familiarity with: `pro/smm-cro/` tier playbooks or equivalent growth-marketing background.

## Steps

1. **Identify the highest-impact drop-off step.**
   Open your funnel report in GA4 or PostHog. Look for the step with the steepest drop — a ≥40% fall-off on a high-traffic step is your primary target. Note the absolute number of lost users per week; this is your opportunity size.

2. **Collect behavioral data on the drop-off step.**
   - Install the Hotjar snippet (or enable Clarity) on the target URL if not already running.
   - Wait at least 7 days and collect ≥200 sessions.
   - Review three data types:
     - **Heatmap (click + move):** identify where users click that is NOT the CTA, and where they never reach.
     - **Scroll map:** note the fold — if ≥50% of users never scroll past the hero, the CTA below the fold is invisible.
     - **Session recordings:** watch 15–20 sessions filtered to users who bounced; note rage-clicks, hesitations, and exit points.

3. **Write a falsifiable hypothesis.**
   Use this template:

   ```
   We believe [specific change] will [lift metric] by [target %]
   because [behavioral evidence from step 2].
   ```

   Real example that produced a 2.1% → 2.9% lift on a SaaS pricing page:

   ```
   We believe moving the "Start free trial" CTA from below the pricing
   table to a sticky header bar will lift CTA-click rate by 20%+
   because the scroll map shows 62% of visitors never reach the
   below-fold CTA, and session recordings show users actively
   scrolling up to find the signup button after reading pricing.
   ```

4. **Calculate the required sample size before launching.**
   Use the VWO or Optimizely sample-size calculator (both free, no login required):
   - Baseline conversion rate: read from GA4 (e.g., 2.1%).
   - Minimum detectable effect: your target lift (e.g., 20% relative = 2.52% absolute).
   - Significance: 95%; power: 80%.

   For the example above: baseline 2.1%, MDE 20% relative → ~4 200 visitors per variant. At 1 400 visitors/week per variant, the test runs ~3 weeks.

   Do not end a test early because it "looks good."

5. **Build the variant.**
   - In Optimizely or VWO: use the visual editor or inject JS/CSS via the snippet.
   - In PostHog: create a feature flag, wrap the variant element in `posthog.isFeatureEnabled('cta-sticky-header')`, deploy to staging, QA on mobile + desktop.
   - Ensure both control and variant log the same goal event (e.g., `cta_click` with `location: header` or `location: below_fold`).

6. **Launch the experiment at a 50/50 split.**
   - Turn on the test in your platform.
   - Verify split is live: check the experiment dashboard shows roughly equal traffic within the first hour.
   - Set a calendar reminder for the minimum run duration calculated in step 4.

7. **Monitor without peeking.**
   Check the dashboard once every 2–3 days only to confirm data is flowing (impressions incrementing, no JavaScript errors). Do not make shipping decisions until the pre-calculated sample size is reached.

8. **Read the results at significance threshold.**
   When the sample size is hit, read the p-value:
   - p ≤ 0.05 + positive lift → variant wins, proceed to ship.
   - p ≤ 0.05 + negative lift → control wins; revert, document learnings, repeat from step 2 with new hypothesis.
   - p > 0.05 → inconclusive; run longer (if traffic allows) or accept null result and pivot hypothesis.

9. **Ship the winner.**
   - Merge the variant code to production (or publish the winning Webflow / Unbounce variant as default).
   - Remove the A/B testing snippet or archive the flag.
   - Update your funnel report baseline: record new conversion rate + date in your CRO log (a simple spreadsheet or Notion table works — columns: page, hypothesis, control %, winner %, lift %, test duration, date shipped).

10. **Document and repeat.**
    Add the result to your CRO backlog. Schedule the next hypothesis session for 2 weeks post-ship (give the new baseline time to stabilize). Aim for one completed test per month per high-traffic funnel step.

## Verify

Open your funnel report in GA4 or PostHog, filter to a 14-day window starting 3 days after ship (to avoid novelty effect). Confirm:

```
New conversion rate ≥ (control rate × (1 + target_lift))
```

For the pricing-page example: 2.1% × 1.20 = 2.52% minimum; observed 2.9% → test confirmed in production.

If the lift does not persist in the post-ship baseline, check for: seasonal traffic shifts, a concurrent campaign change, or a broken goal event (re-audit the event in GA4 DebugView or PostHog Live Events).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Test runs 6+ weeks with no significance | Baseline conversion too low or MDE too ambitious | Lower the MDE target to 10% relative, or target a higher-traffic page |
| Control and variant show identical click rates | Goal event firing on both variant elements | Audit event triggers; confirm variant element has the correct selector; preview the experiment in VWO/Optimizely QA mode |
| Heatmap shows no data after 7 days | Snippet not installed on the correct URL | Verify the Hotjar / Clarity snippet fires on the target page via browser DevTools → Network tab → filter `hotjar` or `clarity` |
| Variant flickers on page load (FOOC) | A/B snippet loads async after DOM paint | Load Optimizely/VWO snippet synchronously in `<head>` or use PostHog feature flags server-side to pre-assign variant before HTML render |
| Post-ship lift disappears in 30 days | Novelty effect | Segment returning vs. new visitors; if only new-visitor rate lifted, the change is genuine — returning users already adapted to the old layout |
| Stakeholder pressure to end test early | "The variant is winning 30-0, why wait?" | Share the sample-size calculation; early stopping inflates false-positive rate from 5% to ~30%; run to the calculated N |

## Next

- `pro/smm-cro/landing-page-teardown` — systematic teardown framework to generate 5–10 hypotheses from a single page before running individual tests.
- `pro/growth-marketing/aarrr-funnel` — map your full AARRR funnel to identify which stage (Acquisition, Activation, Retention) has the highest ROI for CRO investment.
- `pro/paid-acquisition/ltv-cac-attribution` — once CRO lifts conversion rate, recalculate LTV:CAC to decide whether to increase ad spend.

## References

- [knowledge/pro/marketing/conversion-optimizer/growth-conversion-optimization](../../../knowledge/pro/marketing/conversion-optimizer/growth-conversion-optimization) — provides the hypothesis-driven CRO loop (observe → hypothesize → test → ship) that structures Steps 1–10 of this playbook.
- [knowledge/pro/marketing/conversion-optimizer/funnel-tactics-advanced](../../../knowledge/pro/marketing/conversion-optimizer/funnel-tactics-advanced) — covers advanced funnel drop-off analysis patterns used in Steps 1–2 to prioritize which page to test first.
