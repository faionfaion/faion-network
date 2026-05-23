<!--
purpose: Pre-launch smoke-test checklist (T-24h and T-2h reruns)
consumes: See content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-500 tokens when loaded as context
-->
# Pre-launch Smoke Tests

Run at T-24h AND T-2h. Both must pass.

- [ ] Anonymous user can load the home page (HTTP 200, no console errors)
- [ ] Anonymous user can sign up (account row created, welcome email delivered <60s)
- [ ] Returning user can log in with email + password
- [ ] Password reset email is delivered
- [ ] Stripe checkout completes for a $1 test charge
- [ ] Stripe webhook receives `checkout.session.completed` and writes the row
- [ ] Welcome email contains the correct activation link
- [ ] Support email forwards to founder inbox
- [ ] Sentry captures a deliberate test error
- [ ] Plausible counts a deliberate test event
- [ ] Status page is reachable and shows "Operational"
