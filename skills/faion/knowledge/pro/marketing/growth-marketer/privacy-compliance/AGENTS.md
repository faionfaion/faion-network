# Privacy-Compliant Analytics

## Summary

Privacy-compliant analytics means implementing a consent management platform (CMP) with default-deny analytics, GA4 Consent Mode v2 wiring, CCPA Global Privacy Control (GPC) signal handling, and IP anonymization — so tracking only activates after explicit user consent. Every new tag or pixel must pass through the consent gate before firing.

## Why

GDPR, UK GDPR, CCPA/CPRA, and LGPD impose fines for analytics cookies set before consent, for "Reject all" buttons that are harder to click than "Accept all" (CNIL fines, 2022–2024), and for US-hosted analytics processing EU personal data without valid SCCs or EU-US DPF. A correct default-deny setup eliminates the most common violations with minimal developer effort.

## When To Use

- Any web or app property tracked by GA4, Plausible, Mixpanel, Amplitude, or PostHog under GDPR, CCPA, or LGPD scope.
- Adding a new analytics or marketing tag — must pass through the consent gate before firing.
- Migrating to GA4 Consent Mode v2 or upgrading a CMP to IAB TCF 2.2.
- Implementing or auditing a CMP: OneTrust, Cookiebot, Iubenda, Osano, CookieYes, Klaro.
- DPIA or vendor review for a new tracker, pixel, or session-replay tool.

## When NOT To Use

- Internal-only tools behind SSO with no third-party analytics — no public consent surface.
- Server-side-only telemetry tied to authenticated user IDs processed under contract (legitimate interest / contract basis) — still needs Records of Processing, but not a cookie banner.
- Static brochure sites with zero cookies and zero analytics — a banner here is legal theater.

## Content

| File | What's inside |
|------|---------------|
| `content/01-consent-setup.xml` | Default-deny rule, Consent Mode v2 configuration, CCPA GPC signal, event queuing pattern |
| `content/02-compliance-rules.xml` | GDPR UI parity rule, sub-processor DPA requirement, IP anonymization limits, agent LLM gotchas |
| `content/03-checklist.xml` | Pre-launch checklist, data anonymization steps, user rights, governance and audit log |

## Templates

| File | Purpose |
|------|---------|
| `templates/analytics-manager.js` | AnalyticsManager class: consent gate, GA4 Consent Mode v2, CCPA GPC, event queue, cookie clearing |
| `templates/consent-test.ts` | Playwright test: no analytics cookies before consent, GA4 fires only after accept |
