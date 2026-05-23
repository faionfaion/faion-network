# Traceability Auto-Maintenance

## Summary

**One-sentence:** A daily automated job that rebuilds the requirement-to-deliverable traceability graph from tickets / commits / tests and alerts a named owner on broken links.

**One-paragraph:** Hand-maintained traceability matrices rot within weeks; engineers stop linking commits, BAs stop updating the matrix, the artefact becomes performative. This methodology installs a daily job that pulls source-of-truth data (tickets, commits, tests), reconstructs the graph, diffs against yesterday, and alerts a named owner on broken or missing links. Output: a versioned traceability-graph artefact + daily diff log + alert payload.

**Ефективно для:**

- Engagements ≥3 months with structured tickets + commit conventions.
- Regulated builds where audit demands a current trace matrix.
- Multi-team programs where no single human can hand-maintain links.
- Re-engineering of stalled projects where the matrix rotted.

## Applies If (ALL must hold)

- ticket-system + git + test-runner all expose IDs the job can join on
- commit messages reference ticket IDs (enforced or near-100%)
- a named owner accepts the daily alert payload
- engagement is long enough that automation ROI > hand maintenance

## Skip If (ANY kills it)

- ticket-commit-test ID conventions are not in place — fix conventions first
- single-developer engagement <2 months — hand-maintained matrix is cheaper
- no named owner for alerts — alerts will be ignored

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ticket-system API + token | JSON over HTTPS | PM / ops |
| git repo access + commit-message convention | git over SSH | engineering |
| test-runner output with ticket-id tags | JUnit / JSON | QA / CI |
| named owner + alert channel | email / Slack / TG | BA / PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[requirements-traceability-full-lifecycle]] | Defines the graph schema this job rebuilds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: daily refresh, source-of-truth not derived, named alert owner, no silent failure, schema-versioned graph | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for graph artefact + alert payload + diff log | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: silent failure, alert-fatigue, ID-drift, stale graph, missing owner | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: configure connectors → run nightly job → diff → alert → persist graph | 700 |
| `content/06-decision-tree.xml` | essential | Tree on convention compliance + owner + engagement length | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `graph_build` | n/a | Deterministic batch. |
| `alert_drafting` | sonnet | Translate diff into actionable alert text. |
| `convention_audit` | haiku | Mechanical check of commit-message conventions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/traceability-job.yml` | GitHub Actions / cron job skeleton. |
| `templates/alert-payload.json` | Alert payload schema with __faion_header__. |
| `templates/_smoke-test.yml` | Minimum viable cron-job config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-traceability-auto-maintenance.py` | Validates the alert payload + graph artefact against the JSON Schema. | Post-job, pre-publish; pre-commit on the config repo. |

## Related

- [[requirements-traceability-full-lifecycle]]
- [[scope-drift-early-warning-metrics]]
- [[definition-of-done-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
