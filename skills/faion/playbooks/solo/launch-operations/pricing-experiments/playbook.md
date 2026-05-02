---
name: pricing-experiments
description: Run a 3-cohort price A/B test ($19/$39/$59) with Stripe lookup_keys and PostHog flags to find your optimal price point.
tier: solo
group: launch-operations
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a running price experiment across three cohorts ($19, $39, $59) wired through Stripe `lookup_key` switching and PostHog feature flags, with conversion and LTV tracked per cohort — giving you statistically grounded data to commit to a final price before you scale marketing.

## Prerequisites

- A Stripe account with at least one active Product (test mode is fine for dry runs; switch to live mode before real buyers hit the page).
- PostHog Cloud or self-hosted PostHog with a project API key (`phc_...`).
- A pricing page you control (HTML/React/Gatsby/Next.js — any stack with server-side or client-side rendering).
- `stripe` CLI installed locally (`brew install stripe/stripe-cli/stripe` or `apt install stripe`).
- At least 300 real visitors per month to reach 100-buyer minimum per cohort in reasonable time.
- Familiarity with the [pricing-strategy methodology](../../../knowledge/solo/marketing/gtm-strategist/ops-pricing-strategy) — this playbook operationalises its A/B test phase.

## Steps

1. **Create three Stripe prices with lookup_keys.**

   In the Stripe Dashboard (or via CLI), create three prices for the same Product. Assign a lookup_key to each:

   ```bash
   stripe prices create \
     --product prod_YourProductId \
     --unit-amount 1900 \
     --currency usd \
     --recurring[interval]=month \
     -d "lookup_key=plan_solo_19"

   stripe prices create \
     --product prod_YourProductId \
     --unit-amount 3900 \
     --currency usd \
     --recurring[interval]=month \
     -d "lookup_key=plan_solo_39"

   stripe prices create \
     --product prod_YourProductId \
     --unit-amount 5900 \
     --currency usd \
     --recurring[interval]=month \
     -d "lookup_key=plan_solo_59"
   ```

   Replace `prod_YourProductId` with your actual Stripe product ID from the Dashboard → Products tab.

2. **Create the PostHog feature flag.**

   In PostHog → Feature Flags → New flag:

   - Key: `pricing_cohort`
   - Type: Multiple variants (multivariate)
   - Variants: `v19` (33%), `v39` (33%), `v59` (34%)
   - Rollout: 100% of users
   - Conditions: none (everyone participates)

   Save. Copy the flag key — you will use it in step 3.

3. **Wire the flag to your pricing page.**

   Fetch the active variant on the server (SSR) or in the component. Example using the PostHog JS SDK:

   ```js
   import posthog from 'posthog-js'

   // Initialise once at app root:
   posthog.init('phc_YourProjectApiKey', { api_host: 'https://us.i.posthog.com' })

   // On pricing page render:
   const variant = posthog.getFeatureFlag('pricing_cohort') // 'v19' | 'v39' | 'v59'

   const LOOKUP_KEYS = {
     v19: 'plan_solo_19',
     v39: 'plan_solo_39',
     v59: 'plan_solo_59',
   }
   const activeLookupKey = LOOKUP_KEYS[variant] ?? 'plan_solo_39' // safe default
   ```

   Pass `activeLookupKey` to your Stripe Checkout session creation call:

   ```js
   // Server-side (Node.js / Python / any backend):
   const session = await stripe.checkout.sessions.create({
     line_items: [{
       price_data: undefined, // not needed when using lookup_key
       price: (await stripe.prices.list({ lookup_keys: [activeLookupKey] })).data[0].id,
       quantity: 1,
     }],
     mode: 'subscription',
     success_url: 'https://yourdomain.com/welcome',
     cancel_url: 'https://yourdomain.com/pricing',
   })
   ```

4. **Capture the conversion event in PostHog.**

   After a successful Stripe webhook (`checkout.session.completed`), fire a server-side PostHog event:

   ```python
   import posthog

   posthog.api_key = "phc_YourProjectApiKey"
   posthog.host = "https://us.i.posthog.com"

   posthog.capture(
       distinct_id=customer_email,
       event="subscription_started",
       properties={
           "pricing_cohort": cohort_variant,   # 'v19'|'v39'|'v59'
           "plan_amount_cents": amount_total,  # from Stripe event
           "lookup_key": lookup_key,
       },
   )
   ```

5. **Build the PostHog experiment dashboard.**

   In PostHog → Experiments → New experiment:

   - Feature flag: `pricing_cohort`
   - Primary metric: `subscription_started` (conversion)
   - Secondary metric: `subscription_started` → `amount_total` (revenue / LTV proxy)
   - Minimum sample size per variant: 100
   - Significance threshold: 95%

   PostHog will compute statistical significance automatically as events flow in.

6. **Monitor until 100 buyers per cohort.**

   Check the experiment dashboard weekly. Do not change prices, copy, or page layout during the test — isolate the price variable only.

   Anti-pattern to avoid: resetting prices every 7–10 days based on early numbers. A sample of 20–30 buyers per cohort is noise, not signal.

7. **Declare a winner and consolidate.**

   Once all three cohorts reach 100 buyers:

   - Compare conversion rate and estimated 30-day LTV per cohort.
   - Pick the variant with the highest `conversion_rate × price_amount` (expected revenue per visitor).
   - In Stripe Dashboard, set the winning `lookup_key` as your sole active price. Archive the others.
   - In PostHog, set the winning variant at 100% rollout and archive the experiment.

## Verify

Open PostHog → Experiments → `pricing_cohort`. Confirm:

1. All three variants show non-zero `subscription_started` event counts.
2. Variant distribution is within ±5 percentage points of 33/33/34 (PostHog shows this in the "Participants" tab).
3. Stripe Dashboard → Payments shows charges for all three price amounts (`$19.00`, `$39.00`, `$59.00`).

Quick CLI check for Stripe events in test mode:

```bash
stripe events list --limit 10 | grep "checkout.session.completed"
```

Should return at least one event per active cohort.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| All users land on the same price | `getFeatureFlag` returns `undefined` before PostHog initialises | Move flag evaluation to `posthog.onFeatureFlags(() => { ... })` callback, or use server-side flag evaluation via PostHog's `/decide` API |
| PostHog variant distribution is 90% v19, 0% v39 | Sticky bucketing is caching old assignments | In PostHog flag settings, disable "Persist feature flags across authentication" and clear the PostHog cookie (`ph_phc_*`) in dev tools to test |
| Stripe Checkout opens with wrong price | Lookup key lookup returns stale data from a previous test | Call `stripe prices list --lookup-keys plan_solo_39` to confirm exactly one active price matches; archive duplicates in the Dashboard |
| Conversion event not firing | Stripe webhook not reaching your server | Run `stripe listen --forward-to localhost:3000/api/stripe-webhook` to debug locally; check logs for 5xx responses |
| Experiment shows "insufficient data" after 300 buyers | Secondary metric (LTV) has high variance | Switch primary metric to conversion rate only; 100-buyer minimum applies per variant for conversion, not LTV |

## Next

- [pricing-experiments → stripe-integration-basics](../stripe-integration-basics/playbook.md) — complete your Stripe Checkout integration before running the experiment if you have not done so yet.
- After declaring a winner, run [pricing-experiments → customer-onboarding-email](../customer-onboarding-email/playbook.md) to reduce churn in the first 30 days.
- When conversion is stable, consider a geek-tier uplift: dynamic annual/monthly toggle using the same lookup_key pattern.

## References

- [knowledge/solo/marketing/gtm-strategist/ops-pricing-strategy](../../../knowledge/solo/marketing/gtm-strategist/ops-pricing-strategy) — provides the price-elasticity model and cohort-sizing rules that back the 100-buyer minimum and the `conversion × price` winner-selection formula in Step 7.
- [knowledge/solo/marketing/gtm-strategist/ops-subscription-models](../../../knowledge/solo/marketing/gtm-strategist/ops-subscription-models) — covers monthly vs. annual subscription trade-offs; informs the decision to test monthly prices first before introducing annual discounts.
- [knowledge/solo/product/product-operations/product-analytics](../../../knowledge/solo/product/product-operations/product-analytics) — defines the event schema and cohort tracking pattern used in Steps 4–5 to wire PostHog capture to the Stripe webhook.
