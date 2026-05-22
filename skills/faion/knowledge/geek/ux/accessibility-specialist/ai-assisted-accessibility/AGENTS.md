---
slug: ai-assisted-accessibility
tier: geek
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI accelerates WCAG auditing by automating scan execution, false-positive filtering, fix suggestion generation, and bulk alt text creation — reducing audit time by 60–75%.
content_id: "a0f551d07b2edb06"
tags: [accessibility, wcag, ai-automation, auditing, testing]
---
# AI-Assisted Accessibility

## Summary

**One-sentence:** AI accelerates WCAG auditing by automating scan execution, false-positive filtering, fix suggestion generation, and bulk alt text creation — reducing audit time by 60–75%.

**One-paragraph:** AI accelerates WCAG auditing by automating scan execution, false-positive filtering, fix suggestion generation, and bulk alt text creation — reducing audit time by 60–75%. A Haiku subagent runs axe-playwright or pa11y, filters noise, and ranks issues by impact. A Sonnet subagent generates code fixes per issue. Human experts validate all AI output before developer tickets are created.

## Applies If (ALL must hold)

- Running automated WCAG audits as part of a CI/CD pipeline before each deployment
- Generating alt text suggestions at scale for image-heavy content pipelines
- Producing draft VPAT/accessibility conformance reports from scan results
- Triaging a large backlog of accessibility issues by AI-assisted priority ranking
- Generating auto-captions for video content as a first pass before human review

## Skip If (ANY kills it)

- Replacing real user testing with people who use assistive technology — AI cannot substitute
- Accepting AI overlay widgets as an accessibility solution — they do not fix underlying code
- Treating AI-generated alt text as final without editorial review for context and brand voice
- Using AI scan results alone as proof of WCAG compliance for legal or procurement purposes
- Cognitive accessibility evaluation — AI tools have poor coverage here even in 2026

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ux/accessibility-specialist/`
