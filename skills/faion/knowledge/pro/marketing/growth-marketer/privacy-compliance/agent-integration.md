# Agent Integration — Privacy Compliance (Analytics)

## When to use
- Web/app properties tracked by GA4, Plausible, Mixpanel, Amplitude, PostHog, or any cookie-setting analytics under GDPR / UK GDPR / CCPA / CPRA / LGPD scope.
- New analytics or marketing tag is being added — must pass through the consent gate before firing.
- Migrating from a non-consent setup, or upgrading to GA4 Consent Mode v2 / IAB TCF 2.2.
- Implementing or auditing a Consent Management Platform (CMP): OneTrust, Cookiebot, Iubenda, Osano, Klaro, CookieYes.
- DPIA / vendor-review work for a new tracker, pixel, or session-replay tool.

## When NOT to use
- Internal-only tools behind SSO with no third-party analytics — there is no public consent surface.
- Server-side-only product telemetry tied to authenticated user IDs you already process under contract — that is `legitimate interest` / contract basis, not cookie consent (still requires Records of Processing).
- Static brochure sites with zero cookies and zero analytics — a banner here is theater.

## Where it fails / limitations
- Consent Mode v2 still pings Google with cookieless beacons; this is "compliant" by Google's reading but contested in EU rulings (CNIL, Austrian DSB).
- "Reject all" buttons that are slower or smaller than "Accept all" violate GDPR (CNIL fines, 2022–2024). Agents writing CMP UIs must enforce parity.
- Plausible / Fathom claim "no consent needed" — only true if you do not also load GA, ads, or other cookies. Mixed setups need consent.
- IP anonymization in GA4 is automatic but does not exempt processing — ICO and EDPB still treat anonymized IP-derived analytics as personal data in many cases.
- Server-side GTM does not bypass consent law; the legal basis is processing, not transport.
- Schrems II / EU-US DPF instability: GA4 + US-hosted vendors require ongoing assessment; a CMP banner does not fix this.

## Agentic workflow
Use subagents to (1) audit the live tag/cookie inventory against the consent matrix, (2) author CMP rules and consent-gated tag templates, (3) write the cookie policy + privacy policy diffs, and (4) verify default-deny on every new release. Never let an agent edit the live consent banner directly — generate diffs into PRs, require legal review before merge.

### Recommended subagents
- `privacy-compliance` / `legal-reviewer` (opus) — interpret regulation, sign off on lawful basis text.
- `frontend-developer` (sonnet) — implement Consent Mode v2, dataLayer, queue events.
- `data-engineer` (sonnet) — server-side GTM, hashing, retention SQL.
- `qa-tester` (sonnet) — Playwright tests asserting no analytics cookies set pre-consent.

### Prompt pattern
```
Input: cookie_audit.json (name, vendor, purpose, lifetime, observed_pre_consent: true/false)
Task: classify each cookie into [strictly_necessary, functional, analytics, marketing]
      flag every observed_pre_consent=true that is NOT strictly_necessary
      output remediation patch using AnalyticsManager from privacy-compliance/README.md
Forbidden: claiming a vendor is "compliant" — only state the gating mechanism applied.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | Headless cookie + network audit pre/post consent | `npm i -D @playwright/test` |
| `lighthouse` | Privacy + perf signals incl. third-party cookies | `npm i -g lighthouse` |
| `cookiepedia` API | Vendor classification lookup | https://cookiepedia.co.uk |
| `klaro` | OSS CMP, fully scriptable config | `npm i klaro` |
| `gtag-helper` / `dataLayer` debugger | Validate Consent Mode v2 signals | https://tagassistant.google.com |
| `oneTrust-cli` (3rd-party) | Sync OneTrust cookie scans into source-control | community tool |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OneTrust | SaaS | Partial — REST API | Enterprise CMP, IAB TCF 2.2, heavy console |
| Cookiebot | SaaS | Yes — REST + script | Auto-scan + consent banner; agent can configure via API |
| Iubenda | SaaS | Yes — REST | Banner + policy generator; multi-jurisdiction |
| Osano | SaaS | Yes — REST | CMP + vendor inventory |
| CookieYes | SaaS | Yes — REST + script | Lightweight CMP; good for small SaaS |
| Klaro | OSS | Yes — config in JS | Self-hosted, GDPR-grade defaults |
| TrustArc | SaaS | Partial | Enterprise; API exists but slow workflow |
| Google Tag Manager (server-side) | SaaS | Yes — REST | Reduces client tags but does not remove consent need |
| Plausible / Fathom | SaaS / OSS | Yes — REST | Cookieless analytics; reduces but does not eliminate consent surface |

## Templates & scripts
See `README.md` for the `AnalyticsManager` class, GA4 Consent Mode v2 defaults, IP-anonymization snippet, async + batched loading. For automated regression in CI, this 30-line Playwright check fails the build if a non-essential cookie is set before consent:

```ts
// tests/consent.spec.ts
import { test, expect } from "@playwright/test";

const ALLOWED_PRE_CONSENT = ["__cf_bm", "csrftoken", "session"]; // strictly necessary

test("no analytics cookies set before consent", async ({ page, context }) => {
  await page.goto("https://example.com");
  await page.waitForLoadState("networkidle");
  const cookies = await context.cookies();
  const violations = cookies.filter(
    (c) => !ALLOWED_PRE_CONSENT.some((ok) => c.name.startsWith(ok))
  );
  expect(violations, JSON.stringify(violations, null, 2)).toEqual([]);
});

test("ga4 fires only after explicit consent", async ({ page }) => {
  const requests: string[] = [];
  page.on("request", (r) => requests.push(r.url()));
  await page.goto("https://example.com");
  expect(requests.find((u) => u.includes("google-analytics.com/g/collect"))).toBeUndefined();

  await page.getByRole("button", { name: /accept all/i }).click();
  await page.waitForRequest((r) => r.url().includes("google-analytics.com"));
});
```

## Best practices
- Default-deny: ship the page with `analytics_storage: 'denied'` and only update on explicit user action — never assume implied consent.
- "Reject all" must be one click and visually equal to "Accept all" — otherwise CNIL/DPC fines apply.
- Keep a versioned consent log (timestamp, version of policy, IP hash, choice) for audit; not consenting once is fine, lying about consent is not.
- Treat sub-processors as vendors — every new pixel/SDK needs DPA, transfer mechanism (SCCs / DPF), and entry in the Records of Processing.
- Tie the cookie policy table to the live CMP scan output, not a hand-written list — it drifts within weeks.
- Server-side tagging reduces client cookies but does not remove lawful-basis requirement; document the basis explicitly.
- Disable `restricted_data_processing` for non-CCPA users to avoid over-restricting analytics outside California.

## AI-agent gotchas
- LLMs confidently quote outdated guidance (pre-Schrems II, pre-Consent Mode v2). Force the agent to cite a dated regulation/source for every claim.
- Agents may suggest "anonymizing IP makes GDPR not apply" — wrong. Anonymization is one mitigation among many; processing law still applies.
- "GA4 is GDPR-compliant" is a marketing claim, not a legal one. Make the agent describe the *gating mechanism* (consent + Consent Mode v2 + EU region) instead.
- Generated banner copy often dark-patterns (highlighted Accept, hidden Reject). Lock UI parity in the template, do not let the agent restyle.
- Hashing emails/IDs without a salt and rotation policy is reversible — instruct the agent to never claim hashing == anonymization.
- Cookie-policy text written by an LLM regularly invents vendor names. Bind the policy to actual scan output (Cookiebot/Osano export) rather than free generation.
- Region detection (EU vs US vs CA) must come from a server-trusted signal (IP geo + GeoIP DB), not from `Accept-Language` or the LLM's guess.

## References
- EDPB Guidelines 03/2022 on consent (revised 2023) — https://edpb.europa.eu
- CNIL, "Cookies and other trackers" — https://www.cnil.fr/en/cookies-and-other-trackers
- ICO guidance on PECR & analytics — https://ico.org.uk
- Google Consent Mode v2 docs — https://developers.google.com/tag-platform/security/guides/consent
- IAB Europe TCF 2.2 — https://iabeurope.eu/tcf-2-2/
- CCPA / CPRA text — https://oag.ca.gov/privacy/ccpa
- Brazilian LGPD overview — https://www.gov.br/anpd
- Schrems II ruling, CJEU C-311/18 — https://curia.europa.eu
