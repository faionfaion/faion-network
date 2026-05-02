---
name: stripe-integration-basics
description: Sign up for Stripe, install the SDK, create a Product and Price, wire a Checkout Session, handle the webhook, and record payments in your database.
tier: solo
group: launch-operations
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Stripe Checkout flow: a button on your site redirects customers to a hosted Stripe payment page, and a webhook endpoint on your server receives the `checkout.session.completed` event and writes a confirmed payment record to your database.

## Prerequisites

- A Stripe account (free signup at https://stripe.com).
- Node.js 18+ **or** Python 3.10+ installed locally.
- A web server you control (Express, FastAPI, Django, etc.) reachable by Stripe webhooks — or the Stripe CLI for local testing.
- A database with a `payments` table (or equivalent). Any SQL or NoSQL store works.
- `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` env vars available to your server process.

## Steps

1. **Create your Stripe account** at https://stripe.com. Complete the activation form (business name, bank details). Until activation you stay in test mode; live payments require it.

2. **Copy your test API keys.** In the Stripe Dashboard go to Developers → API keys. Copy the **Secret key** (`sk_test_...`) into your `.env` as `STRIPE_SECRET_KEY`. Never commit this value.

3. **Install the Stripe SDK.**

   Node:
   ```bash
   npm install stripe
   ```

   Python:
   ```bash
   pip install stripe
   ```

4. **Create a Product and Price in the dashboard.** Go to Products → Add product. Set a name (e.g., `Solo Plan`), pricing model `Standard pricing`, price `$19.00 USD`, billing `One time`. Save. Copy the **Price ID** (`price_...`) — you need it in the next step.

5. **Create a Checkout Session on your server** and redirect the customer to the hosted page.

   Node (Express):
   ```js
   const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

   app.post('/create-checkout-session', async (req, res) => {
     const session = await stripe.checkout.sessions.create({
       payment_method_types: ['card'],
       line_items: [{ price: 'price_1PxxxxYYYYZZZZ', quantity: 1 }],
       mode: 'payment',
       success_url: 'https://myapp.com/thank-you?session_id={CHECKOUT_SESSION_ID}',
       cancel_url: 'https://myapp.com/pricing',
     });
     res.redirect(303, session.url);
   });
   ```

   Python (FastAPI):
   ```python
   import stripe, os
   from fastapi import APIRouter
   from fastapi.responses import RedirectResponse

   stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
   router = APIRouter()

   @router.post("/create-checkout-session")
   async def create_checkout_session():
       session = stripe.checkout.Session.create(
           payment_method_types=["card"],
           line_items=[{"price": "price_1PxxxxYYYYZZZZ", "quantity": 1}],
           mode="payment",
           success_url="https://myapp.com/thank-you?session_id={CHECKOUT_SESSION_ID}",
           cancel_url="https://myapp.com/pricing",
       )
       return RedirectResponse(session.url, status_code=303)
   ```

   Replace `price_1PxxxxYYYYZZZZ` with the Price ID from Step 4 and `myapp.com` with your actual domain.

6. **Wire the success and cancel URLs.** Add the two routes:
   - `GET /thank-you` — show a "Payment received" page. Read `session_id` from the query string if you want to display order details.
   - `GET /pricing` — existing page. No changes needed.

7. **Set up the Stripe webhook.** Go to Developers → Webhooks → Add endpoint. Set the URL to `https://myapp.com/webhook/stripe`. Select event `checkout.session.completed`. Save. Copy the **Signing secret** (`whsec_...`) into `.env` as `STRIPE_WEBHOOK_SECRET`.

8. **Handle the webhook and record the payment.**

   Node (Express — must use raw body parser for this route):
   ```js
   const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

   app.post('/webhook/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
     const sig = req.headers['stripe-signature'];
     let event;
     try {
       event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
     } catch (err) {
       return res.status(400).send(`Webhook Error: ${err.message}`);
     }

     if (event.type === 'checkout.session.completed') {
       const session = event.data.object;
       await db.query(
         'INSERT INTO payments (stripe_session_id, amount_total, currency, customer_email, created_at) VALUES ($1, $2, $3, $4, NOW())',
         [session.id, session.amount_total, session.currency, session.customer_details?.email]
       );
     }
     res.json({ received: true });
   });
   ```

   Python (FastAPI):
   ```python
   from fastapi import Request, HTTPException
   import stripe, os

   @router.post("/webhook/stripe")
   async def stripe_webhook(request: Request):
       payload = await request.body()
       sig = request.headers.get("stripe-signature")
       try:
           event = stripe.Webhook.construct_event(
               payload, sig, os.environ["STRIPE_WEBHOOK_SECRET"]
           )
       except stripe.error.SignatureVerificationError:
           raise HTTPException(status_code=400, detail="Invalid signature")

       if event["type"] == "checkout.session.completed":
           session = event["data"]["object"]
           await db.execute(
               "INSERT INTO payments (stripe_session_id, amount_total, currency, customer_email) VALUES ($1, $2, $3, $4)",
               session["id"], session["amount_total"], session["currency"],
               session["customer_details"]["email"]
           )
       return {"received": True}
   ```

9. **Test end-to-end with the test card.** Click your payment button, enter card number `4242 4242 4242 4242`, any future expiry (e.g., `12/28`), CVC `424`, any postal code. The payment should complete and redirect to `/thank-you`.

10. **Install the Stripe CLI for local webhook testing** (optional but recommended before deploy):

    ```bash
    stripe listen --forward-to localhost:8000/webhook/stripe
    ```

    This tunnels live test events to your local server.

## Verify

Run the following from your terminal (replace the base URL and key):

```bash
curl -s https://api.stripe.com/v1/checkout/sessions \
  -u sk_test_YOUR_KEY: \
  -d "limit=1" | python3 -m json.tool | grep '"status"'
```

Expected output contains `"status": "complete"` for a session completed with the test card. If no sessions exist yet, the array is empty — complete one test payment first.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `StripeInvalidRequestError: No such price` | Price ID typo or wrong env (live key vs test Price) | Copy Price ID from Dashboard directly; ensure `sk_test_` key is used with `price_` IDs from test mode |
| Webhook returns 400 `Invalid signature` | Raw body not preserved (body parser consumed it before the webhook handler) | In Express, mount `express.raw()` on `/webhook/stripe` before `express.json()` on all other routes; in FastAPI use `await request.body()` not `await request.json()` |
| `success_url` never loads after payment | Missing `{CHECKOUT_SESSION_ID}` placeholder in URL or route not registered | Confirm the placeholder is literally `{CHECKOUT_SESSION_ID}` (Stripe substitutes it at redirect time); check your route is mounted |
| Payment page says "Your card was declined" with `4242` | Test card used against a live-mode session | Verify `STRIPE_SECRET_KEY` starts with `sk_test_`; test cards only work in test mode |
| Webhook fires but no DB row written | DB connection error swallowed silently | Wrap the INSERT in try/catch; log the error; always return `200` to Stripe regardless so it stops retrying |

## Next

- `customer-onboarding-email` — send a transactional confirmation email immediately after `checkout.session.completed`.
- `pricing-experiments` — create multiple Prices on the same Product and A/B test price points without code changes.
- Upgrade path: the `api-key-auth` playbook (solo/api-design) adds per-customer API keys provisioned on payment success.

## References

- [knowledge/solo/dev/api-developer/api-authentication](../../../knowledge/solo/dev/api-developer/api-authentication) — Stripe webhook signature verification is a specialized HMAC request-authentication pattern; this methodology covers the signing contract that backs Step 8's `constructEvent` call.
- [knowledge/solo/dev/api-developer/api-error-handling](../../../knowledge/solo/dev/api-developer/api-error-handling) — error response shapes for the webhook endpoint (400 on bad signature, 200 always on success) follow the error-handling contract defined here; applied directly in Step 8.
