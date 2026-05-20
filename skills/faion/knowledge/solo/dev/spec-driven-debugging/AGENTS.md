---
slug: spec-driven-debugging
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Failing spec first, then minimize repro, then fix — bug-scale SDD that the feature-scale SDD doesn't cover.
content_id: "153077e23d5ec818"
tags: [spec-driven-debugging, dev, solo]
---

# Spec-Driven Debugging

## Summary

**One-sentence:** Failing spec first, then minimize repro, then fix — bug-scale SDD that the feature-scale SDD doesn't cover.

**One-paragraph:** SDD covers spec-driven development at feature scope; nothing covers bug-scale SDD. Working devs spend ~30% of time debugging. Output: bug-spec template + minimization protocol + fix-with-test record.

## Applies If (ALL must hold)

- bug reported with reproducible symptom
- test infrastructure exists
- developer has authority to add tests

## Skip If (ANY kills it)

- infrastructure / config bugs with no code path
- bugs that take longer to write a test for than to fix
- research / spike investigation (different mode)

## Prerequisites

- test framework + assertion style
- version control hash of the reproducing state
- stack trace or log of failure

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill — provides operating context for this methodology |
| `solo/sdd/sdd` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/exploratory-testing-charters` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `solo/sdd/sdd`
- peer methodology: `solo/dev/exploratory-testing-charters`
- peer methodology: `solo/dev/test-as-living-documentation`
- external: https://www.kanat.dev/spec-driven-debugging; https://twosigma.com/insights/article/test-driven-development-anti-patterns/
