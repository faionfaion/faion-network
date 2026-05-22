---
slug: qa-ac-to-assertion-mapping
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c0a778987672829a"
summary: A mapping discipline that ties every acceptance criterion in a user story to a named, behavior-asserting test, so the PR review can verify each AC has a real assertion (not just a structural test) before merge.
tags: [acceptance-criteria, assertions, qa, ai-generated-tests, testing, traceability]
---

# Acceptance Criterion to Assertion Mapping

## Summary

**One-sentence:** Map every acceptance criterion (AC) in a user story to a named test with a behavior-asserting assertion, then verify the mapping at PR review — catching the AI-generated-test failure mode where structural assertions hit 100% line coverage without testing what the AC actually says.

**One-paragraph:** Testing methodologies cover techniques and patterns but not the verification step: "for each AC, is there an assertion that actually proves it?" AI-generated tests favor structural assertions (assert method was called, assert no exception raised, assert response status 200) that look productive in PRs but say nothing about behavior. This discipline introduces an explicit mapping artifact: a small YAML or table next to the story / PR description listing each AC, the test file(s) and test name(s) that cover it, and a one-line note on what assertion proves the behavior. PR review then walks the mapping: any AC with no behavior-asserting test, or any test where the listed assertion does not match the AC, is blocked. Primary output: an `ac-mapping.yaml` per story or per PR plus a reviewer-facing summary that surfaces unmapped ACs.

## Applies If (ALL must hold)

- team uses user stories or feature specs with explicit acceptance criteria
- PRs are reviewed before merge
- AI-assisted test generation is in active use (Copilot, Cursor, Claude Code) OR the team has experienced under-testing despite high line coverage
- product is past MVP with real users (correctness regressions cost money)

## Skip If (ANY kills it)

- team does not write acceptance criteria — fix that first (writing ACs is the upstream discipline)
- single-engineer team with self-review only — discipline is harder to enforce; lighter pattern works
- pure-exploration phase, no real users — formal mapping has negative ROI when requirements are still mutating daily
- compliance environment where every test already maps to a formal requirement — the mapping exists in a heavier system, do not duplicate

## Prerequisites

- user stories or specs follow a consistent AC format (Given/When/Then OR numbered AC list OR Gherkin)
- PR template has space for a test-mapping section
- a definition of "behavior-asserting assertion" the team agrees on (see content/01)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist` | The audit checklist that uses the AC mapping during PR review |
| `pro/dev/code-quality/mutation-testing-ci-gate` | Complementary signal: weak assertions surface in mutation survivors |
| `solo/dev/testing-developer/qa-exploratory-charter-template` | What the AC-mapped tests are NOT supposed to catch (left to exploratory) |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: explicit mapping artifact, behavior-not-structural, one AC many tests OK, mapping at PR not after, reviewer walks the map | ~900 |
| `content/02-output-contract.xml` | essential | ac-mapping.yaml schema with required fields, forbidden patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: missing mapping, structural-only, wrong-AC-tagged, mapping-out-of-date, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_acceptance_criteria_from_story` | haiku | Mechanical parsing from a structured story field |
| `propose_test_per_ac` | sonnet | Per-AC bounded judgment from existing test files |
| `classify_assertion_behavior_vs_structural` | sonnet | Per-assertion bounded judgment using rule from 01 |
| `flag_unmapped_acs_at_pr` | haiku | Set difference between AC list and mapped ACs |

## Templates

| File | Purpose |
|------|---------|
| `templates/ac-mapping.yaml` | YAML form: list of ac_id, test_path, test_name, asserted_behavior |
| `templates/pr-mapping-section.md` | PR-description snippet that reviewers expect to find |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/extract-acs.py` | Pulls ACs from the linked story (Jira, Linear, GitHub Issue) and pre-populates ac-mapping.yaml | At PR open |
| `scripts/check-mapping-complete.py` | Validates that every AC is mapped to at least one test name that exists in the diff | At PR review and pre-merge |

## Related

- parent skill: `solo/dev/testing-developer/SKILL.md`
- peer methodologies: `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist`, `solo/dev/testing-developer/qa-exploratory-charter-template`
- external: [Adzic, Specification by Example (Manning, 2011)] · [Hauer, "ATDD by Example" (Addison-Wesley, 2015)] · [Lisa Crispin agile-testing blog on AC-to-test traceability]
