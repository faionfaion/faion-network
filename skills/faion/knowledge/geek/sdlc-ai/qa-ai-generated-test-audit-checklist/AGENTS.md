---
slug: qa-ai-generated-test-audit-checklist
tier: solo
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "09088f8a0957d827"
summary: A solo-tier audit checklist for AI-generated test PRs that catches the dominant failure modes — happy-path-only bias, structural assertions, missing failure cases, untested boundary conditions, mock-only verification — before merge.
tags: [ai-generated-tests, audit, pr-review, qa, claude-code, copilot]
---

# AI-Generated Test PR Audit Checklist

## Summary

**One-sentence:** A concrete 12-item audit checklist a solo QA engineer (or reviewing developer) walks through on every AI-generated test PR, catching happy-path bias, structural-only assertions, missing failure cases, and mock-only verification before merge.

**One-paragraph:** AI-generated tests (Copilot, Cursor, Claude Code, Cody) exhibit a consistent bias profile: they cover the happy path well, generate plausible-looking structural assertions, dodge failure cases, mock everything they cannot easily set up, and produce test names that sound thorough without testing the underlying behavior. Faion has `test-mutation-feedback-loop` at the geek tier (AI-agent oriented) but no actionable artifact at the solo tier for a human reviewing AI test output. This checklist is the artifact: 12 items the reviewer walks, with a pass / flag verdict and a one-line repair suggestion. Items cover assertion class (behavior vs structural), failure-case presence, boundary conditions, mock scope, AC mapping, test independence, and naming honesty. Primary output: a filled-in checklist in the PR description plus go/no-go verdict.

## Applies If (ALL must hold)

- PR includes tests authored or significantly assisted by an AI coding assistant
- reviewer is a human (this checklist is not for the AI to self-review)
- merge gate exists where the reviewer can block on quality grounds
- team has experienced the AI-test failure modes in the past (or wants to prevent them)

## Skip If (ANY kills it)

- PR has no test changes — checklist does not apply
- AI assistance was minor (single-line completion) — overhead exceeds benefit
- team is in throwaway-prototype phase with no real users — test quality investment has negative ROI
- mature TDD-driven team where AI tests follow human-written test specs — the spec acts as a stronger gate already

## Prerequisites

- PR template includes a section for the filled-in checklist
- reviewer has 10-15 minutes to walk the checklist
- a baseline of what "good" looks like for the team's stack (see content/01 for examples)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/qa-ac-to-assertion-mapping` | The AC mapping is one of the checklist's inputs |
| `pro/dev/code-quality/mutation-testing-ci-gate` | Mutation testing is the long-term safety net; this checklist is the short-term review tool |
| `geek/sdlc-ai/test-mutation-feedback-loop` | The geek-tier AI-agent variant; this is the solo-tier human variant |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules covering the 12 checklist items, grouped: assertion class, failure cases, boundaries, mocks, naming | ~1000 |
| `content/02-output-contract.xml` | essential | Checklist YAML schema and reviewer verdict format | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes specific to AI tests with detectors + repairs | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pre_review_lint_pass` | haiku | Automated detector pass on the diff before human walks the list |
| `assertion_class_classification` | sonnet | Per-test bounded judgment |
| `failure_case_gap_analysis` | sonnet | Per-AC judgment on whether a failure case is missing |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-checklist.yaml` | The 12 items with pass / flag fields per item |
| `templates/pr-description-section.md` | PR description snippet the reviewer fills in |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/ai-test-prelint.py` | Lints test diff for known AI-output anti-patterns (excessive mocks, no failure cases, structural-only assertions, generic test names) | At PR open |
| `scripts/checklist-required.py` | Blocks PR-ready transition until the checklist is filled in | At PR-ready gate |

## Related

- parent skill: `geek/sdlc-ai/SKILL.md` (note: this methodology is solo-tier but placed under geek/sdlc-ai for taxonomy reasons)
- peer methodologies: `solo/dev/testing-developer/qa-ac-to-assertion-mapping`, `pro/dev/code-quality/mutation-testing-ci-gate`
- external: [Coplien and Bjørnvig, Lean Architecture (Wiley, 2010)] · [Kent Beck Test-Commit-Revert blog] · [Microsoft Research "DocPrompting" failure-case analysis] · [GitHub Copilot Test Generation Quality reports]
