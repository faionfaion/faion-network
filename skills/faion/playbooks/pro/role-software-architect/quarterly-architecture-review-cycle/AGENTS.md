---
slug: quarterly-architecture-review-cycle
tier: pro
group: role-software-architect
persona: software architect
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "A recurring (every ~13 weeks) architecture-health review across the team's owned systems. Done = published delta report covering drift from ADRs, debt heatmap, fitness-function results, top 3 risks..."
content_id: e11793c096557f75
methodology_refs:
  - inc-postmortem-auto-draft-no-publish
  - kb-agents-md-context-pyramid
  - quality-attributes-analysis
  - dora-metrics
  - architecture-decision-records
  - c4-model
  - trade-off-decision-matrix
  - trade-off-stakeholder-communication
  - trade-off-technical-debt
---

# Quarterly architecture review cycle

**Persona:** software architect · **Tier:** pro · **Complexity:** medium · **Angle:** global

## Context

A recurring (every ~13 weeks) architecture-health review across the team's owned systems. Done = published delta report covering drift from ADRs, debt heatmap, fitness-function results, top 3 risks, and 3-5 commitments for next quarter. Optimised to be an enabler not a blocker.

This is a global-angle playbook. Medium complexity — expect the work to span multiple sessions if medium = deep, a focused interval if medium, and a single sitting if light. The persona is a software architect operating in a team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Quarterly architecture review cycle ships with written success criteria met and evidence attached
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
- `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` (tier: geek)
- `solo/dev/software-architect/trade-off-decision-matrix` (tier: solo)

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
- `geek/sdlc-ai/kb-agents-md-context-pyramid` (tier: geek)
- `solo/dev/software-architect/trade-off-stakeholder-communication` (tier: solo)

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
- `pro/dev/software-architect/quality-attributes-analysis` (tier: pro)
- `solo/dev/software-architect/trade-off-technical-debt` (tier: solo)

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
- `pro/infra/devops-engineer/dora-metrics` (tier: pro)

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
- `solo/dev/software-architect/architecture-decision-records` (tier: solo)

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
- `solo/dev/software-architect/c4-model` (tier: solo)

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

- `inc-postmortem-auto-draft-no-publish` — `faion/knowledge/geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` (tier: geek)
- `kb-agents-md-context-pyramid` — `faion/knowledge/geek/sdlc-ai/kb-agents-md-context-pyramid` (tier: geek)
- `quality-attributes-analysis` — `faion/knowledge/pro/dev/software-architect/quality-attributes-analysis` (tier: pro)
- `dora-metrics` — `faion/knowledge/pro/infra/devops-engineer/dora-metrics` (tier: pro)
- `architecture-decision-records` — `faion/knowledge/solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `c4-model` — `faion/knowledge/solo/dev/software-architect/c4-model` (tier: solo)
- `trade-off-decision-matrix` — `faion/knowledge/solo/dev/software-architect/trade-off-decision-matrix` (tier: solo)
- `trade-off-stakeholder-communication` — `faion/knowledge/solo/dev/software-architect/trade-off-stakeholder-communication` (tier: solo)
- `trade-off-technical-debt` — `faion/knowledge/solo/dev/software-architect/trade-off-technical-debt` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `fitness-functions-as-code` (expected tier: pro)
- `architecture-debt-scoring-rubric` (expected tier: pro)
- `architecture-review-cadence-protocol` (expected tier: pro)
