---
slug: ai-over-reliance-self-audit
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Periodic audit for solo developers: which parts of the codebase do I no longer understand, which decisions did the model make that I rubber-stamped, and how to recover.
content_id: "7530fa416af02b42"
tags: [ai-over-reliance-self-audit, dev, solo]
---

# AI Over-Reliance Self-Audit

## Summary

**One-sentence:** Periodic audit for solo developers: which parts of the codebase do I no longer understand, which decisions did the model make that I rubber-stamped, and how to recover.

**One-paragraph:** Solo devs slide into AI over-reliance fast: hours saved compound into months of code the human author cannot explain. Mechanism: quarterly 2-hour audit — blast-radius map, rubber-stamp inventory, 90-day recovery plan. Output: comprehension-debt artefact + recovery plan.

## Applies If (ALL must hold)

- solo dev or 2-person team
- ≥50% of code in last 90 days was AI-generated or AI-edited
- developer is sole owner of long-term maintenance

## Skip If (ANY kills it)

- throwaway prototype or one-off script
- team ≥2 reviewers per PR — peer review absorbs the risk
- AI usage constrained to line-by-line suggestions

## Prerequisites

- git log with commit metadata (or AI-tool log)
- list of services/modules in scope
- 2 contiguous hours blocked for the audit

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill — provides operating context for this methodology |
| `solo/dev/library-evaluation-rubric` | peer methodology — produces inputs or consumes outputs |
| `junior-ai-co-pilot-curriculum` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `solo/dev/software-developer/`
- peer methodology: `solo/dev/library-evaluation-rubric`
- peer methodology: `junior-ai-co-pilot-curriculum`
- external: https://stackoverflow.blog/2024/03/05/ai-coding-assistants-survey/
