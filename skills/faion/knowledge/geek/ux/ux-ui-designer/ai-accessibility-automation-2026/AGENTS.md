# AI Accessibility Automation 2026

## Summary

Methodology for integrating AI-powered tools into accessibility workflows: automated WCAG scanning, AI-assisted issue triage and code remediation, VPAT 2.5 draft generation, and ADA Title II video captioning pipelines. AI augments detection (covering 60–70% of automatable issues) while humans own AT testing, complex judgment, and legal sign-off.

## Why

94.8% of homepages still contain detectable WCAG 2 failures (WebAIM 2026). Manual auditing doesn't scale. AI tooling closes the detection gap for repetitive, automatable checks — reducing false positives, surfacing code-fix suggestions, and generating structured compliance documentation in seconds rather than hours. The 30–40% that AI misses (ARIA live regions, keyboard traps, focus management) requires human + AT validation.

## When To Use

- Establishing a continuous accessibility baseline in CI/CD where every PR is scanned before merge
- Scaling audits across 100+ pages where manual review is impractical
- Generating ADA/VPAT documentation for procurement or legal requirements
- Integrating video captioning and audio description workflows for ADA Title II compliance (2026)
- Post-launch regression monitoring to catch regressions introduced by routine updates

## When NOT To Use

- As the only validation method — AI covers 60–70%; the rest requires human + AT testing
- Replacing user testing with people with disabilities — automation cannot validate cognitive accessibility or AT compatibility
- Auditing complex interactive patterns (custom data grids, drag-and-drop, real-time updates) — dynamic AT behavior is not captured by static scanners
- On SPAs requiring authentication without session management — scanners will scan only the login page
- As legal compliance proof without human expert review and sign-off

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow.xml` | Five-step AI-augmented accessibility pipeline, human/AI responsibility split, CI/CD integration rules |
| `content/02-tools-and-services.xml` | CLI tools, SaaS services, agent-friendliness ratings, gotchas |
| `content/03-prompts-and-patterns.xml` | Agentic workflow, recommended subagents, prompt patterns for violation triage and VPAT drafting |

## Templates

| File | Purpose |
|------|---------|
| `templates/pa11y-scanner.py` | pa11y-ci batch scanner with JSON output |
| `templates/prompt-violation-triage.txt` | Prompt for AI-assisted WCAG violation triage |
| `templates/prompt-vpat-draft.txt` | Prompt for VPAT 2.5 Section 508 draft generation |
