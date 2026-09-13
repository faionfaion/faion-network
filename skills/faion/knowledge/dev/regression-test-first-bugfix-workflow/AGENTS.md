# Regression Test First Bugfix Workflow

## Summary

**One-sentence:** A pinned playbook step: write the failing regression test from the production bug BEFORE writing the fix, then ship both in the same PR.

**One-paragraph:** Produces a workflow record for the most common production-debug situation: a Sentry/Datadog alert fires; the developer reproduces it as a failing test (red) committed FIRST, then writes the minimal fix (green), then ships both atomically. The record links alert → red test → fix PR → post-merge verification + outcome review. TDD exists as a methodology, but "red-test-from-prod-bug" is the missing operationalised flow this artefact pins.

**Ефективно для:** software developer reactively closing the loop між реальним production-багом і запіненим regression-тестом, який доводить, що баг більше не відтворюється.

## Applies If (ALL must hold)

- A production alert in Sentry, Datadog, a log aggregator or a customer ticket carries a payload (exception type and message or wrong output, request body, locale, timezone, feature flags, record ids) and an issue id.
- Running those payload inputs against the unfixed code reproduces the same failure on three consecutive runs.
- The repo has a test runner with a `tests/regression/` directory (or equivalent) and CI that runs on every pushed commit, so a test-only commit gets its own failing run.
- One developer owns the fix and can be recorded as `role:handle`.
- The alerting tool can keep the issue open until the test merges and reports regression events for the issue over the next 90 days.

## Skip If (ANY kills it)

- No fixed input reproduces the failure (race with a third-party service, infrastructure flake): add structured logging and a synthetic monitor instead; a regression test would flake.
- The bug is configuration drift with no code change: write a config validator, not a code regression test.
- CI does not run per commit, so a test-only commit cannot be shown failing; fix CI first.
- The alert cannot be reproduced locally and no staging environment exists: escalate to observability or QA before this workflow.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Alert issue with payload | URL + issue id + event JSON (exception or wrong output, request body, locale, timezone, flags, ids) | Sentry / Datadog / log aggregator / ticket |
| Test runner and regression directory | `pyproject.toml` / `package.json` / `go.mod` with `tests/regression/` | the repo |
| CI per commit | CI run URLs for a single commit | GitHub Actions / GitLab CI / equivalent |
| Developer handle | `role:handle` | the ticket assignee |
| SLA for the fix | hours until the fix must ship | the incident or on-call policy |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/qa-edge-case-spec-template` | The pinned regression spec format this flow may emit on harder cases. |
| `free/dev/software-developer/django-pytest` | Common runner used for the red/green cycle on Django backends. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: red test committed before fix, fails for the alert reason, inputs from alert payload, deterministic + located, minimal fix with assertions untouched, CI red-then-green, hotfix carries follow-up, alert closed after 90-day window | ~2000 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the workflow record: alert with observed outcome and payload-derived reproducing inputs, red test committed under tests/regression/ with its failing CI run (or pending with a follow-up due within 14 days), fix with first commit and diff size, green CI run, owner, review at merge plus 90 days; valid and invalid records; 8 forbidden patterns | ~3450 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: test after fix, wrong-reason failure, invented inputs, flaky test, assertion edited, hotfix follow-up forgotten | ~1250 |
| `content/04-procedure.xml` | medium | 8 steps: lift inputs from the alert payload, write the red test, commit it alone, confirm the red run in CI, minimal fix in its own commit, green run in CI, merge and date the review at plus 90 days, hotfix variant or close the loop against the alerting tool | ~1850 |
| `content/05-examples.xml` | recommended | Complete record for a Sentry zero-amount checkout bug (tr_TR inputs, red test with failing run 76, 18-line fix, green run 77, 90-day review) with a note per value, plus the same bug fixed the usual way and what the validator prints | ~1650 |
| `content/06-decision-tree.xml` | essential | Decision: full red-test flow vs hotfix-then-test based on SLA + reproducibility | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `reproduce-alert-locally` | sonnet | Mechanical: read stack trace, write minimal repro. |
| `author-red-test` | sonnet | Code-shaped output, deterministic. |
| `author-fix` | opus | Root-cause judgement worth opus tokens. |
| `outcome-review-synthesis` | opus | Cross-cycle: did red-test prevent recurrence? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Workflow record skeleton with sections alert / red-test / fix / verification / review. |
| `templates/skeleton.md` | Workflow record skeleton with sections alert / red-test / fix / verification / review. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-regression-test-first-bugfix-workflow.py` | Validate the workflow record schema, links, and ownership. | Pre-merge on the fix PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[qa-edge-case-spec-template]] — pinned spec format this workflow attaches on hard cases.
- [[django-pytest]] — pytest runner pattern.
- [[code-review]] — PR review pattern that gates the red-test-first checkbox.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks between the full red-test-first flow and a hotfix-then-test variant based on SLA pressure, reproducibility, and whether a staging environment can validate the fix before merge.
