---
slug: test-as-living-documentation
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: BDD-style readable tests, doc-string-driven test generation, Given-When-Then enforcement — testing for documentation fidelity, not just regression.
content_id: "09320402b2ffedbe"
tags: [test-as-living-documentation, dev, solo]
---

# Test as Living Documentation

## Summary

**One-sentence:** BDD-style readable tests, doc-string-driven test generation, Given-When-Then enforcement — testing for documentation fidelity, not just regression.

**One-paragraph:** Faion's testing-patterns mentions Given-When-Then as a pattern but does not address documentation-fidelity: tests readable by BAs/PMs, auto-published as feature docs, synced with acceptance criteria. Output: BDD style guide + test-to-doc generator + AC linkage.

## Applies If (ALL must hold)

- team has business stakeholders consuming test output
- acceptance criteria exist (Jira, Linear, GitHub Issues)
- team uses a BDD-capable framework (Cucumber/Behave/SpecFlow) OR can adopt one

## Skip If (ANY kills it)

- infra-only system with no business-readable surface
- team treats tests as private dev artefact only
- AC do not exist (build AC discipline first)

## Prerequisites

- AC format defined
- test framework supports natural-language style
- doc generation pipeline (Cucumber Reports, Pickles, custom)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill — provides operating context for this methodology |
| `solo/dev/exploratory-testing-charters` | peer methodology — produces inputs or consumes outputs |
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
- peer methodology: `solo/dev/exploratory-testing-charters`
- peer methodology: `free/dev/testing-developer`
- peer methodology: `pro/dev/perf-test-basics`
- external: https://cucumber.io/docs/bdd/; https://dannorth.net/introducing-bdd/
