# Regression Test First Bugfix Workflow

## Summary

**One-sentence:** A pinned playbook step: write the failing regression test from the production bug BEFORE writing the fix, then ship both in the same PR.

**One-paragraph:** Produces a workflow record for the most common production-debug situation: a Sentry/Datadog alert fires; the developer reproduces it as a failing test (red) committed FIRST, then writes the minimal fix (green), then ships both atomically. The record links alert → red test → fix PR → post-merge verification + outcome review. TDD exists as a methodology, but "red-test-from-prod-bug" is the missing operationalised flow this artefact pins.

**Ефективно для:** software developer reactively closing the loop між реальним production-багом і запіненим regression-тестом, який доводить, що баг більше не відтворюється.

## Applies If (ALL must hold)

- A production alert (Sentry / Datadog / customer report) has fired with a reproducible signal.
- The codebase has a working test runner (pytest / jest / vitest / go test).
- The bug touches code under regression-friendly control (deterministic given fixed input).
- A named developer owns the fix (assigned in the ticket).
- The team's PR template accepts a "regression test first" checkbox.

## Skip If (ANY kills it)

- Non-deterministic root cause (flaky infra, race conditions in third-party SaaS) where no stable input reproduces it.
- Hotfix where the SLA explicitly allows ship-first, test-after (record the test as follow-up ticket).
- Bug is purely a configuration drift (no code change → no code regression test needed; write a config validator instead).
- Cannot reproduce locally AND no staging environment available — escalate to obs/QA before applying this workflow.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Alert URL | URL | Sentry / Datadog / log aggregator |
| Stack trace + reproducing inputs | text | alert payload |
| Test runner config | TOML/JSON | repo `pyproject.toml` / `package.json` |
| Branch naming convention | string | repo CONTRIBUTING |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/qa-edge-case-spec-template` | The pinned regression spec format this flow may emit on harder cases. |
| `free/dev/software-developer/django-pytest` | Common runner used for the red/green cycle on Django backends. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: explicit trigger, bounded output, evidence-anchored, named owner, iteration loop | ~1000 |
| `content/02-output-contract.xml` | essential | Schema for the workflow record (alert, red-test, fix, verification) + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: cargo-cult, anonymous owner, drift, example bleed, no review, vague trigger | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: capture → reproduce → red test → fix → verify → ship + review | ~600 |
| `content/06-decision-tree.xml` | essential | Decision: full red-test flow vs hotfix-then-test based on SLA + reproducibility | ~300 |

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
| `templates/skeleton.md` | Workflow record skeleton with sections alert / red-test / fix / verification / review. |
| `templates/header.yaml` | Frontmatter schema: owner, version, alert_url, fix_pr_url, last_reviewed. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-regression-test-first-bugfix-workflow.py` | Validate the workflow record schema, links, and ownership. | Pre-merge on the fix PR + weekly staleness scan. |

## Related

- [[qa-edge-case-spec-template]] — pinned spec format this workflow attaches on hard cases.
- [[django-pytest]] — pytest runner pattern.
- [[code-review]] — PR review pattern that gates the red-test-first checkbox.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks between the full red-test-first flow and a hotfix-then-test variant based on SLA pressure, reproducibility, and whether a staging environment can validate the fix before merge.
