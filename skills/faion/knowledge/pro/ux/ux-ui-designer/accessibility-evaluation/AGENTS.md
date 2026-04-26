# Accessibility Evaluation

## Summary

A five-stage audit process for WCAG 2.1/2.2 AA conformance: automated scan (axe, Pa11y, Lighthouse) → triage → scripted keyboard testing (Playwright) → screen reader verification (NVDA/JAWS/VoiceOver) → structured report. Automated tools catch 30-40% of issues; stages 3-4 are mandatory to reach meaningful coverage. Screen reader verification requires a human — no LLM can reproduce AT speech buffers.

## Why

"axe-clean = compliant" is the most common audit failure. Automated tools are blind to ARIA misuse, focus-order problems in modals, live-region behavior, and cognitive accessibility. Legal risk (ADA Title II, EAA, procurement VPAT requirements) requires structured evidence: per-criterion findings, remediation recommendations citing W3C techniques, and POUR-grouped tables — not just tool output.

## When To Use

- Pre-release WCAG 2.1/2.2 AA audit before launch.
- Regression check after design system upgrades or major refactors.
- Procurement / RFP responses requiring VPAT or ACR documentation.
- Post-incident remediation when a complaint or lawsuit names specific WCAG criteria.
- CI gating on PRs touching shared library components.

## When NOT To Use

- Early lo-fi wireframe stage — use accessibility-first-design heuristics, not a full audit.
- Pure ATAG or UAAG compliance — different rule sets; this methodology covers WCAG content/UI scope only.
- Native iOS/Android — use Accessibility Inspector (Xcode) and Accessibility Scanner (Android).
- PDF or document accessibility — use PAC 2024 or Adobe Acrobat Pro checker.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Five-stage audit process, keyboard test matrix, screen reader pairings, issue priority tiers |
| `content/02-agent-patterns.xml` | Agent pipeline roles, prompt patterns for triage and keyboard trace, gotchas, tool reference |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-report.md` | Accessibility audit report: executive summary, methodology, POUR findings tables, per-issue template |
| `templates/scan.mjs` | Playwright + axe-core scanner: emits per-page JSON consumed by triage agent |

## Scripts

none
