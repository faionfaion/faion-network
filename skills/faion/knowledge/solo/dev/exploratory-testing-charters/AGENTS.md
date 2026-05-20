---
slug: exploratory-testing-charters
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Session-based, charter-driven, heuristic-based exploratory testing (Bach/Bolton) — the discipline faion's scripted/automated testing corpus is missing.
content_id: "3b981f54a7f40a89"
tags: [exploratory-testing-charters, dev, solo]
---

# Exploratory Testing Charters

## Summary

**One-sentence:** Session-based, charter-driven, heuristic-based exploratory testing (Bach/Bolton) — the discipline faion's scripted/automated testing corpus is missing.

**One-paragraph:** Faion's entire testing corpus is scripted/automated. Modern QA pairs automation with structured exploratory testing. Output: charter template + heuristic catalogue + session-debrief template.

## Applies If (ALL must hold)

- product has a UI or API surface used by humans
- tester or developer has ≥1h per week for exploratory sessions
- team values bug discovery beyond regression coverage

## Skip If (ANY kills it)

- infrastructure-only systems with no human-facing surface
- team treats QA as 100% automation gate — different philosophy
- single-script test product (calculator, single transform)

## Prerequisites

- list of risk areas in the current release
- test heuristics reference (Bach SFDIPOT, ISTQB-EXT, Karen Johnson cheat sheet)
- session note format (text doc, Notion, dedicated tool)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill — provides operating context for this methodology |
| `solo/dev/automation-tooling` | peer methodology — produces inputs or consumes outputs |
| `free/dev/testing-developer` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `solo/dev/automation-tooling`
- peer methodology: `free/dev/testing-developer`
- peer methodology: `pro/dev/perf-test-basics`
- external: https://www.satisfice.com/exploratory-testing (James Bach); http://www.developsense.com/blog/ (Michael Bolton); https://kaner.com/?p=104
