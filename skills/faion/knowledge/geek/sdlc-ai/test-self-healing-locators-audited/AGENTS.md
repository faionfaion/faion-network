# Self-Healing Locators with Mandatory Audit Diff

## Summary

In Playwright, Cypress, or Selenium suites where an AI healer auto-repairs broken selectors, restrict healing to candidates that match the original locator's accessibility role and accessible name, and require every heal to land as a reviewable diff (`healed-selectors.diff` or equivalent) before the next CI run consumes it. Auto-healing without an audit trail is silent test rot; allowing arbitrary CSS-substitution heals is how an E2E suite ends up clicking the wrong button on a payment screen.

## Why

Microsoft's Playwright self-healing benchmark reports ~75% success on selector-related failures via accessibility-tree matching, with maintenance time dropping ~33% in the first quarter; accessibility-tree heals (`Role: button, Name: Checkout`) are roughly 10× more stable than DOM-class heals (`div.checkout-btn-v3`). Healing is therefore high-leverage but high-risk: a wrong heal in an auth or payment flow turns a real bug into a silent green build. The two-part rule — same-role-and-name + human-reviewed diff — is the published mitigation; without it, auto-heal is a foot-gun.

## When To Use

- Large E2E suites (>200 tests) with regular UI churn from a fast-shipping product team.
- Design-system migrations and component-rename refactors where DOM changes en masse.
- Cypress / Playwright projects already using role-based or test-id locators (`getByRole`, `getByTestId`).
- Cross-browser regression suites where flake from selector drift dominates failures.

## When NOT To Use

- High-stakes flows: payments, login, role-elevation, account deletion — wrong heal = wrong click = silent prod regression.
- Small E2E suites (<50 tests) where humans can repair selectors faster than reviewing heal diffs.
- Suites that locate elements by visual position or pixel coordinate — no accessible name to anchor on.
- A/B-tested UI where the same role+name appears in two variants — heals collide.

## Content

| File | What's inside |
|------|---------------|
| `content/01-role-name-anchor.xml` | Rule: heals must preserve role + accessible-name; class-only heals are forbidden. |
| `content/02-audit-diff-gate.xml` | Rule: every heal lands as a committed diff; CI fails if the diff is unreviewed. |

## Templates

| File | Purpose |
|------|---------|
| `templates/healer-policy.json` | Policy file the healer reads: allowed roles, forbidden flows, diff path. |
| `templates/healer-ci.yml` | CI workflow snippet that fails when `healed-selectors.diff` exists without review. |
