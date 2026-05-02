---
name: ltv-cac-attribution
description: Define LTV and CAC for your SaaS, build a multi-touch attribution model, and set a data-driven rule for when to scale paid spend.
tier: pro
group: paid-acquisition
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a spreadsheet model that calculates LTV, CAC, and payback period for your SaaS using real revenue data, a UTM tagging taxonomy wired into Mixpanel or Amplitude, a multi-touch attribution model you can query, and a clear rule that tells you when scaled paid spend is justified.

## Prerequisites

- A SaaS product with at least 3 months of paying-customer data in Stripe or your billing system.
- Access to Google Analytics 4 or a product analytics tool (Mixpanel / Amplitude).
- Paid ad accounts (Google Ads, Meta Ads) with conversion tracking enabled.
- A spreadsheet (Google Sheets or Excel) for the LTV/CAC model.
- UTM parameters being appended to all paid ad landing URLs (if not yet, this playbook covers setup).
- Familiarity with basic SaaS metrics (MRR, churn rate).

## Steps

### 1. Pull your baseline revenue and retention data

Export from Stripe (or your billing tool) the following for the last 6 months:

- Total MRR at start and end of period.
- Number of new paid customers acquired each month.
- Number of customers who churned each month.

Calculate monthly churn rate: `churned customers ÷ total customers at start of month`. Average across 6 months. For this example: 120 churned ÷ 2 400 total = **5% monthly churn**.

### 2. Calculate LTV

Formula: `LTV = ARPU × (1 / monthly_churn_rate)`

Using the hypothetical SaaS at $39/mo:

- ARPU = $39 (single plan; if you have multiple, use revenue-weighted average)
- Monthly churn = 5% → average customer lifetime = 1 / 0.05 = **20 months**
- LTV = $39 × 20 = **$780**

If you have expansion revenue (upgrades, add-ons), include it: `LTV = (ARPU + avg monthly expansion) × lifetime`. For this example, assume no expansion: LTV = **$780**.

Record this in cell B2 of your model spreadsheet.

### 3. Calculate CAC

Formula: `CAC = total paid acquisition spend ÷ new paid customers acquired`

Pull from your ad accounts and CRM for last month:

- Google Ads spend: $1 200
- Meta Ads spend: $800
- Total paid spend: **$2 000**
- New paid customers from paid channels (attributed, see Step 6): **40**
- CAC = $2 000 ÷ 40 = **$50**

If you also count sales salaries or agency fees as acquisition cost, add them to the numerator. For lean SaaS teams, use ad spend only first, then add overhead in a separate "fully-loaded CAC" column.

Record CAC in cell B3.

### 4. Calculate payback period and LTV/CAC ratio

In your spreadsheet:

- Payback period = `CAC ÷ ARPU` = $50 ÷ $39 = **~1.3 months** (excellent; most SaaS aim for ≤12 months)
- LTV/CAC ratio = $780 ÷ $50 = **15.6x**

This example is healthy. The decision rule:

| LTV/CAC | Interpretation | Action |
|---------|---------------|--------|
| < 1x | Losing money on every customer | Pause paid; fix pricing or churn first |
| 1x–3x | Marginal; risk | Hold spend flat; optimize CAC or improve retention |
| ≥ 3x | Healthy unit economics | Scale paid spend |
| ≥ 5x | Strong signal | Aggressive scaling justified |

**Scale only when LTV/CAC ≥ 3x.**

### 5. Set up UTM taxonomy

Every paid ad URL must carry 5 UTM parameters. Use this taxonomy:

| Parameter | Values | Example |
|-----------|--------|---------|
| `utm_source` | `google`, `meta`, `linkedin` | `google` |
| `utm_medium` | `cpc`, `paid-social`, `display` | `cpc` |
| `utm_campaign` | `{tier}-{goal}-{quarter}` | `pro-trial-q2-2026` |
| `utm_content` | ad creative ID or description | `headline-a` |
| `utm_term` | keyword (Google) or audience slug (Meta) | `saas-growth-tools` |

Build URLs using Google's [Campaign URL Builder](https://ga-dev-tools.google/campaign-url-builder/). Example final URL:

```
https://faion.net/pro?utm_source=google&utm_medium=cpc&utm_campaign=pro-trial-q2-2026&utm_content=headline-a&utm_term=saas-growth-tools
```

Paste generated URLs into your ad platform's "Final URL" field — never the display URL.

### 6. Configure attribution in Mixpanel or Amplitude

**Mixpanel:**

1. Go to Project Settings → Attribution.
2. Set attribution model to **Linear** (distributes credit equally across all touches in the conversion path). This is more honest than last-touch for multi-channel campaigns.
3. In the Events section, confirm you're capturing `utm_source`, `utm_medium`, `utm_campaign` as event properties on your `Sign Up` and `Subscription Started` events. If not, update your tracking code:
   ```js
   mixpanel.track('Subscription Started', {
     utm_source: getUrlParam('utm_source'),
     utm_medium: getUrlParam('utm_medium'),
     utm_campaign: getUrlParam('utm_campaign'),
     plan: 'pro',
     mrr: 39,
   });
   ```
4. Build a Funnels report: `Page View (utm_source = google) → Sign Up → Subscription Started`. Filter by `utm_campaign = pro-trial-q2-2026`.

**Amplitude:**

1. Go to Data → Sources → confirm UTM parameters are being ingested. Amplitude auto-captures them if you use the Browser SDK v2+.
2. Create a Chart → Funnel Analysis: `utm_source is google` → `subscription_started`.
3. Under Attribution, select **Linear** for the same reason as above.
4. Save as a Dashboard tile titled "Paid Attribution — Q2 2026".

### 7. Wire attribution data back to your CAC model

Each week, export from Mixpanel/Amplitude:

- New paid subscriptions attributed to each `utm_source` + `utm_campaign`.
- Pull matching spend from Google Ads / Meta Ads API (or export CSV).

Update your spreadsheet:

| Campaign | Spend | Attributed Conversions | CAC | LTV/CAC |
|----------|-------|----------------------|-----|---------|
| pro-trial-q2-2026 (Google) | $1 200 | 28 | $42.86 | 18.2x |
| pro-retarget-q2-2026 (Meta) | $800 | 12 | $66.67 | 11.7x |

Apply the decision rule per campaign: both exceed 3x → scale both, prioritize Google (better CAC).

### 8. Define your scaling trigger and budget ceiling

Add two cells to the model:

- **Scaling trigger:** `=IF(B4 >= 3, "SCALE", "HOLD")` where B4 = LTV/CAC ratio.
- **Max monthly budget:** `= target_new_customers × CAC`. If you want 200 new customers next month at $50 CAC: budget ceiling = $10 000.

Review these numbers weekly during active campaigns. Reduce budget if CAC rises above 1/3 of LTV ($260 in this example).

## Verify

Open your Mixpanel or Amplitude dashboard and run a Funnels report filtered to `utm_source = google` for the last 30 days. Confirm:

1. `Subscription Started` events appear with `utm_campaign` property populated (not null).
2. Conversion count matches (within ±5%) the "Conversions" column in your Google Ads account for the same period.
3. Your spreadsheet LTV/CAC cell reads ≥ 3 before any budget increase is approved.

If UTM properties are null on `Subscription Started`, UTMs are being dropped at redirect — check your landing page for meta-refresh redirects or JS router that strips query params.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `utm_source` is null on 30–40% of Subscription Started events | Session timeout between ad click and conversion | Switch attribution window to 30-day click in Mixpanel; enable `distinct_id` persistence across subdomains |
| CAC doubles month-over-month with flat spend | Audience saturation | Expand lookalike audiences or add new ad sets targeting different intent keywords; rotate creatives |
| LTV/CAC drops below 3x despite good ARPU | Churn spike | Pause scaling; diagnose churn (exit surveys, cohort analysis); fix before resuming paid |
| Google Ads "Conversions" column shows 0 | Conversion action not firing | Check Google Tag Manager: verify the `purchase` or `sign_up` tag fires on your `/thank-you` page using GTM Preview mode |
| Mixpanel funnel shows fewer conversions than Stripe | UTM not passed to backend on checkout | Store UTM params in `localStorage` on first page load; send them as metadata on the Stripe customer object via your API |
| Payback period > 12 months | ARPU too low or CAC too high | Either raise price (A/B test $49 vs $39), reduce spend on high-CAC campaigns, or improve landing-page conversion rate |

## Next

- `google-ads-first-campaign` — once LTV/CAC ≥ 3x is confirmed, use this playbook to launch or restructure your Google Search campaign with proper bidding strategy.
- Apply cohort analysis (see `knowledge/pro/marketing/growth-marketer/cohort-basics`) to segment LTV by acquisition channel — Google vs Meta cohorts often have meaningfully different retention curves.
- When monthly paid budget exceeds $5 000, introduce a **Data-Driven Attribution** model in Google Ads (replaces last-click; requires ≥300 conversions in 30 days) and re-export attributed conversion counts to your spreadsheet.

## References

- [knowledge/pro/marketing/ppc-manager/ads-attribution-models](../../../knowledge/pro/marketing/ppc-manager/ads-attribution-models) — linear vs last-touch vs data-driven attribution trade-offs; backs the choice of Linear model in Steps 6 and the upgrade trigger in Next
- [knowledge/pro/marketing/ppc-manager/ads-budget-optimization](../../../knowledge/pro/marketing/ppc-manager/ads-budget-optimization) — CAC-based budget ceiling formula and scaling decision logic used in Step 8
- [knowledge/pro/marketing/growth-marketer/ops-metrics-basics](../../../knowledge/pro/marketing/growth-marketer/ops-metrics-basics) — ARPU, churn rate, and LTV calculation methodology underlying Steps 2–4
- [knowledge/pro/marketing/growth-marketer/cohort-basics](../../../knowledge/pro/marketing/growth-marketer/cohort-basics) — cohort retention analysis that feeds accurate average lifetime into the LTV formula; referenced in Next
- [knowledge/pro/marketing/ppc-manager/growth-paid-acquisition](../../../knowledge/pro/marketing/ppc-manager/growth-paid-acquisition) — paid acquisition channel strategy and LTV/CAC threshold benchmarks used in the decision-rule table in Step 4
