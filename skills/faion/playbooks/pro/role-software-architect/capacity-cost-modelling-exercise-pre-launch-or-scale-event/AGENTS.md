---
slug: capacity-cost-modelling-exercise-pre-launch-or-scale-event
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
summary: Build a defensible capacity + cost projection ahead of a launch / migration / scale event. Done = capacity model with 3 traffic scenarios, cost model tied to cloud price sheet, recommended rightsiz...
content_id: 3b13bbdc0a00845a
methodology_refs:
  - quality-attributes-analysis
  - reliability-architecture
  - finops-cost-visibility
  - finops
  - finops-devops-cost-alerts
  - finops-devops-cost-commitments
  - finops-devops-cost-rightsizing
  - finops-devops-cost-tagging
  - aws-cost-optimization
  - aws-well-architected-framework
  - k8s-scaling-availability
  - architecture-decision-records
  - caching-architecture
  - performance-architecture
  - trade-off-build-vs-buy
---

# Capacity + cost-modelling exercise (pre-launch or scale-event)

**Persona:** software architect · **Tier:** pro · **Complexity:** medium · **Angle:** global

## Context

Build a defensible capacity + cost projection ahead of a launch / migration / scale event. Done = capacity model with 3 traffic scenarios, cost model tied to cloud price sheet, recommended rightsizing actions, and a finance sign-off.

This is a global-angle playbook. Medium complexity — expect the work to span multiple sessions if medium = deep, a focused interval if medium, and a single sitting if light. The persona is a software architect operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Capacity + cost-modelling exercise (pre-launch or scale-event) ships with written success criteria met and evidence attached
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
- `pro/dev/software-architect/quality-attributes-analysis` (tier: pro)
- `pro/infra/devops-engineer/finops-devops-cost-rightsizing` (tier: pro)
- `solo/dev/software-architect/caching-architecture` (tier: solo)

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
- `pro/dev/software-architect/reliability-architecture` (tier: pro)
- `pro/infra/devops-engineer/finops-devops-cost-tagging` (tier: pro)
- `solo/dev/software-architect/performance-architecture` (tier: solo)

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
- `pro/infra/cicd-engineer/finops-cost-visibility` (tier: pro)
- `pro/infra/infrastructure-engineer/aws-cost-optimization` (tier: pro)
- `solo/dev/software-architect/trade-off-build-vs-buy` (tier: solo)

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
- `pro/infra/devops-engineer/finops` (tier: pro)
- `pro/infra/infrastructure-engineer/aws-well-architected-framework` (tier: pro)

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
- `pro/infra/devops-engineer/finops-devops-cost-alerts` (tier: pro)
- `pro/infra/infrastructure-engineer/k8s-scaling-availability` (tier: pro)

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
- `pro/infra/devops-engineer/finops-devops-cost-commitments` (tier: pro)
- `solo/dev/software-architect/architecture-decision-records` (tier: solo)

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

- `quality-attributes-analysis` — `faion/knowledge/pro/dev/software-architect/quality-attributes-analysis` (tier: pro)
- `reliability-architecture` — `faion/knowledge/pro/dev/software-architect/reliability-architecture` (tier: pro)
- `finops-cost-visibility` — `faion/knowledge/pro/infra/cicd-engineer/finops-cost-visibility` (tier: pro)
- `finops` — `faion/knowledge/pro/infra/devops-engineer/finops` (tier: pro)
- `finops-devops-cost-alerts` — `faion/knowledge/pro/infra/devops-engineer/finops-devops-cost-alerts` (tier: pro)
- `finops-devops-cost-commitments` — `faion/knowledge/pro/infra/devops-engineer/finops-devops-cost-commitments` (tier: pro)
- `finops-devops-cost-rightsizing` — `faion/knowledge/pro/infra/devops-engineer/finops-devops-cost-rightsizing` (tier: pro)
- `finops-devops-cost-tagging` — `faion/knowledge/pro/infra/devops-engineer/finops-devops-cost-tagging` (tier: pro)
- `aws-cost-optimization` — `faion/knowledge/pro/infra/infrastructure-engineer/aws-cost-optimization` (tier: pro)
- `aws-well-architected-framework` — `faion/knowledge/pro/infra/infrastructure-engineer/aws-well-architected-framework` (tier: pro)
- `k8s-scaling-availability` — `faion/knowledge/pro/infra/infrastructure-engineer/k8s-scaling-availability` (tier: pro)
- `architecture-decision-records` — `faion/knowledge/solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `caching-architecture` — `faion/knowledge/solo/dev/software-architect/caching-architecture` (tier: solo)
- `performance-architecture` — `faion/knowledge/solo/dev/software-architect/performance-architecture` (tier: solo)
- `trade-off-build-vs-buy` — `faion/knowledge/solo/dev/software-architect/trade-off-build-vs-buy` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `cloud-cost-model-canonical-template` (expected tier: pro)
- `capacity-bottleneck-checklist` (expected tier: pro)
- `egress-cost-hidden-budget-guide` (expected tier: pro)
