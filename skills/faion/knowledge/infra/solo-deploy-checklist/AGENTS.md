# Solo Deploy Checklist

## Summary

**One-sentence:** Generates a one-page pre/during/post deploy checklist for a solo operator — explicit go/no-go criteria per line — gated by a documented rollback path.

**One-paragraph:** Solo founders deploy on Friday at 6pm without a rollback path. This methodology pins a fixed 9-pre / 4-during / 4-post checklist with explicit go/no-go per line. Pre: backup, branch, tests green, migration plan, rollback plan, feature-flag default, observability ready, customer comms, time of day. During: deploy in transaction order, watch logs, smoke-test, declare 'stable' after N minutes. Post: mark release, update changelog, verify metrics, sleep. Output: a DeployChecklist artefact.

**Ефективно для:**

- Solo founder pushing to a single live production with no staging duplicate.
- Operator who has shipped a Friday-evening regression at least once.
- Deploys involving DB migrations OR third-party integration changes.
- Audit of recent deploys against the checklist.

## Applies If (ALL must hold)

- Solo founder pushing to a single live production environment.
- Real users will see the change.
- Deploy involves code, DB migration, infra change, or third-party update.
- A rollback path is technically possible.

## Skip If (ANY kills it)

- Internal tooling with no user impact and trivial revert — overkill.
- Static-content micro-update (typo fix, image swap) — overkill.
- Live incident — use incident-triage runbook instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Working deploy script (one-command) | shell script path | operator repo |
| Monitoring surface (Sentry / OpenStatus) | URL | monitoring plan |
| Documented rollback procedure for current version | doc path | operator repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| solo-incident-triage-checklist | Incident triage is the fallback if deploy goes wrong. |
| monitoring-logging | Observability prerequisite consumed from monitoring plan. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-rollback-documented, r2-backup-before-migration, r3-tests-green-not-amber, r4-named-owner, r5-no-friday-evening | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Solo Deploy Checklist artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: no-rollback-path, friday-evening-deploy, untested-migration, observability-missing | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-checklist` | sonnet | Per-deploy contextualisation. |
| `audit-recent-deploys` | sonnet | Diff history against rule-set. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-deploy-checklist.json` | DeployChecklist JSON skeleton (pre/during/post). |
| `templates/solo-deploy-checklist.md` | Markdown checklist to tick through during the deploy. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-deploy-checklist.py` | Validate DeployChecklist JSON against the schema. | Before pushing to prod + post-deploy audit. |

## Related

- [[solo-incident-triage-checklist]]
- [[monitoring-logging]]
- [[deploy-scripts]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
