# AI Accessibility Automation 2026

## Summary

Full continuous accessibility automation pipeline for products with frequent deployments: axe-playwright scans every deploy, AI ranks and de-duplicates violations, code fixes are suggested per issue, VPAT 2.5 drafts are generated from scan summaries, and caption/alt-text pipelines run on every media upload. All AI outputs are gated by a human accessibility lead before entering the developer backlog.

## Why

94.8% of homepages still fail WCAG 2 (WebAIM 2026). Manual audits ($5k–$20k each) happen at most twice a year; AI-assisted continuous monitoring costs $100–$2,000/month and catches regressions before production. ADA Title II compliance (effective April 2026 for state/local government) requires documented conformance — AI VPAT drafting converts hours of work to seconds.

## When To Use

- Establishing continuous accessibility monitoring in a CI/CD pipeline for frequent-deploy products
- Generating ADA Title II compliance documentation for public-sector or higher-education digital products
- Scaling remediation across a large codebase where manual triaging is cost-prohibitive
- Producing AI-assisted VPAT drafts for enterprise procurement processes
- Automating captioning and audio description pipelines for video-heavy content operations

## When NOT To Use

- No existing accessibility baseline — start with a manual audit first
- Product is in pre-MVP prototyping — defer automation until UI stabilizes
- Proposing AI automation as a replacement for user testing with assistive technology users
- Deploying AI overlay widgets as the compliance strategy — overlays do not satisfy ADA Title II
- Budget-only driver with no compliance risk — automation tools cost money; weigh against risk

## Content

| File | What's inside |
|------|---------------|
| `content/01-capabilities.xml` | AI vs traditional tool comparison; enterprise platform survey; new 2026 efficiency features |
| `content/02-pipeline.xml` | 5-stage automation workflow; human-AI responsibility split; video accessibility (ADA Title II) |
| `content/03-anti-patterns.xml` | VPAT legal risk, ARIA fix errors, overlay failures, chunking large axe output, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-a11y-gate.sh` | CI gate: runs axe-cli, diffs against baseline, fails on new Critical violations |
| `templates/prompt-scan-triage.txt` | Haiku prompt: axe JSON → filtered, ranked, grouped issue report with fixes |
| `templates/prompt-vpat-draft.txt` | Haiku prompt: scan summary → VPAT 2.5 section draft with DRAFT watermark |
