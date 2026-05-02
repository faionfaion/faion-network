---
name: payment-flow
description: Wire Stripe Checkout end-to-end — pricing page to webhook to activation email — with idempotency, grace period, and retry logic.
tier: solo
group: launch-operations
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working payment flow: visitors click a pricing-page button, land on Stripe Checkout, pay, and your server receives the webhook, updates `users.subscription_status` in your database, and sends an activation email. Failed payments enter a grace period with automatic retries, duplicate webhook deliveries are deduplicated, refunds and prorated upgrades are handled.

## Prerequisites

- A Stripe account at https://dashboard.stripe.com (free signup).
- A product and price already created in the Stripe Dashboard (or via CLI).
- Python 3.11+ backend (Django or Flask); adapt library calls for Node if needed.
- `stripe` Python package installed: `pip install stripe`.
- A `users` table with a `subscription_status` column (`TEXT`, default `'inactive'`).
- A transactional email service configured (e.g. Resend, SendGrid) — the activation email step uses it.
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, and `STRIPE_PRICE_ID` in your environment (`.env` file, never committed).
- A publicly reachable webhook endpoint during development: use `stripe listen --forward-to localhost:8000/webhooks/stripe/` from Stripe CLI.

## Steps

### 1. Install and configure the Stripe client

```python
# payments/stripe_client.py
import os
import stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
```

Never hard-code the key. Load from `os.environ` so the same code runs in dev and prod.

### 2. Build the Checkout Session endpoint

```python
# payments/views.py  (Django function-based view)
import stripe
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

PRICE_ID = os.environ["STRIPE_PRICE_ID"]   # e.g. price_1PqzAbCdEfGhIjKl

@login_required
@require_POST
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": PRICE_ID, "quantity": 1}],
        success_url="https://myapp.io/dashboard?checkout=success",
        cancel_url="https://myapp.io/pricing?checkout=cancelled",
        customer_email=request.user.email,
        client_reference_id=str(request.user.pk),   # ties session → user
        subscription_data={
            "trial_period_days": 0,              # set >0 to add a free trial
        },
    )
    return JsonResponse({"url": session.url})
```

### 3. Add the pricing-page button

```html
<!-- pricing.html — inside your pricing card -->
<button
  data-plan="solo"
  onclick="startCheckout()"
  class="btn-primary">
  Get Solo — $19/mo
</button>

<script>
async function startCheckout() {
  const res = await fetch('/payments/checkout/', {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
  });
  const { url } = await res.json();
  window.location.href = url;   // redirect to Stripe-hosted page
}
</script>
```

No card details ever touch your server. Stripe handles PCI compliance.

### 4. Create the webhook endpoint

```python
# payments/views.py  (continued)
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from myapp.models import User

WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return JsonResponse({"error": "invalid"}, status=400)

    _dispatch_event(event)
    return JsonResponse({"received": True})


def _dispatch_event(event):
    etype = event["type"]
    if etype == "checkout.session.completed":
        _handle_checkout_completed(event["data"]["object"])
    elif etype == "invoice.paid":
        _handle_invoice_paid(event["data"]["object"])
    elif etype == "invoice.payment_failed":
        _handle_payment_failed(event["data"]["object"])
    elif etype in ("customer.subscription.deleted", "customer.subscription.updated"):
        _handle_subscription_change(event["data"]["object"])
```

### 5. Update the database idempotently on checkout completion

```python
from django.utils import timezone

def _handle_checkout_completed(session):
    user_id = session.get("client_reference_id")
    stripe_customer_id = session.get("customer")
    stripe_subscription_id = session.get("subscription")
    if not user_id:
        return   # safety: no user linked

    with transaction.atomic():
        updated = User.objects.filter(pk=user_id).update(
            subscription_status="active",
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
            activated_at=timezone.now(),
        )
    if updated:
        _send_activation_email(user_id)
```

Idempotency: `User.objects.filter(pk=...).update(...)` is a no-op if called twice — Stripe may deliver the same event more than once. No duplicate emails: check `activated_at` before sending.

### 6. Send the activation email

```python
import resend   # pip install resend; swap for sendgrid/postmark as needed

def _send_activation_email(user_id):
    user = User.objects.get(pk=user_id)
    if user.activation_email_sent:
        return   # idempotency guard

    resend.Emails.send({
        "from": "hello@myapp.io",
        "to": user.email,
        "subject": "Your Solo plan is active",
        "html": f"<p>Hi {user.first_name}, you're all set. "
                f"<a href='https://myapp.io/dashboard'>Open your dashboard</a>.</p>",
    })
    User.objects.filter(pk=user_id).update(activation_email_sent=True)
```

### 7. Handle failed payments and the grace period

```python
GRACE_PERIOD_DAYS = 7

def _handle_payment_failed(invoice):
    subscription_id = invoice.get("subscription")
    if not subscription_id:
        return
    user = User.objects.filter(
        stripe_subscription_id=subscription_id
    ).first()
    if not user:
        return

    attempt = invoice.get("attempt_count", 1)
    if attempt == 1:
        # Start grace period — keep access, notify user
        User.objects.filter(pk=user.pk).update(
            subscription_status="grace",
            grace_until=timezone.now() + timezone.timedelta(days=GRACE_PERIOD_DAYS),
        )
        _send_payment_failed_email(user, attempt=1)
    else:
        # Subsequent failure inside grace period — still notify
        _send_payment_failed_email(user, attempt=attempt)


def _handle_invoice_paid(invoice):
    # Recovers from grace period when retry succeeds
    subscription_id = invoice.get("subscription")
    User.objects.filter(
        stripe_subscription_id=subscription_id
    ).update(
        subscription_status="active",
        grace_until=None,
    )
```

Stripe retries automatically on the schedule set in your Dashboard under "Subscriptions → Retry schedule" (default: day 1, 3, 5, 7). After all retries fail, Stripe fires `customer.subscription.deleted`.

### 8. Cancel subscription on deletion

```python
def _handle_subscription_change(subscription):
    sub_id = subscription["id"]
    status = subscription["status"]   # "canceled", "past_due", "active", etc.

    mapping = {
        "active": "active",
        "past_due": "grace",
        "canceled": "inactive",
        "unpaid": "inactive",
    }
    db_status = mapping.get(status, "inactive")
    User.objects.filter(stripe_subscription_id=sub_id).update(
        subscription_status=db_status
    )
```

### 9. Handle refunds

```python
# Stripe fires charge.refunded — handle in _dispatch_event
def _handle_refund(charge):
    # Full refund → cancel subscription immediately
    customer_id = charge.get("customer")
    if charge.get("amount_refunded") >= charge.get("amount"):
        User.objects.filter(stripe_customer_id=customer_id).update(
            subscription_status="inactive"
        )
        # Optionally cancel the Stripe subscription too:
        user = User.objects.filter(stripe_customer_id=customer_id).first()
        if user and user.stripe_subscription_id:
            stripe.Subscription.cancel(user.stripe_subscription_id)
```

Add `"charge.refunded": _handle_refund` to `_dispatch_event`.

### 10. Handle prorated upgrades

```python
def upgrade_subscription(user, new_price_id):
    """Call from your billing-settings view when the user clicks 'Upgrade'."""
    subscription = stripe.Subscription.retrieve(user.stripe_subscription_id)
    stripe.Subscription.modify(
        user.stripe_subscription_id,
        items=[{
            "id": subscription["items"]["data"][0]["id"],
            "price": new_price_id,
        }],
        proration_behavior="create_prorations",  # charges/credits the diff immediately
    )
    # The resulting invoice.paid event updates the DB via the webhook handler.
```

### 11. Register the URL

```python
# urls.py
from django.urls import path
from payments import views

urlpatterns = [
    path("payments/checkout/", views.create_checkout_session),
    path("webhooks/stripe/", views.stripe_webhook),
    path("billing/upgrade/", views.upgrade_plan_view),
]
```

### 12. Test locally with Stripe CLI

```bash
stripe listen --forward-to localhost:8000/webhooks/stripe/
# In another terminal:
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
stripe trigger invoice.paid
```

Watch your server logs. Each event should log a 200 response.

## Verify

Create a test Checkout Session using Stripe's test card `4242 4242 4242 4242`, expiry `12/34`, CVC `123`. After completing checkout, run:

```bash
python manage.py shell -c "
from myapp.models import User
u = User.objects.get(email='<your-test-email>')
print(u.subscription_status, u.stripe_subscription_id)
"
```

Expected output: `active sub_...`. Also verify the activation email arrives in your inbox.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `400 Webhook Error: No signatures found` | `STRIPE_WEBHOOK_SECRET` wrong or missing | Re-copy the secret from `stripe listen` output (dev) or Dashboard → Webhooks → Reveal secret (prod); it starts with `whsec_` |
| `checkout.session.completed` fires but `client_reference_id` is `None` | Session created without `client_reference_id` | Pass `client_reference_id=str(request.user.pk)` in `stripe.checkout.Session.create()`; requires user to be authenticated before redirect |
| Duplicate activation emails | Webhook delivered twice and `activation_email_sent` guard not set | Ensure `_send_activation_email` sets `activation_email_sent=True` atomically before returning; use `select_for_update()` if concurrent workers possible |
| Grace period never ends even after retries succeed | `invoice.paid` handler not registered | Add `"invoice.paid": _handle_invoice_paid` in `_dispatch_event`; also enable the event in the Stripe webhook config in Dashboard |
| Prorated upgrade creates unexpected invoice | `proration_behavior="none"` set elsewhere | Remove conflicting overrides; `"create_prorations"` is the correct value for immediate billing of the price difference |
| `StripeInvalidRequestError: No such customer` on upgrade | User's `stripe_customer_id` is stale (test/prod mix) | Ensure you use matching Stripe environments; test keys produce `cus_test_...`, prod keys produce `cus_...` |

## Next

- Add the [solo/customer-onboarding-email](../customer-onboarding-email/playbook.md) playbook to extend the activation email sequence with a drip campaign.
- Set up dunning emails (payment-failed notice series) using your transactional email provider's automation flows — triggered by the `grace` status the webhook sets.
- Move to metered billing by replacing `mode="subscription"` with `mode="subscription"` + `usage_type="metered"` on the price, then report usage via `stripe.SubscriptionItem.create_usage_record()`.

## References

- [knowledge/solo/dev/api-developer/api-authentication](../../../knowledge/solo/dev/api-developer/api-authentication) — Stripe webhook signature verification (`Webhook.construct_event`) follows the HMAC-SHA256 pattern this methodology defines; the idempotency-key pattern for deduplicating duplicate deliveries is drawn directly from its API auth primitives section.
- [knowledge/solo/dev/api-developer/api-error-handling](../../../knowledge/solo/dev/api-developer/api-error-handling) — retry-safe handlers and grace-period state machine in Steps 7–8 apply the error-boundary and partial-failure patterns from this methodology; specifically, the `attempt_count` branching logic follows its "escalating fallback" model.
