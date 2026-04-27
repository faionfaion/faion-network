# AI-Assisted Accessibility

## Summary

Pipeline for WCAG 2.2 AA compliance using AI-enhanced automated scanning (axe-core, Lighthouse, pa11y) as the first pass, followed by manual assistive technology testing for interactive components and cognitive accessibility. Automated tools catch ~60-70% of auditable issues; the remaining 30-40% require human + AT verification.

## Why

Manual accessibility audits are expert-intensive and expensive. AI-enhanced tools (axe DevTools, Deque) reduce false positives and suggest code fixes in context, cutting remediation time. Treating AI-only results as sufficient produces incomplete compliance; the pipeline enforces the correct sequence — automate first, then verify with real AT.

## When To Use

- Sprint includes new UI components that must meet WCAG 2.2 AA before merge
- Accessibility audit needed for an existing product with no prior testing baseline
- Small team without a dedicated accessibility specialist (AI augments coverage)
- Preparing a VPAT for enterprise procurement
- Video/audio content being published (ADA Title II 2026 captions/audio descriptions required)

## When NOT To Use

- Treating AI overlay widgets as a substitute for fixing underlying code — overlays are not compliant solutions
- As the only testing method — automated tools miss 30-40% of issues
- Complex interactive patterns (drag-and-drop, data grids, custom widgets) — AI scoring is unreliable; manual AT testing required
- When user testing with people with disabilities is scheduled — do automated pass first, fix, then test with real users

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-and-rules.xml` | Audit pipeline order, CI gate rules, tool roles, VPAT guidance |
| `content/02-tools-and-gotchas.xml` | CLI tools, services, agent workflow, AI gotchas, limitations |

## Templates

| File | Purpose |
|------|---------|
| `templates/axe-playwright-runner.py` | Run axe-core via Playwright, return violation JSON |
| `templates/prompt-audit-results.txt` | Agent prompt: map axe JSON violations to WCAG criteria with code fixes |
| `templates/prompt-vpat-draft.txt` | Agent prompt: draft WCAG 2.2 AA conformance statement from known issues |
