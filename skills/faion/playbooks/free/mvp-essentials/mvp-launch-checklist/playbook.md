---
name: mvp-launch-checklist
description: Run a 12-gate launch-day script before flipping your MVP to public — HTTPS, signup, email, payment, error pages, analytics, support, legal, social preview, copy, mobile, and rollback.
tier: free
group: mvp-essentials
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have verified all 12 launch gates in sequence, confirmed your MVP is safe for public traffic, and have a written rollback plan ready — so you can flip the "live" switch with confidence rather than hope.

## Prerequisites

- A deployed MVP at a stable URL (e.g., `https://myapp.vercel.app` or your custom domain).
- HTTPS configured on your domain (Cloudflare or your host's free TLS).
- A real payment processor account set up (Stripe or Lemon Squeezy in test mode).
- A transactional email provider connected (Resend, SendGrid, or Postmark free tier).
- A real card to test checkout end-to-end (your own Stripe-issued test card or a real card in test mode).
- Basic analytics tool installed (PostHog, Plausible, or Umami).
- A support email address you actively monitor.
- ToS and Privacy Policy pages drafted (even one paragraph each clears the legal gate).

## Steps

Work through gates in order. Mark each gate with `[x]` in a local `LAUNCH-GATES.md` file. Do not proceed to the next gate until the current one passes.

### Gate 1 — HTTPS works end-to-end

Open a new browser tab and navigate to `http://myapp.com` (the plain HTTP version). Confirm the browser automatically redirects to `https://myapp.com` and the browser shows a padlock. Then run:

```bash
curl -I http://myapp.com
```

The response must include `301` or `302` redirect to `https://`. If you see `200` on HTTP, your redirect is not configured — add an HTTPS redirect in Cloudflare (set SSL/TLS mode to "Full (Strict)") or in your hosting dashboard.

### Gate 2 — Signup flow works in an incognito window

Open an incognito (private) window. Navigate to your signup page. Create a new account using an email address you have not used before (e.g., a `+tag` alias like `yourname+launch01@gmail.com`). Complete every step without using autofill. If any step breaks, you have found a real user bug.

### Gate 3 — Email confirmation arrives within 5 minutes

After Gate 2, check the inbox for `yourname+launch01@gmail.com`. The confirmation or welcome email should arrive within 5 minutes. If it lands in spam, open it and mark "Not spam" — but also fix the problem: add SPF, DKIM, and DMARC records for your sending domain. Most transactional providers give you these DNS records in their dashboard.

### Gate 4 — Payment flow completes on a real (test-mode) card

Log in as the user you created in Gate 2. Navigate to the upgrade or checkout page. Complete a purchase using Stripe's test card number `4242 4242 4242 4242`, any future expiry (e.g., `12/28`), any CVC, and any postal code. Confirm you see a success page or success state in the app. Check your Stripe dashboard at https://dashboard.stripe.com/test/payments — the payment should appear as "Succeeded".

### Gate 5 — Error pages exist for 404 and 500

Navigate to a URL that does not exist on your app, e.g., `https://myapp.com/this-page-does-not-exist`. You should see a custom 404 page — not a raw framework error or a blank white screen. Then temporarily trigger a 500 (or check your hosting provider's custom error page config) to confirm users see a readable message instead of a stack trace. Most hosts (Vercel, Railway, Render) let you configure a custom `404.html` or `error.html`.

### Gate 6 — Basic analytics are installed and recording

Open your analytics dashboard (PostHog at https://app.posthog.com, Plausible, or Umami). Navigate to your app in a normal (non-incognito) browser tab. Within 60 seconds, your dashboard should show at least one new page view event. If nothing appears, check that your snippet or SDK is present in the `<head>` of every page and is not blocked by an ad blocker in your own browser (test in a second browser or on a phone).

### Gate 7 — Support email is monitored and auto-replies work

Send a test email to your support address (e.g., `support@myapp.com`) from a personal account. Confirm you receive it. If you have an auto-reply configured, verify the reply arrives within 2 minutes. Add a filter or label in your inbox so support emails surface immediately — do not let them fall into a general inbox during launch week.

### Gate 8 — ToS and Privacy Policy are linked from the footer

Open your app's homepage. Scroll to the footer. Confirm there are clickable links to "Terms of Service" and "Privacy Policy". Click each link and confirm the pages load. They do not need to be lawyer-drafted — a plain English paragraph stating what data you collect and what users agree to is enough to pass this gate. Missing legal links block app store submissions and payment processor approvals.

### Gate 9 — Social preview metadata renders correctly

Go to https://www.opengraph.xyz and enter your app URL. The tool will render your `og:title`, `og:description`, and `og:image` as they appear when shared on Twitter/X, LinkedIn, and Slack. Confirm:
- `og:title` is set and not empty.
- `og:description` is ≤160 characters.
- `og:image` is present and renders as a readable preview image (min 1200×630 px).

If any tag is missing, add it to your HTML `<head>` or your CMS/framework's metadata config.

### Gate 10 — All copy is proofread

Run your app's key pages (homepage, signup, onboarding first step, pricing) through https://languagetool.org (free, no account required). Fix every flagged grammatical error and misspelling before launch. Typos on the first screen damage trust more than any bug. Copy the text from each page into the tool; it processes plain text directly.

### Gate 11 — Mobile layout is functional on a real phone

Open your app on an actual mobile device (iOS Safari or Android Chrome — not only DevTools resize). Test the core loop: land on the homepage, sign up, complete the main action. Confirm no button is unclickable due to overflow, no text is cut off, and no form field requires horizontal scrolling. If you find a mobile layout break, fix it before proceeding — see the `mobile-responsive` methodology for quick fixes.

### Gate 12 — Rollback plan is written down

Create or update `LAUNCH-GATES.md` with a rollback section:

```
ROLLBACK PLAN

Trigger: any of the following within first 24h post-launch:
- Payment processing fails for >2 consecutive real users
- Signup confirmation emails fail for >10 new users
- Server error rate >5% (check hosting dashboard or Sentry)

Steps:
1. Set Cloudflare DNS for myapp.com to point at maintenance page
   (A record → 192.0.2.1 is a reserved IP that returns no response;
    or use Cloudflare Pages maintenance branch)
2. Post status update in any community where you announced launch
3. Fix the issue locally, re-run Gates 1-12, then restore DNS
```

Fill in real values for your domain, hosting provider, and error thresholds. This plan is not optional — writing it forces you to think through failure modes before they happen.

## Verify

After all 12 gates are marked `[x]`, run:

```bash
grep -c "\[x\]" LAUNCH-GATES.md
```

The output must be `12`. If it is less than 12, open `LAUNCH-GATES.md`, find the unchecked gate, and complete it before announcing launch publicly.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Confirmation email never arrives (Gate 3) | Transactional email provider not verified or DNS records missing | Log in to your email provider dashboard (Resend: https://resend.com/domains, SendGrid: https://app.sendgrid.com/settings/sender_auth). Add the SPF, DKIM, and DMARC TXT records shown there to your DNS in Cloudflare. Allow 10 minutes for propagation, then re-test. |
| Stripe test payment shows "Card declined" (Gate 4) | Wrong card number or Stripe not in test mode | Confirm you are using `4242 4242 4242 4242` exactly. Confirm your Stripe dashboard URL shows `/test/` in the path — if not, toggle to test mode using the switch in the top-left corner. |
| `og:image` does not render in opengraph.xyz (Gate 9) | Image URL is relative or behind auth | Use an absolute URL starting with `https://`. The image must be publicly accessible without login. Host it on your CDN or a public S3 bucket. |
| Mobile button unclickable (Gate 11) | Button inside a container with `overflow: hidden` or `pointer-events: none` on a parent | Open Chrome DevTools on the phone via `chrome://inspect` or use Safari's Web Inspector. Inspect the unresponsive element, look for `pointer-events`, `overflow`, or `z-index` on parent layers. |
| Rollback plan feels unnecessary (Gate 12) | Optimism bias — common in solo builders before first launch | Write it anyway. The act of writing the plan surfaces implicit assumptions about your infrastructure. If it takes more than 15 minutes, your deploy process is too complex. |

## Next

- `ugly-first-version` — if you skipped design entirely and the mobile gate keeps failing, this playbook explains the deliberate tradeoffs between shipping fast and visual quality.
- After passing all 12 gates: post your launch URL publicly, then spend the next 72 hours on user support instead of new features.
- Once you have 10 paying users: revisit Gate 6 data to find the first conversion drop-off point and fix exactly that.

## References

- [knowledge/free/dev/software-developer/error-handling](../../../knowledge/free/dev/software-developer/error-handling) — Gate 5 (custom error pages) applies the error-surface principle from this methodology: every unhandled case must reach the user as a readable message, not a raw stack trace or blank screen.
- [knowledge/free/dev/software-developer/mobile-responsive](../../../knowledge/free/dev/software-developer/mobile-responsive) — Gate 11 relies on the responsive layout checklist from this methodology to identify overflow, touch-target, and viewport-width issues on real devices during the pre-launch pass.
