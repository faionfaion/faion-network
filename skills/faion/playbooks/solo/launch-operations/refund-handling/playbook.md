---
name: refund-handling
description: Define a 30-day no-questions-asked refund policy, automate Stripe refunds, write a concise refund email, and exit-flag accounts to block re-subscription for 90 days.
tier: solo
group: launch-operations
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a legally sound 30-day refund policy displayed on your pricing page, checkout, and footer; a Stripe-automated refund endpoint (or a documented manual flow); a copy-paste refund email template that is concise, apology-free, and asks one why-question; and a database flag that prevents refunded users from re-subscribing within 90 days.

## Prerequisites

- A Stripe account at https://dashboard.stripe.com with at least one live subscription product.
- Python 3.11+ backend (Django); adapt calls for Flask/Node as needed.
- `stripe` package installed: `pip install stripe`.
- A `users` table with `subscription_status`, `stripe_customer_id`, and `stripe_subscription_id` columns — the `payment-flow` playbook sets these up.
- A transactional email service configured (Resend, SendGrid, or Postmark).
- `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in your environment (never committed).
- Policy copy published at a stable URL on your site (Step 1 covers this).

## Steps

### 1. Write the policy and add it to your site

Add this block to your pricing page, checkout confirmation page, and site footer:

```
30-day money-back guarantee. If you are not satisfied within 30 days of your first payment,
contact support@myapp.io and we will issue a full refund — no questions asked.
Refunds apply to the first billing period only. Renewals are not eligible.
```

Link the phrase "30-day money-back guarantee" to `/refund-policy` and publish a standalone policy page at that URL. Keep the wording identical across all three surfaces.

### 2. Add the refund_flagged column to your users table

```python
# migrations/0012_add_refund_flag.py
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [("accounts", "0011_add_stripe_fields")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="refund_flagged_at",
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="user",
            name="refund_count",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
```

Run `python manage.py migrate`.

### 3. Build the refund endpoint

```python
# billing/views.py
import stripe
import os
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import User

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
REFUND_WINDOW_DAYS = 30
RESUBSCRIBE_BLOCK_DAYS = 90


@login_required
@require_POST
def request_refund(request):
    user = request.user

    # Guard: already refunded once → manual review path
    if user.refund_count >= 1:
        return JsonResponse(
            {"error": "refund_already_issued",
             "message": "You have already received a refund. "
                        "Contact support@myapp.io for manual review."},
            status=400,
        )

    # Guard: outside 30-day window
    if not user.activated_at or (timezone.now() - user.activated_at).days > REFUND_WINDOW_DAYS:
        return JsonResponse(
            {"error": "outside_window",
             "message": "Refund window has expired (30 days from first payment)."},
            status=400,
        )

    # Guard: no active subscription to refund
    if not user.stripe_subscription_id:
        return JsonResponse({"error": "no_subscription"}, status=400)

    # Retrieve the latest paid invoice for this subscription
    invoices = stripe.Invoice.list(
        subscription=user.stripe_subscription_id,
        status="paid",
        limit=1,
    )
    if not invoices.data:
        return JsonResponse({"error": "no_paid_invoice"}, status=400)

    invoice = invoices.data[0]
    charge_id = invoice.get("charge")

    # Issue the refund via Stripe API
    refund = stripe.Refund.create(
        charge=charge_id,
        reason="requested_by_customer",
    )

    # Cancel the subscription (no proration — refund covers it)
    stripe.Subscription.cancel(user.stripe_subscription_id)

    # Update local state
    User.objects.filter(pk=user.pk).update(
        subscription_status="refunded",
        refund_flagged_at=timezone.now(),
        refund_count=user.refund_count + 1,
    )

    return JsonResponse({"refund_id": refund.id, "status": "issued"})
```

Register the URL:

```python
# urls.py
path("billing/refund/", billing_views.request_refund),
```

### 4. Add the 90-day re-subscription block

Check this guard in your checkout session creation view (from `payment-flow` playbook):

```python
# billing/views.py — inside create_checkout_session, before stripe.checkout.Session.create
from datetime import timedelta

if user.refund_flagged_at:
    block_until = user.refund_flagged_at + timedelta(days=RESUBSCRIBE_BLOCK_DAYS)
    if timezone.now() < block_until:
        days_remaining = (block_until - timezone.now()).days
        return JsonResponse(
            {"error": "resubscribe_blocked",
             "message": f"Re-subscription is not available for {days_remaining} more days."},
            status=403,
        )
```

This runs entirely server-side. Never rely on a frontend-only guard for this.

### 5. Handle the refund webhook (idempotency)

Stripe fires `charge.refunded` asynchronously. Add the handler so your DB stays consistent even if the API call in Step 3 succeeds but the response is lost:

```python
# billing/webhook_handlers.py
from accounts.models import User
from django.utils import timezone


def handle_charge_refunded(charge):
    """Idempotent: safe to call multiple times for the same charge."""
    customer_id = charge.get("customer")
    if not customer_id:
        return

    amount = charge.get("amount", 0)
    amount_refunded = charge.get("amount_refunded", 0)
    full_refund = amount_refunded >= amount

    if full_refund:
        updated = User.objects.filter(
            stripe_customer_id=customer_id,
            subscription_status__in=("active", "grace"),
        ).update(
            subscription_status="refunded",
            refund_flagged_at=timezone.now(),
        )
        # Only increment refund_count if the row was not already flagged
        if updated:
            User.objects.filter(
                stripe_customer_id=customer_id,
                refund_count=0,
            ).update(refund_count=1)
```

Register in your webhook dispatcher:

```python
elif etype == "charge.refunded":
    handle_charge_refunded(event["data"]["object"])
```

### 6. Write and send the refund confirmation email

Send this immediately after `stripe.Refund.create()` succeeds in Step 3:

```python
import resend  # swap for sendgrid/postmark

def send_refund_email(user):
    resend.Emails.send({
        "from": "support@myapp.io",
        "to": user.email,
        "subject": "Your refund is on its way",
        "html": f"""
<p>Hi {user.first_name},</p>

<p>Your refund of <strong>$19.00</strong> has been issued and will appear on your
statement within 5–10 business days, depending on your bank.</p>

<p>Your account access ends today.</p>

<p>One question: what was the main reason you decided to cancel?
Reply to this email — your answer helps us improve.</p>

<p>— The myapp.io team</p>
""",
    })
```

Key decisions baked into this copy:
- No "sorry" or "apologize" — keeps the tone neutral and professional.
- States the exact amount and timeline upfront.
- Asks exactly one open question to capture churn signal.
- Does not offer a discount or alternative — that belongs in a separate churn-intervention flow.

### 7. Add a self-serve refund button to the billing settings page

```html
<!-- billing_settings.html -->
{% if user.subscription_status == "active" and user.activated_at %}
  {% with days_left=refund_days_remaining %}
  {% if days_left > 0 %}
  <p>Money-back guarantee: <strong>{{ days_left }} day{{ days_left|pluralize }} remaining</strong></p>
  <button
    id="btn-refund"
    onclick="requestRefund()"
    class="btn-danger-outline">
    Request refund
  </button>
  {% endif %}
  {% endwith %}
{% endif %}

<script>
async function requestRefund() {
  if (!confirm("This will cancel your subscription and issue a full refund. Continue?")) return;
  const res = await fetch("/billing/refund/", {
    method: "POST",
    headers: {"X-CSRFToken": getCookie("csrftoken")},
  });
  const data = await res.json();
  if (res.ok) {
    document.getElementById("btn-refund").remove();
    alert("Refund issued. You will receive a confirmation email.");
    window.location.href = "/";
  } else {
    alert(data.message || "Refund could not be processed. Contact support@myapp.io.");
  }
}
</script>
```

Pass `refund_days_remaining` from the view:

```python
from datetime import timedelta

def billing_settings_view(request):
    user = request.user
    days_remaining = 0
    if user.activated_at:
        elapsed = (timezone.now() - user.activated_at).days
        days_remaining = max(0, 30 - elapsed)
    return render(request, "billing_settings.html", {"refund_days_remaining": days_remaining})
```

## Verify

In Stripe test mode, create a subscription using test card `4242 4242 4242 4242` (expiry `12/34`, CVC `123`). Then call the refund endpoint:

```bash
curl -X POST https://myapp.io/billing/refund/ \
  -H "Cookie: sessionid=<your-test-session>" \
  -H "X-CSRFToken: <token>"
```

Expected JSON response: `{"refund_id": "re_...", "status": "issued"}`.

Confirm in the Stripe Dashboard under Payments → Refunds that the refund shows `succeeded`. Then check the DB:

```bash
python manage.py shell -c "
from accounts.models import User
u = User.objects.get(email='test@myapp.io')
print(u.subscription_status, u.refund_flagged_at, u.refund_count)
"
```

Expected: `refunded <datetime> 1`. Attempt checkout again — the 90-day block should return HTTP 403.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `stripe.error.InvalidRequestError: charge already refunded` | Refund endpoint called twice before webhook fires | Add a DB-level check: `if user.subscription_status == "refunded": return 400` before calling `stripe.Refund.create()` |
| Refund button still visible after refund issued | `subscription_status` not updated before page re-render | Ensure `User.objects.filter(...).update(subscription_status="refunded")` runs before the JSON response is returned; add a page reload after the fetch succeeds |
| 90-day block triggers for a user who was not refunded | `refund_flagged_at` was set by a stale migration or test seed | Audit the column: `User.objects.filter(refund_flagged_at__isnull=False).values("email", "refund_count")`; null out bad rows with `.update(refund_flagged_at=None, refund_count=0)` |
| `charge.refunded` webhook fires but handler not reached | Event type not registered in Stripe Dashboard webhook config | Go to Dashboard → Developers → Webhooks → your endpoint → Edit → add `charge.refunded` to the event list |
| Refund email sent twice | `handle_charge_refunded` called once by webhook AND once by the refund endpoint | Gate `send_refund_email()` on a `refund_email_sent` boolean field (same pattern as `activation_email_sent` in `payment-flow`) |

## Next

- Set up churn-saving logic before the refund button is shown: see [solo/launch-operations/churn-intervention](../churn-intervention/playbook.md) — offer a pause or downgrade before issuing a refund.
- Track refund rate per cohort in your analytics: `refund_count / activated_users` by week gives you a leading product-quality signal.
- Add a Stripe webhook test for `charge.refunded` to your test suite using `stripe trigger charge.refunded` to validate the idempotency handler.

## References

- [knowledge/solo/marketing/content-marketer/growth-email-marketing](../../../knowledge/solo/marketing/content-marketer/growth-email-marketing) — the refund confirmation email in Step 6 applies the single-CTA and one-question survey pattern from this methodology's transactional email templates; the "no apology" framing comes from its copy-tone guidelines for post-cancellation messages.
- [knowledge/solo/comms/communicator/difficult-conversations](../../../knowledge/solo/comms/communicator/difficult-conversations) — the decision to state the refund amount upfront and skip discount offers in Step 6 follows this methodology's principle of leading with facts and separating churn-recovery from the refund confirmation exchange.
- [knowledge/solo/marketing/content-marketer/growth-onboarding-emails](../../../knowledge/solo/marketing/content-marketer/growth-onboarding-emails) — the one open-ended why-question in the refund email is drawn from this methodology's offboarding survey pattern, which shows that a single reply-to question yields higher response rates than an embedded multi-choice form.
