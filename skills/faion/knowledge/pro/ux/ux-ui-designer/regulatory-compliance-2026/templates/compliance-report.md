<!-- purpose: skeleton for a regulatory-compliance-2026 report -->
<!-- consumes: surface inventory + jurisdiction list + testing logs -->
<!-- produces: report artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~600-1200 tokens when loaded as context -->

# Accessibility Compliance Report — <PRODUCT>

- Report date: <YYYY-MM-DD>
- Owner: <name + email>
- Cycle: <quarterly | release | annual>

## Surface inventory

| ID | Type | URL / Bundle | Jurisdictions |
|----|------|--------------|---------------|
| web-app | web | https://app.example.com | US, EU |
| ios-app | ios | com.example.ios | US |

## Regulation matrix

| Surface | Regulation | WCAG version | WCAG level | Deadline |
|---------|------------|--------------|------------|----------|
| web-app | ADA-Title-II | 2.1 | AA | 2026-04-24 |
| web-app | EAA | 2.1 | AA | 2025-06-28 |

## Testing log

- Automated: axe-core / pa11y / Lighthouse runs on <date>; <N> issues open.
- Manual: keyboard + VoiceOver/NVDA sweep on <date>; <N> issues open.
- AT-user: <name or vendor> session on <date>; <N> issues.

## Accessibility statement

- URL: https://example.com/accessibility
- Last updated: <YYYY-MM-DD>
- WCAG version / level (design baseline): 2.2 AA
- Feedback channels: <email>, <phone>, <form>
- Methodology checked: automated, manual, AT-user

## Remediation backlog

| ID | WCAG SC | Surface | Severity | Owner |
|----|---------|---------|----------|-------|
| R-001 | 1.4.3 | web-app | high | fe-team |

## Sign-off

- A11y lead: <name + date>
- Legal counsel: <name + date>
