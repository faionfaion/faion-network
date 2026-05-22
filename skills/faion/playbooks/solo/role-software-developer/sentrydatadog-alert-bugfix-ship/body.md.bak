# Sentry/Datadog alert → bugfix → ship

**Persona:** software developer · **Tier:** solo · **Complexity:** medium · **Angle:** atomic

## Context

Production alert is acknowledged, reproduced locally, root-caused, fixed with a regression test, deployed, and the alert is either resolved or explicitly suppressed with a linked ticket.

This is a atomic-angle playbook. Medium complexity — expect the work to span multiple sessions if medium = deep, a focused interval if medium, and a single sitting if light. The persona is a software developer operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Sentry/Datadog alert → bugfix → ship ships with written success criteria met and evidence attached
- Baseline → post-change metric delta recorded against the relevant quality attribute
- Rollback path rehearsed at least once and documented in the runbook
- Decision doc (continue / iterate / revert) signed off by named owner

## Steps

Walk the stages in order. Do not advance until each stage's decision gate is met in writing.

### Step 1 — Frame

**Intent.** Name the problem in writing and set explicit success criteria.

**Tasks**
- Write a one-paragraph problem statement tied to a quality attribute or user outcome
- List concrete success criteria (measurable, observable, time-bounded)
- Identify the smallest credible scope that still moves the needle

**Outputs**
- Problem brief
- Success-criteria list
- Scope boundary

**Backed by methodology**
- `free/dev/software-developer/error-handling` (tier: free)
- `pro/dev/software-developer/api-monitoring-logging` (tier: pro)

### Step 2 — Assess

**Intent.** Inventory current state vs target with evidence, not opinion.

**Tasks**
- Run a structured assessment of the affected system (code, tests, docs, ops surface)
- Capture baseline metrics that the work will need to beat
- List the top 5 risks and one mitigation per risk

**Outputs**
- Current-state inventory
- Baseline metrics
- Risk register

**Backed by methodology**
- `free/dev/software-developer/refactoring-patterns` (tier: free)
- `pro/dev/software-developer/api-monitoring-metrics` (tier: pro)

### Step 3 — Plan

**Intent.** Decompose into a sequenced backlog with explicit decision points.

**Tasks**
- Break the work into tasks of ≤1 day each, with dependencies named
- Mark reversible vs irreversible (one-way-door) decisions
- Define rollback / kill conditions for each major step

**Outputs**
- Task plan
- Decision log skeleton
- Rollback playbook

**Backed by methodology**
- `free/dev/testing-developer/integration-testing` (tier: free)
- `solo/dev/automation-tooling/cd-pipelines` (tier: solo)

### Step 4 — Execute

**Intent.** Ship the change behind safe deployment controls.

**Tasks**
- Implement the plan in small, individually shippable steps
- Keep all changes behind feature flags or branch-by-abstraction where reversible
- Update tests + docs in the same change set, never as a follow-up

**Outputs**
- Shipped change set
- Updated tests + docs

**Backed by methodology**
- `free/dev/testing-developer/unit-testing` (tier: free)

### Step 5 — Verify

**Intent.** Prove the change cleared the success criteria with evidence.

**Tasks**
- Run targeted tests + smoke on the most-trafficked surfaces
- Compare post-change metrics against the baseline captured earlier
- Capture user / operator feedback within the first 48 hours

**Outputs**
- Verification report
- Metric delta vs baseline

**Backed by methodology**
- `pro/dev/software-developer/api-monitoring-alerting` (tier: pro)

### Step 6 — Close

**Intent.** Lock in the gain: documentation, learnings, and a single decision artifact.

**Tasks**
- Write the decision / outcome doc (continue / iterate / revert) with evidence trail
- Update ADRs, runbooks, and pattern memory with what changed
- Schedule the next review checkpoint or archive the workstream

**Outputs**
- Decision doc
- Updated ADR / runbook / memory entry

**Backed by methodology**
- `pro/dev/software-developer/api-monitoring-health-checks` (tier: pro)

## Decision points

- **After Step 1 (Frame).** Advance only after a peer can restate the problem in their own words and agree the criteria are testable.
- **After Step 2 (Assess).** Advance only when baselines are recorded and risks have owners.
- **After Step 3 (Plan).** Advance only when every task has a definition-of-done and the plan fits on one page.
- **After Step 4 (Execute).** Advance only when CI is green, the change is observable in staging, and rollback was rehearsed at least once.
- **After Step 5 (Verify).** Advance only when metrics meet the criteria and no regression alerts are open.
- **After Step 6 (Close).** Done when the decision doc is single-link shareable and the team can name the next checkpoint.

If any gate fails: stop, re-plan, and either re-enter the previous step or kill the workstream with a written rationale.

## References

Methodologies cited in this playbook (resolve via `faion get-content <slug>`):

- `error-handling` — `faion/knowledge/free/dev/software-developer/error-handling` (tier: free)
- `refactoring-patterns` — `faion/knowledge/free/dev/software-developer/refactoring-patterns` (tier: free)
- `integration-testing` — `faion/knowledge/free/dev/testing-developer/integration-testing` (tier: free)
- `unit-testing` — `faion/knowledge/free/dev/testing-developer/unit-testing` (tier: free)
- `api-monitoring-alerting` — `faion/knowledge/pro/dev/software-developer/api-monitoring-alerting` (tier: pro)
- `api-monitoring-health-checks` — `faion/knowledge/pro/dev/software-developer/api-monitoring-health-checks` (tier: pro)
- `api-monitoring-logging` — `faion/knowledge/pro/dev/software-developer/api-monitoring-logging` (tier: pro)
- `api-monitoring-metrics` — `faion/knowledge/pro/dev/software-developer/api-monitoring-metrics` (tier: pro)
- `cd-pipelines` — `faion/knowledge/solo/dev/automation-tooling/cd-pipelines` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `alert-to-fix-incident-loop` (expected tier: solo)
- `regression-test-first-bugfix-workflow` (expected tier: solo)
