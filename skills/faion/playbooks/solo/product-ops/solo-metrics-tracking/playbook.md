---
name: solo-metrics-tracking
description: Wire 5 KPIs (MRR, paid signups/wk, churn rate, NPS, free→paid conversion) into a single-page dashboard so you act on numbers, not gut feel.
tier: solo
group: product-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have five live metrics — MRR, paid signups per week, churn rate, NPS, and free-to-paid conversion — feeding a single-page dashboard you review every Monday. You will know what to check, where each number comes from, and what a bad number tells you to do next.

## Prerequisites

- A Stripe account with at least one active subscription product.
- A PostHog account (free tier is sufficient; https://posthog.com) with the JS or Python snippet installed in your product.
- Access to your Stripe dashboard (https://dashboard.stripe.com).
- A transactional email sender (e.g., Resend, SendGrid, Mailgun, or Postmark) for the one-question NPS email.
- Either a Notion workspace or a Google Sheets account for the dashboard — or a ChartMogul account (free tier at https://chartmogul.com, up to $10k MRR).
- Optional but recommended: Plausible Analytics (https://plausible.io) for privacy-first page-level conversion funnels.

## Steps

1. **Decide on your single dashboard surface.**
   Pick one: Notion database table, Google Sheets, or ChartMogul free tier. All three work; pick what you already have open all day. The point is one URL you open on Monday, not five tabs.
   - Notion: create a database named `Weekly Metrics` with columns: `Week`, `MRR ($)`, `Paid signups`, `Churn rate (%)`, `NPS`, `Free→Paid (%)`.
   - Google Sheets: same columns in row 1, freeze row 1, format column C as currency.
   - ChartMogul: connects to Stripe directly and calculates MRR + churn automatically; you add NPS and signups columns manually.

2. **Wire MRR from Stripe.**
   - Open https://dashboard.stripe.com/revenue → "Monthly recurring revenue" card shows current MRR.
   - If you use ChartMogul: go to https://app.chartmogul.com → Data Sources → Add Stripe. ChartMogul pulls MRR, churn MRR, and new MRR automatically after OAuth.
   - If you use Notion/Sheets: every Monday, read the Stripe MRR card and paste it. You do not need a script; manual entry at this scale is acceptable until you hit $5k MRR.
   - Record: `MRR = $X` for the current week.

3. **Count paid signups per week from PostHog.**
   PostHog tracks the event `subscription_created` (or whatever you fire when Stripe's `checkout.session.completed` webhook fires). If you have not wired the webhook yet:
   ```python
   # In your Stripe webhook handler (Django/Flask/FastAPI):
   import posthog
   posthog.capture(
       distinct_id=customer_email,
       event="subscription_created",
       properties={"plan": price_id, "mrr": amount_cents / 100}
   )
   ```
   In PostHog → Insights → Trends: select event `subscription_created`, time range = last 7 days, breakdown = none. The resulting count is your weekly paid signups. Paste to dashboard.

4. **Calculate churn rate.**
   Churn rate (%) = (customers lost this month / customers at start of month) × 100.
   - In Stripe: go to https://dashboard.stripe.com/subscriptions → filter "Canceled" → set date range to the current month. Count = customers lost.
   - In Stripe: go to Customers → filter Active subscriptions at the start of the month. Count = starting customers.
   - If using ChartMogul: the "Churn Rate" card on the Overview page calculates this automatically.
   - Record: `Churn = X%`.
   - Healthy range for a niche SaaS: ≤5% monthly. Above 8% means a retention problem needs fixing before you add features.

5. **Collect NPS via a one-question email.**
   NPS = % Promoters (9–10) − % Detractors (0–6). Send this email to active paid users 14 days after their first charge:
   ```
   Subject: Quick question about <YourProduct>
   Body:
   Hi <first_name>,

   On a scale of 0–10, how likely are you to recommend <YourProduct>
   to a friend or colleague?

   Reply with your number — that's all I need.

   — <Your name>
   ```
   Collect replies in a spreadsheet. Every Monday, count your last 30 replies:
   - Promoters: 9–10
   - Passives: 7–8
   - Detractors: 0–6
   - NPS = (Promoters / Total) × 100 − (Detractors / Total) × 100
   If you have fewer than 10 responses, record "N/A" — do not calculate NPS from 3 replies.
   Automate delivery with your email sender's trigger API when the `subscription_created` event fires; set a 14-day delay.

6. **Track free-to-paid conversion rate.**
   Conversion (%) = (new paid customers this week / new free signups this week) × 100.
   - New paid customers: from Step 3 (PostHog `subscription_created` count).
   - New free signups: in PostHog → Insights → Trends → event `user_signed_up` (or equivalent), last 7 days.
   - Paste ratio to dashboard. If you use Plausible, you can also track the `/checkout` page visit-to-completion funnel as a proxy.
   - Healthy range: 3–8% for product-led freemium. Below 2% means your upgrade trigger or pricing page needs work.

7. **Set up a Monday 15-minute review ritual.**
   Create a recurring calendar block every Monday at 09:00. In the block:
   - Open your dashboard (one URL).
   - Paste this week's five numbers (Steps 2–6 take <10 minutes combined once wired).
   - Compare to the prior week. If any metric moved more than 20% in either direction, write one sentence on why before closing the tab.
   - If churn > 8% or free→paid < 2%, open PostHog → Session recordings → filter users who churned this month → watch 3 recordings before building anything new.

## Verify

Open your dashboard URL and confirm all five columns have a non-null value for the current week:

```
MRR ($)       — from Stripe or ChartMogul
Paid signups  — from PostHog (subscription_created, last 7d)
Churn (%)     — from Stripe canceled / active ratio
NPS           — from reply log (or N/A if <10 responses)
Free→Paid (%) — PostHog signups vs subscription_created ratio
```

If any cell is blank after completing the steps, go back to the corresponding step. A dashboard with one missing column is worse than no dashboard — you will unconsciously ignore the gap.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| PostHog shows zero `subscription_created` events | Webhook handler fires but PostHog capture call is not reached | Add a `print` / log line immediately before the `posthog.capture()` call; check your server logs for the Stripe webhook delivery. Verify PostHog project API key is correct. |
| Stripe MRR card shows $0 after adding a subscriber | Subscriber is on a trial or one-time payment, not a recurring subscription | Check the subscription in Stripe dashboard → confirm `status=active` and `plan.interval=month`. One-time payments do not count toward MRR. |
| ChartMogul "pending" data source for >1h | OAuth token is stale or Stripe Connect permissions changed | Disconnect and reconnect the Stripe data source in ChartMogul → Data Sources. |
| NPS replies come in but the score seems suspiciously high | Recency bias — only happy users reply to email | Add a follow-up reminder 7 days later to non-responders; aim for ≥20% response rate before trusting the NPS value. |
| Free→paid conversion is 0% but you know users converted | `user_signed_up` event fires before email verification, so "free signups" includes bots | Filter PostHog `user_signed_up` to `properties.email_verified = true`, or use `onboarding_completed` if you have it. |
| Dashboard has five numbers but nobody looks at it | Ritual not protected — review block gets pushed | Move the calendar block to a fixed time with no exceptions for 4 weeks; after that it becomes a habit. Put the dashboard URL in your browser's pinned tabs. |

## Next

- Run `backlog-hygiene` after your first three Monday reviews — the churn and conversion signals often surface features worth re-prioritizing.
- When free→paid conversion drops below 2% for two consecutive weeks, run a session-recording audit in PostHog before adding any new features.
- Upgrade to ChartMogul Starter ($100/mo) when you surpass $10k MRR — the cohort retention charts and MRR movement waterfall become worth the cost.

## References

- [knowledge/solo/product/product-operations/product-analytics](../../../knowledge/solo/product/product-operations/product-analytics) — the AARRR metric categories (Acquisition, Activation, Retention, Revenue) map directly to the five KPIs in this playbook: MRR and signups cover Revenue/Acquisition, churn covers Retention, NPS covers qualitative Engagement, and free→paid covers Activation.
