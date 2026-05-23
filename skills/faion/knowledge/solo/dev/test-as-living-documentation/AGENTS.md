---
slug: test-as-living-documentation
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "BDD-style Given/When/Then tests linked 1:1 to acceptance criteria, auto-published as living documentation reviewable by business stakeholders."
content_id: "95d7667a1210a3e6"
complexity: medium
produces: spec
est_tokens: 5100
tags: [bdd, given-when-then, testing, documentation, ac]
---
# Test as Living Documentation

## Summary

**One-sentence:** BDD-style Given/When/Then tests linked 1:1 to acceptance criteria, auto-published as living documentation reviewable by business stakeholders.

**One-paragraph:** Most test suites are unreadable to non-developers; AC drift silently and tests become regression-only. This methodology applies Given/When/Then style with strict naming, ties every test back to a tracked AC ID, publishes a generated doc on every run (Cucumber HTML / Pickles / custom), tracks AC-coverage (>=80% AC has >=1 test), and runs a quarterly stakeholder review against the generated docs. Output: a BDD style guide + AC-to-test mapping spec + generated-docs URL signed off by a named BA/PM owner.

**Ефективно для:**

- AC and tests drift - lock test names to AC IDs.
- BAs can't read the test suite - publish generated HTML docs.
- AC coverage unknown - install coverage tracker, target >=80%.
- Test suite reviewed only by devs - quarterly stakeholder review.
- AI-generated tests pass without behaviour assertions - GWT enforces behaviour.

## Applies If (ALL must hold)

- AC exist in a tracker (Jira, Linear, GitHub Issues) with stable IDs
- team uses or can adopt a BDD framework (Cucumber, Behave, SpecFlow, pytest-bdd)
- business stakeholders consume test output (BA / PM / product / sales)
- doc generation pipeline exists or can be installed (Cucumber Reports, Pickles, custom HTML)

## Skip If (ANY kills it)

- infra-only system with no business-readable surface
- team treats tests as a private dev artefact only
- AC do not yet exist - build AC discipline first, then return here

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AC corpus | tracker export with stable IDs | Jira / Linear / GitHub Issues |
| BDD framework | installed + CI-wired | engineering |
| Doc generator | outputs HTML or Markdown per run | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-ac-to-assertion-mapping]] | per-AC assertion discipline grounds the test names |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / gate) | ~900 |
| `content/05-examples.xml` | essential | End-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-given-when-then` | sonnet | Translating AC sentence to GWT phrasing needs judgement. |
| `compute-ac-coverage` | haiku | Mechanical join of AC IDs to test files. |
| `review-generated-docs` | opus | Stakeholder-readable phrasing requires senior judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-as-living-documentation.md` | Markdown skeleton for the Test as Living Documentation artefact. |
| `templates/_smoke-test.json` | Minimum viable test-as-living-documentation record for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-as-living-documentation.py` | Validate Test as Living Documentation artefact against content/02-output-contract.xml. | After draft, before merge; pre-commit hook. |

## Related

- [[qa-ac-to-assertion-mapping]]
- [[qa-exploratory-charter-template]]
- [[uat-script-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree filters on AC-corpus existence, stakeholder-reader presence, and BDD-framework availability; routes runs without any of those signals to skip-this-methodology so the artefact only lands where consumers exist.
