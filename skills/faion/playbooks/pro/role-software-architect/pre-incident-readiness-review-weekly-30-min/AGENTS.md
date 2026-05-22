---
slug: pre-incident-readiness-review-weekly-30-min
tier: pro
group: role-software-architect
persona: software architect
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Done = the top-N production-critical services have current runbooks, on-call rotation, alert routing, and SLO dashboards; any gap is owned with a date; SLO burn-rate trend is reviewed and acted on.
content_id: 41576aa5c6a103da
methodology_refs:
  - inc-runbook-as-markdown-tagged-steps
  - observability-architecture
  - reliability-architecture
  - risk-register
---

# Pre-incident readiness review (weekly 30-min)

**Persona:** software architect · **Tier:** pro · **Complexity:** light · **Angle:** atomic

## Context

Done = the top-N production-critical services have current runbooks, on-call rotation, alert routing, and SLO dashboards; any gap is owned with a date; SLO burn-rate trend is reviewed and acted on.

This is a atomic-angle playbook. Light complexity — expect the work to span multiple sessions if light = deep, a focused interval if medium, and a single sitting if light. The persona is a software architect operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Pre-incident readiness review (weekly 30-min) ships with written success criteria met and evidence attached
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
- `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` (tier: geek)

### Step 2 — Plan

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
- `pro/dev/software-architect/observability-architecture` (tier: pro)

### Step 3 — Execute

**Intent.** Ship the change behind safe deployment controls.

**Tasks**
- Implement the plan in small, individually shippable steps
- Keep all changes behind feature flags or branch-by-abstraction where reversible
- Update tests + docs in the same change set, never as a follow-up

**Outputs**
- Shipped change set
- Updated tests + docs

**Backed by methodology**
- `pro/dev/software-architect/reliability-architecture` (tier: pro)

### Step 4 — Verify

**Intent.** Prove the change cleared the success criteria with evidence.

**Tasks**
- Run targeted tests + smoke on the most-trafficked surfaces
- Compare post-change metrics against the baseline captured earlier
- Capture user / operator feedback within the first 48 hours

**Outputs**
- Verification report
- Metric delta vs baseline

**Backed by methodology**
- `pro/pm/project-manager/risk-register` (tier: pro)

### Step 5 — Close

**Intent.** Lock in the gain: documentation, learnings, and a single decision artifact.

**Tasks**
- Write the decision / outcome doc (continue / iterate / revert) with evidence trail
- Update ADRs, runbooks, and pattern memory with what changed
- Schedule the next review checkpoint or archive the workstream

**Outputs**
- Decision doc
- Updated ADR / runbook / memory entry

**Backed by methodology**
- `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` (tier: geek)

## Decision points

- **After Step 1 (Frame).** Advance only after a peer can restate the problem in their own words and agree the criteria are testable.
- **After Step 2 (Plan).** Advance only when every task has a definition-of-done and the plan fits on one page.
- **After Step 3 (Execute).** Advance only when CI is green, the change is observable in staging, and rollback was rehearsed at least once.
- **After Step 4 (Verify).** Advance only when metrics meet the criteria and no regression alerts are open.
- **After Step 5 (Close).** Done when the decision doc is single-link shareable and the team can name the next checkpoint.

If any gate fails: stop, re-plan, and either re-enter the previous step or kill the workstream with a written rationale.

## References

Methodologies cited in this playbook (resolve via `faion get-content <slug>`):

- `inc-runbook-as-markdown-tagged-steps` — `faion/knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` (tier: geek)
- `observability-architecture` — `faion/knowledge/pro/dev/software-architect/observability-architecture` (tier: pro)
- `reliability-architecture` — `faion/knowledge/pro/dev/software-architect/reliability-architecture` (tier: pro)
- `risk-register` — `faion/knowledge/pro/pm/project-manager/risk-register` (tier: pro)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `readiness-matrix-template` (expected tier: pro)
- `slo-burn-rate-review-protocol` (expected tier: pro)
