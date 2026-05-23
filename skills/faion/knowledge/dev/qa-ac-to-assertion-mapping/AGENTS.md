# Acceptance Criterion to Assertion Mapping

## Summary

**One-sentence:** Map every acceptance criterion (AC) in a user story to a named test with a behavior-asserting assertion, then verify the mapping at PR review — catching the AI-generated-test failure mode where structural assertions hit 100% line coverage without testing what the AC actually says.

**One-paragraph:** Testing methodologies cover techniques and patterns but not the verification step: "for each AC, is there an assertion that actually proves it?" AI-generated tests favour structural assertions (assert method was called, assert no exception raised, assert response status 200) that look productive in PRs but say nothing about behaviour. This discipline introduces an explicit mapping artefact: a small YAML or table next to the story / PR description listing each AC, the test file(s) and test name(s) that cover it, and a one-line note on what assertion proves the behaviour. PR review then walks the mapping: any AC with no behavior-asserting test, or any test where the listed assertion does not match the AC, is blocked. Primary output: an `ac-mapping.yaml` per story or per PR plus a reviewer-facing summary that surfaces unmapped ACs.

**Ефективно для:**

- AI-assisted test generation (Copilot, Cursor, Claude Code) — primary risk surface for structural-only assertions.
- Teams with high line coverage but recurring regressions on shipped behaviour.
- PR review processes that currently rubber-stamp tests because CI is green.
- Compliance-adjacent products where AC traceability is needed but full IV&V is overkill.
- New hires onboarding who need to learn the team's "behaviour first" testing stance.

## Applies If (ALL must hold)

- Team uses user stories or feature specs with explicit acceptance criteria.
- PRs are reviewed before merge.
- AI-assisted test generation is in active use OR the team has experienced under-testing despite high line coverage.
- Product is past MVP with real users (correctness regressions cost money).

## Skip If (ANY kills it)

- Team does not write acceptance criteria — fix that first (writing ACs is the upstream discipline).
- Single-engineer team with no review step — discipline is harder to enforce; lighter pattern works.
- Pure-exploration phase, no real users — formal mapping has negative ROI when requirements are still mutating daily.
- Compliance environment where every test already maps to a formal requirement — the mapping exists in a heavier system, do not duplicate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| User story with explicit AC list | Given/When/Then, numbered, or Gherkin | product |
| PR template with mapping section | markdown skeleton in `.github/` | engineering |
| Definition of "behavior-asserting assertion" | one-page rubric per content/01 | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-risk-matrix-method]] | Risk quadrant tells you which AC mappings need the heaviest assertion scrutiny. |
| [[qa-exploratory-charter-template]] | What AC-mapped tests are NOT supposed to catch — the gap exploratory covers. |
| [[solo-self-code-review-protocol]] | The protocol the reviewer runs the mapping inside. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip rule: explicit mapping, behavior-not-structural, one-AC-many-tests, mapping-at-PR-open, reviewer walks the map | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for ac-mapping.yaml + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: extract ACs → draft mapping → classify assertions → review walk → pre-merge gate | ~800 |
| `content/05-examples.xml` | essential | Worked example: signup-form story mapped to behaviour-asserting tests | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_acceptance_criteria_from_story` | haiku | Mechanical parsing from a structured story field. |
| `propose_test_per_ac` | sonnet | Per-AC bounded judgment against existing test files. |
| `classify_assertion_behavior_vs_structural` | sonnet | Per-assertion bounded judgment using rule from 01. |
| `flag_unmapped_acs_at_pr` | haiku | Set difference between AC list and mapped ACs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ac-mapping.yaml` | YAML skeleton listing ac_id, test_path, test_name, asserted_behavior, assertion_class. |
| `templates/pr-mapping-section.md` | PR-description snippet reviewers expect to find. |
| `templates/_smoke-test.json` | Minimum viable filled-in mapping used by the validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-ac-to-assertion-mapping.py` | Validate ac-mapping.yaml (or its JSON form) against `content/02-output-contract.xml` schema. | Pre-merge gate; on PR open after extract-acs auto-populates. |

## Related

- [[qa-risk-matrix-method]]
- [[qa-exploratory-charter-template]]
- [[solo-self-code-review-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs — AC count, mapping presence, assertion class, reviewer-walked flag — onto a rule id from `content/01-core-rules.xml`. Walk it on every PR open and again at pre-merge; the leaf "skip-this-methodology" is the only legal escape when the precondition gate fails.
