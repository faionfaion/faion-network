---
name: churn-intervention
description: Detect cancellation signals early and intervene with targeted emails and exit surveys before a user leaves.
tier: solo
group: launch-operations
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have three automated churn guardrails in place: a daily SQL job that flags inactive users at 7 days and 14 days, a Stripe webhook listener that catches `customer.subscription.updated` (cancellation scheduled), and an exit-survey URL wired into your cancel page — plus a quarterly cohort retention review you can run in 15 minutes.

## Prerequisites

- A SaaS product with Stripe Billing (subscriptions, not one-off payments).
- A PostgreSQL database with a `users` table that has `last_login_at` (or equivalent activity timestamp).
- An ESP account capable of transactional sends: [Loops](https://loops.so), [Resend](https://resend.com), or [Postmark](https://postmarkapp.com).
- Python 3.11+ or Node 20+ on your server for the webhook listener.
- Completed [customer-onboarding-email](../customer-onboarding-email/playbook.md) — verified sending domain (SPF + DKIM) required.
- Stripe CLI installed locally for webhook testing: `brew install stripe/stripe-cli/stripe`.

## Steps

### 1. Define your three churn signals

Use these definitions verbatim — the SQL in Step 2 assumes them:

| Signal | Trigger | Severity |
|--------|---------|----------|
| **Silence-7** | No login for 7 days | Warm |
| **Silence-14** | No login for 14 days | Hot |
| **Downgrade event** | Stripe `customer.subscription.updated` where `previous_attributes.items` had higher `unit_amount` | Hot |
| **Cancel scheduled** | Stripe `customer.subscription.updated` where `cancel_at_period_end = true` | Critical |
| **Negative-sentiment ticket** | Support ticket body matches word list below | Hot |

Negative-sentiment word list (seed, extend as you learn):
```
cancel, refund, disappointed, not working, waste, switching, too expensive,
competitor, unsubscribe, delete my account, close account
```

### 2. Wire the daily SQL detector

Run this query once per day (cron at 08:00 UTC). Replace `myapp` with your schema name.

```sql
-- silence_detector.sql
-- Returns users in Silence-7 and Silence-14 windows
SELECT
    u.id,
    u.email,
    u.first_name,
    u.plan,
    u.last_login_at,
    CURRENT_DATE - u.last_login_at::date AS days_silent,
    CASE
        WHEN CURRENT_DATE - u.last_login_at::date BETWEEN 7 AND 13 THEN 'silence-7'
        WHEN CURRENT_DATE - u.last_login_at::date = 14              THEN 'silence-14'
    END AS churn_signal
FROM myapp.users u
JOIN myapp.subscriptions s ON s.user_id = u.id
WHERE
    s.status = 'active'
    AND u.last_login_at < NOW() - INTERVAL '7 days'
    AND u.last_login_at >= NOW() - INTERVAL '15 days'
    AND u.unsubscribed_at IS NULL
ORDER BY days_silent DESC;
```

Schedule with cron (or your task runner):

```bash
# /etc/cron.d/churn-detector
0 8 * * * deploy psql $DATABASE_URL -f /srv/myapp/scripts/silence_detector.sql -t --no-align -F',' | python3 /srv/myapp/scripts/enqueue_churn_emails.py
```

`enqueue_churn_emails.py` reads each row, looks up the `churn_signal`, and fires the correct ESP API call (see Step 4).

### 3. Set up the Stripe webhook listener

Create a Stripe webhook endpoint at `https://api.myapp.com/webhooks/stripe` listening for:

- `customer.subscription.updated`
- `customer.subscription.deleted`

Minimal Python (Flask) example:

```python
# webhooks/stripe_handler.py
import stripe
import os
from flask import Flask, request, abort
from churn_emails import send_cancel_alert

app = Flask(__name__)
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]

@app.route("/webhooks/stripe", methods=["POST"])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        abort(400)

    if event["type"] == "customer.subscription.updated":
        sub = event["data"]["object"]
        prev = event["data"].get("previous_attributes", {})
        if sub.get("cancel_at_period_end") and not prev.get("cancel_at_period_end"):
            # cancel scheduled — trigger critical path
            send_cancel_alert(sub["customer"], signal="cancel-scheduled")
        elif "items" in prev:
            # possible downgrade — compare amounts
            old_amount = prev["items"]["data"][0]["price"]["unit_amount"]
            new_amount = sub["items"]["data"][0]["price"]["unit_amount"]
            if new_amount < old_amount:
                send_cancel_alert(sub["customer"], signal="downgrade")

    return "", 200
```

Register the endpoint in the Stripe Dashboard under Developers → Webhooks, or via CLI:

```bash
stripe listen --forward-to localhost:5000/webhooks/stripe  # dev
stripe webhooks create --url https://api.myapp.com/webhooks/stripe \
  --events customer.subscription.updated,customer.subscription.deleted  # prod
```

### 4. Write the automated intervention emails

**Silence-7 email** (automated, sent by `enqueue_churn_emails.py`):

Subject: `Still figuring things out, <first_name>?`

```
Hi <first_name>,

Noticed you haven't logged into <product-name> in a week. Sometimes the
first week is the hardest — here's the one thing most users do to unlock value:

→ [<high-value action>](https://myapp.com/onboarding/step-2)

If something got in the way, hit reply. I read every message.

— <founder-name>
```

**Silence-14 email** (personal, from founder's real address — do NOT use noreply@):

Subject: `Quick question about <product-name>`

```
Hi <first_name>,

It's been two weeks since you logged in. Before I assume things aren't
working for you, I'd love to know what happened.

Two options:
1. [Pick a 15-minute call](https://cal.com/<your-handle>/15min) — I'll fix it live.
2. Hit reply with one line: what stopped you from using <product-name>?

No pressure. Your answer helps me build something better.

— <founder-name>
```

Send this one from your personal address via your ESP's "from" override, not a transactional queue. Silence-14 converts best when it reads like a human wrote it at 9am.

**Cancel-scheduled email** (triggered by Stripe webhook, within 5 minutes):

Subject: `Before you go — can I ask one thing?`

```
Hi <first_name>,

I saw you cancelled <product-name> (renewal on <cancel_date>). I'm sorry
it didn't work out.

One question: what was the main reason?

→ [Take the 2-minute exit survey](https://myapp.com/exit-survey?uid=<user_id>)

If it's pricing, I have options. Reply and let's talk.

— <founder-name>
```

### 5. Add the exit survey to your cancel page

Use [Tally](https://tally.so) (free tier covers this) or a plain HTML form posted to your backend.

Tally setup:
1. Create a new form at https://tally.so/forms.
2. Add these four questions:
   - "What was the main reason you cancelled?" (multiple choice: Too expensive / Missing feature / Not using it / Switching to competitor / Other)
   - "What would have made you stay?" (long text, optional)
   - "Would you come back if we added ___?" (long text, optional)
   - "May we follow up with you?" (yes/no)
3. Embed the form URL as a redirect on your cancel confirmation page: `https://myapp.com/cancel/confirmed → https://tally.so/r/<form-id>?uid=<user_id>`.

Alternative (plain HTML form → your backend):

```html
<form action="https://api.myapp.com/exit-survey" method="post">
  <input type="hidden" name="user_id" value="{{ user.id }}">
  <label>Main reason for cancelling:</label>
  <select name="reason">
    <option value="price">Too expensive</option>
    <option value="missing-feature">Missing a feature</option>
    <option value="not-using">Not using it enough</option>
    <option value="competitor">Switching to a competitor</option>
    <option value="other">Other</option>
  </select>
  <label>What would have made you stay? (optional)</label>
  <textarea name="feedback" rows="3"></textarea>
  <button type="submit">Submit</button>
</form>
```

### 6. Run the quarterly cohort retention review

Schedule 15 minutes at the end of each quarter. Run this SQL against your production database:

```sql
-- cohort_retention.sql
-- Monthly cohort retention: % of users active 30 / 60 / 90 days after signup
WITH cohorts AS (
    SELECT
        DATE_TRUNC('month', created_at)::date AS cohort_month,
        id AS user_id
    FROM myapp.users
    WHERE created_at >= NOW() - INTERVAL '12 months'
),
activity AS (
    SELECT
        c.cohort_month,
        c.user_id,
        EXTRACT(DAY FROM (l.login_at - u.created_at)) AS days_after_signup
    FROM cohorts c
    JOIN myapp.users u ON u.id = c.user_id
    JOIN myapp.login_events l ON l.user_id = c.user_id
)
SELECT
    cohort_month,
    COUNT(DISTINCT user_id)                                          AS cohort_size,
    COUNT(DISTINCT CASE WHEN days_after_signup BETWEEN 25 AND 35 THEN user_id END)
        * 100 / NULLIF(COUNT(DISTINCT user_id), 0)                  AS retained_30d_pct,
    COUNT(DISTINCT CASE WHEN days_after_signup BETWEEN 55 AND 65 THEN user_id END)
        * 100 / NULLIF(COUNT(DISTINCT user_id), 0)                  AS retained_60d_pct,
    COUNT(DISTINCT CASE WHEN days_after_signup BETWEEN 85 AND 95 THEN user_id END)
        * 100 / NULLIF(COUNT(DISTINCT user_id), 0)                  AS retained_90d_pct
FROM activity
GROUP BY cohort_month
ORDER BY cohort_month;
```

For each cohort where `retained_30d_pct` dropped more than 5 points quarter-over-quarter, open the exit survey responses from that month and look for a common theme.

## Verify

Run the silence detector manually and confirm it returns rows (or an empty result set — both are valid):

```bash
psql $DATABASE_URL -f /srv/myapp/scripts/silence_detector.sql -t --no-align -F','
```

Then fire a test event via the Stripe CLI and confirm your webhook handler returns `200` and the cancel-scheduled email appears in your ESP logs:

```bash
stripe trigger customer.subscription.updated \
  --override customer.subscription.updated:data.object.cancel_at_period_end=true
```

Check your ESP dashboard (Loops / Resend / Postmark) for a new event within 30 seconds.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `silence_detector.sql` returns 0 rows even though inactive users exist | `last_login_at` column is NULL for old records | `UPDATE myapp.users SET last_login_at = created_at WHERE last_login_at IS NULL;` then re-run; add a NOT NULL constraint going forward |
| Stripe webhook returns 400 "No signatures found" | `STRIPE_WEBHOOK_SECRET` env var is the signing secret from Stripe Dashboard, not the API key | Go to Dashboard → Webhooks → your endpoint → "Signing secret"; copy the `whsec_…` value into `STRIPE_WEBHOOK_SECRET` |
| Cancel-scheduled email arrives 2 minutes after cancel but Stripe shows no delivery | ESP DKIM not verified; email lands in spam | Check ESP sending domain settings; run `dig TXT mail._domainkey.myapp.com` — must return the DKIM TXT record |
| Cohort retention SQL returns NULL for `retained_30d_pct` | No `login_events` table — your schema logs logins differently | Replace `myapp.login_events` with your actual session/event table; change `login_at` to the right timestamp column |
| Exit-survey completion rate below 5% | Survey loads after cancellation is already confirmed — user has no incentive | Embed the survey *before* the final "Confirm cancel" button; offer a 1-month pause instead of cancellation as the CTA above the survey |

## Next

- [customer-onboarding-email](../customer-onboarding-email/playbook.md) — reduce churn at the root by activating users in week 1 before silence signals appear.
- [pricing-experiments](../pricing-experiments/playbook.md) — if exit surveys reveal price as the top cancellation reason, run a pricing experiment before adjusting list prices.
- Review `knowledge/solo/product/product-operations/product-analytics` for cohort analysis patterns to extend the quarterly review into weekly leading indicators.

## References

- [knowledge/solo/marketing/content-marketer/growth-email-marketing](../../../knowledge/solo/marketing/content-marketer/growth-email-marketing) — email sequencing and sender-reputation rules that govern the Silence-7 and Silence-14 drip timing in Steps 4 and 5.
- [knowledge/solo/product/product-operations/feedback-management](../../../knowledge/solo/product/product-operations/feedback-management) — structures the exit-survey question design and the quarterly cohort review loop in Steps 5 and 6 so feedback routes to product decisions, not a dead inbox.
- [knowledge/solo/product/product-operations/product-analytics](../../../knowledge/solo/product/product-operations/product-analytics) — cohort retention calculation methodology underpinning the SQL query in Step 6 and the 5-point drop threshold for action.
