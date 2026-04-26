# Accessibility Testing Process

## Summary

Five-step accessibility testing process combining automated scanning (axe, WAVE, Lighthouse, Pa11y), manual keyboard testing, screen reader verification, cognitive accessibility checks, and prioritized issue documentation. Automated tools catch ~30-40% of WCAG violations; the rest require structured manual walkthroughs with real AT.

## Why

Automated scanners produce false confidence: a "0 violations" axe report does not equal WCAG conformance. SC 1.3.1 (Info and Relationships), 2.4.6 (Headings and Labels), 3.3.3 (Error Suggestion) require human judgment. Running both axe and Pa11y catches ~15% more issues than either alone because their rule sets diverge. The complete process — automated + keyboard + screen reader + cognitive + documentation — is the minimum evidence trail for ADA Title II and EAA compliance.

## When To Use

- Pre-release WCAG 2.1/2.2 audit on a web product.
- CI gate for new pages or components — automated scan must pass before merge.
- Quarterly compliance review for ADA Title II or EAA-bound products.
- Procurement: generating VPAT/ACR evidence from real test runs.
- Triage: converting a raw a11y issue dump into a prioritized remediation plan.

## When NOT To Use

- Design-stage review — use `accessibility-first-design` (cheaper to fix in Figma than in code).
- Native mobile-only flows — axe/Pa11y do not cover XCUITest/Espresso; use platform-specific scanners.
- XR/spatial interfaces — WCAG does not fully cover them; use `spatial-accessibility` and W3C XAUR.
- Quick one-off contrast tweak — run Colour Contrast Analyser directly, not a full audit.

## Content

| File | What's inside |
|------|---------------|
| `content/01-testing-process.xml` | Five testing steps: automated scan, keyboard, screen reader, cognitive, document-and-fix. Tool selection, what each step catches and misses. |
| `content/02-issue-prioritization.xml` | Priority rubric (Critical/High/Medium/Low), common false positives, CI integration patterns, agentic pipeline. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-report.md` | Accessibility audit report template with executive summary, methodology table, findings by WCAG principle, and issue detail format. |
| `templates/a11y-scan.sh` | Shell script running axe + Pa11y + Lighthouse in sequence, outputting JSON reports and a summary.md. |
