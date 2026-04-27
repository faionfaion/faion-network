# AI-Assisted Accessibility

## Summary

AI accelerates WCAG auditing by automating scan execution, false-positive filtering, fix suggestion generation, and bulk alt text creation — reducing audit time by 60–75%. A Haiku subagent runs axe-playwright or pa11y, filters noise, and ranks issues by impact. A Sonnet subagent generates code fixes per issue. Human experts validate all AI output before developer tickets are created.

## Why

Manual accessibility audits take 20–40 hours and happen infrequently; AI-assisted workflows compress the same coverage to 5–10 hours and enable continuous monitoring on every deploy. AI reduces false positives from 30–40% to 10–15% and attaches code fix suggestions directly to issues, cutting developer context-switching.

## When To Use

- Running automated WCAG audits as part of a CI/CD pipeline before each deployment
- Generating alt text suggestions at scale for image-heavy content pipelines
- Producing draft VPAT/accessibility conformance reports from scan results
- Triaging a large backlog of accessibility issues by AI-assisted priority ranking
- Generating auto-captions for video content as a first pass before human review

## When NOT To Use

- Replacing real user testing with people who use assistive technology — AI cannot substitute
- Accepting AI overlay widgets as an accessibility solution — they do not fix underlying code
- Treating AI-generated alt text as final without editorial review for context and brand voice
- Using AI scan results alone as proof of WCAG compliance for legal or procurement purposes
- Cognitive accessibility evaluation — AI tools have poor coverage here even in 2026

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-landscape.xml` | AI-powered tools by category; integration points (design, dev, CI/CD, testing) |
| `content/02-workflow.xml` | 5-stage pipeline: scan → AI suggestions → manual verification → user testing → monitoring |
| `content/03-anti-patterns.xml` | Overlay failures, alt text limitations, caption accuracy requirements, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-a11y-gate.sh` | pa11y-ci CI gate script with threshold configuration |
| `templates/pa11yci.json` | pa11y-ci config: WCAG2AA, axe + htmlcs runners, ignore list |
| `templates/prompt-triage-issues.txt` | Haiku prompt: axe JSON → ranked issue list with fix suggestions |
| `templates/prompt-generate-fix.txt` | Sonnet prompt: WCAG violation + code snippet → concrete code fix |
