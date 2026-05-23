---
slug: mr-error-tracker-draft-pr
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: When a prod exception crosses event-count + fixability thresholds in the error tracker (Sentry/Bugsink/Rollbar/Starsling), an agent ingests the structured signal, proposes a patch + regression test, and opens a draft PR bidirectionally linked to the alert.
content_id: "65d8f37cbff1f148"
complexity: deep
produces: playbook-step
est_tokens: 4100
tags: [error-tracker, pull-request, sentry, draft-pr, codeowners]
---
# Error-Tracker to Draft-PR Pipeline

## Summary

**One-sentence:** When a prod exception crosses event-count + fixability thresholds in the error tracker (Sentry/Bugsink/Rollbar/Starsling), an agent ingests the structured signal, proposes a patch + regression test, and opens a draft PR bidirectionally linked to the alert.

**One-paragraph:** Error-Tracker to Draft-PR Pipeline produces a playbook-step artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Production exception with > N events affecting > M users.
- Reproducible-via-trace exception with clear stack + breadcrumbs.
- Repo has CODEOWNERS so PR routes to right reviewer.
- Recent diff covers the exception locus — high-fix-confidence.

## Applies If (ALL must hold)

- Error tracker integrated and emits structured webhooks.
- Repo linked in tracker; recent diffs accessible.
- Agent has commit + PR draft authority on a branch.
- Reviewer policy: draft-PR is reviewed before any merge.

## Skip If (ANY kills it)

- Tracker doesn't expose structured signal — manual triage faster.
- Repo has no tests — patch can't be validated.
- Exception cluster is intermittent / flaky — codemod-style fix risky.
- Reviewer load already saturated — surge of draft PRs is harm, not help.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Error tracker webhook | Sentry/Bugsink/etc. | platform |
| Repo + agent token | draft-PR rights | platform |
| Threshold policy | event-count + fixability score | lead |
| CODEOWNERS file | routing for autodrafts | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mr-graph-vs-diff-reviewer]] | Code review against draft PR |
| [[lint-autofix-vs-flag-decision-rule]] | Sibling policy |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal_ingest` | haiku | Parse webhook payload. |
| `repro_and_diff_locate` | sonnet | Find recent diff overlapping locus. |
| `patch_and_test_draft` | opus | Propose patch + regression test. |
| `pr_open_and_link` | haiku | Open draft PR, link alert. |

## Templates

| File | Purpose |
|------|---------|
| `templates/draft-pr-body.md` | Draft PR body with alert link + patch rationale. |
| `templates/threshold-policy.yaml` | Event-count + fixability threshold config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-tracker-draft-pr.py` | Validate the playbook-step artefact. | pre-merge of pipeline change |

## Related

- [[mr-graph-vs-diff-reviewer]]
- [[inc-postmortem-auto-draft-no-publish]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
