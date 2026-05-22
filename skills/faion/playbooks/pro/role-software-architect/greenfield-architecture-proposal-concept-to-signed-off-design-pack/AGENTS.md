---
slug: greenfield-architecture-proposal-concept-to-signed-off-design-pack
tier: pro
group: role-software-architect
persona: software architect
goal: plan-design
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "From blank slate to a reviewed, signed-off architecture pack: context + container diagrams, ADR set, quality-attribute scenarios, cost model, risk register. Stakeholders (product + eng leads + secu..."
content_id: eeae4a01a6e21a2c
methodology_refs:
  - domain-driven-design
  - observability-architecture
  - quality-attributes-analysis
  - reliability-architecture
  - finops-cost-visibility
  - finops-framework
  - aws-cost-optimization
  - aws-well-architected-framework
  - arch-pattern-clean
  - arch-pattern-ddd
  - arch-pattern-hexagonal
  - architecture-decision-records
  - c4-model
  - caching-architecture
  - data-modeling
  - database-selection
  - decision-tree-architecture-style
  - decision-tree-build-vs-buy
  - decision-tree-cloud-provider
  - decision-tree-tech-stack
  - performance-architecture
  - quality-attributes
  - security-architecture
  - system-design-process
  - trade-off-build-vs-buy
  - trade-off-decision-matrix
  - trade-off-quality-attributes
  - trade-off-stakeholder-communication
  - trade-off-technical-debt
---

# Greenfield architecture proposal — concept to signed-off design pack

**Persona:** software architect · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Context

From blank slate to a reviewed, signed-off architecture pack: context + container diagrams, ADR set, quality-attribute scenarios, cost model, risk register. Stakeholders (product + eng leads + security) approve before any code is written.

This is a global-angle playbook. Deep complexity — expect the work to span multiple sessions if deep = deep, a focused interval if medium, and a single sitting if light. The persona is a software architect operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Greenfield architecture proposal — concept to signed-off design pack ships with written success criteria met and evidence attached
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
- `pro/dev/code-quality/domain-driven-design` (tier: pro)
- `solo/dev/software-architect/arch-pattern-clean` (tier: solo)
- `solo/dev/software-architect/decision-tree-architecture-style` (tier: solo)
- `solo/dev/software-architect/trade-off-build-vs-buy` (tier: solo)

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
- `pro/dev/software-architect/observability-architecture` (tier: pro)
- `solo/dev/software-architect/arch-pattern-ddd` (tier: solo)
- `solo/dev/software-architect/decision-tree-build-vs-buy` (tier: solo)
- `solo/dev/software-architect/trade-off-decision-matrix` (tier: solo)

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
- `solo/dev/software-architect/arch-pattern-hexagonal` (tier: solo)
- `solo/dev/software-architect/decision-tree-cloud-provider` (tier: solo)
- `solo/dev/software-architect/trade-off-quality-attributes` (tier: solo)

### Step 4 — Pilot

**Intent.** Prove the approach on a small, reversible slice before committing the full budget.

**Tasks**
- Pick the lowest-blast-radius slice that exercises the riskiest assumption
- Run the slice end-to-end, including verification and rollback rehearsal
- Write up what changed vs the plan and update the rollback playbook

**Outputs**
- Pilot result
- Updated rollback playbook

**Backed by methodology**
- `pro/dev/software-architect/reliability-architecture` (tier: pro)
- `solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `solo/dev/software-architect/decision-tree-tech-stack` (tier: solo)
- `solo/dev/software-architect/trade-off-stakeholder-communication` (tier: solo)

### Step 5 — Execute

**Intent.** Ship the change behind safe deployment controls.

**Tasks**
- Implement the plan in small, individually shippable steps
- Keep all changes behind feature flags or branch-by-abstraction where reversible
- Update tests + docs in the same change set, never as a follow-up

**Outputs**
- Shipped change set
- Updated tests + docs

**Backed by methodology**
- `pro/infra/cicd-engineer/finops-cost-visibility` (tier: pro)
- `solo/dev/software-architect/c4-model` (tier: solo)
- `solo/dev/software-architect/performance-architecture` (tier: solo)
- `solo/dev/software-architect/trade-off-technical-debt` (tier: solo)

### Step 6 — Verify

**Intent.** Prove the change cleared the success criteria with evidence.

**Tasks**
- Run targeted tests + smoke on the most-trafficked surfaces
- Compare post-change metrics against the baseline captured earlier
- Capture user / operator feedback within the first 48 hours

**Outputs**
- Verification report
- Metric delta vs baseline

**Backed by methodology**
- `pro/infra/cicd-engineer/finops-framework` (tier: pro)
- `solo/dev/software-architect/caching-architecture` (tier: solo)
- `solo/dev/software-architect/quality-attributes` (tier: solo)

### Step 7 — Roll out

**Intent.** Expand the change from pilot scope to full target audience.

**Tasks**
- Increase rollout percentage in measured steps with explicit pause points
- Watch SLO / error budgets on each step; halt if any breach
- Communicate progress + rollback option to all affected stakeholders

**Outputs**
- Rollout log
- Stakeholder update

**Backed by methodology**
- `pro/infra/infrastructure-engineer/aws-cost-optimization` (tier: pro)
- `solo/dev/software-architect/data-modeling` (tier: solo)
- `solo/dev/software-architect/security-architecture` (tier: solo)

### Step 8 — Close

**Intent.** Lock in the gain: documentation, learnings, and a single decision artifact.

**Tasks**
- Write the decision / outcome doc (continue / iterate / revert) with evidence trail
- Update ADRs, runbooks, and pattern memory with what changed
- Schedule the next review checkpoint or archive the workstream

**Outputs**
- Decision doc
- Updated ADR / runbook / memory entry

**Backed by methodology**
- `pro/infra/infrastructure-engineer/aws-well-architected-framework` (tier: pro)
- `solo/dev/software-architect/database-selection` (tier: solo)
- `solo/dev/software-architect/system-design-process` (tier: solo)

## Decision points

- **After Step 1 (Frame).** Advance only after a peer can restate the problem in their own words and agree the criteria are testable.
- **After Step 2 (Assess).** Advance only when baselines are recorded and risks have owners.
- **After Step 3 (Plan).** Advance only when every task has a definition-of-done and the plan fits on one page.
- **After Step 4 (Pilot).** Advance only if the pilot meets its success criteria; otherwise re-plan or kill.
- **After Step 5 (Execute).** Advance only when CI is green, the change is observable in staging, and rollback was rehearsed at least once.
- **After Step 6 (Verify).** Advance only when metrics meet the criteria and no regression alerts are open.
- **After Step 7 (Roll out).** Advance only after 100% rollout has been stable for the agreed soak period.
- **After Step 8 (Close).** Done when the decision doc is single-link shareable and the team can name the next checkpoint.

If any gate fails: stop, re-plan, and either re-enter the previous step or kill the workstream with a written rationale.

## References

Methodologies cited in this playbook (resolve via `faion get-content <slug>`):

- `domain-driven-design` — `faion/knowledge/pro/dev/code-quality/domain-driven-design` (tier: pro)
- `observability-architecture` — `faion/knowledge/pro/dev/software-architect/observability-architecture` (tier: pro)
- `quality-attributes-analysis` — `faion/knowledge/pro/dev/software-architect/quality-attributes-analysis` (tier: pro)
- `reliability-architecture` — `faion/knowledge/pro/dev/software-architect/reliability-architecture` (tier: pro)
- `finops-cost-visibility` — `faion/knowledge/pro/infra/cicd-engineer/finops-cost-visibility` (tier: pro)
- `finops-framework` — `faion/knowledge/pro/infra/cicd-engineer/finops-framework` (tier: pro)
- `aws-cost-optimization` — `faion/knowledge/pro/infra/infrastructure-engineer/aws-cost-optimization` (tier: pro)
- `aws-well-architected-framework` — `faion/knowledge/pro/infra/infrastructure-engineer/aws-well-architected-framework` (tier: pro)
- `arch-pattern-clean` — `faion/knowledge/solo/dev/software-architect/arch-pattern-clean` (tier: solo)
- `arch-pattern-ddd` — `faion/knowledge/solo/dev/software-architect/arch-pattern-ddd` (tier: solo)
- `arch-pattern-hexagonal` — `faion/knowledge/solo/dev/software-architect/arch-pattern-hexagonal` (tier: solo)
- `architecture-decision-records` — `faion/knowledge/solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `c4-model` — `faion/knowledge/solo/dev/software-architect/c4-model` (tier: solo)
- `caching-architecture` — `faion/knowledge/solo/dev/software-architect/caching-architecture` (tier: solo)
- `data-modeling` — `faion/knowledge/solo/dev/software-architect/data-modeling` (tier: solo)
- `database-selection` — `faion/knowledge/solo/dev/software-architect/database-selection` (tier: solo)
- `decision-tree-architecture-style` — `faion/knowledge/solo/dev/software-architect/decision-tree-architecture-style` (tier: solo)
- `decision-tree-build-vs-buy` — `faion/knowledge/solo/dev/software-architect/decision-tree-build-vs-buy` (tier: solo)
- `decision-tree-cloud-provider` — `faion/knowledge/solo/dev/software-architect/decision-tree-cloud-provider` (tier: solo)
- `decision-tree-tech-stack` — `faion/knowledge/solo/dev/software-architect/decision-tree-tech-stack` (tier: solo)
- `performance-architecture` — `faion/knowledge/solo/dev/software-architect/performance-architecture` (tier: solo)
- `quality-attributes` — `faion/knowledge/solo/dev/software-architect/quality-attributes` (tier: solo)
- `security-architecture` — `faion/knowledge/solo/dev/software-architect/security-architecture` (tier: solo)
- `system-design-process` — `faion/knowledge/solo/dev/software-architect/system-design-process` (tier: solo)
- `trade-off-build-vs-buy` — `faion/knowledge/solo/dev/software-architect/trade-off-build-vs-buy` (tier: solo)
- `trade-off-decision-matrix` — `faion/knowledge/solo/dev/software-architect/trade-off-decision-matrix` (tier: solo)
- `trade-off-quality-attributes` — `faion/knowledge/solo/dev/software-architect/trade-off-quality-attributes` (tier: solo)
- `trade-off-stakeholder-communication` — `faion/knowledge/solo/dev/software-architect/trade-off-stakeholder-communication` (tier: solo)
- `trade-off-technical-debt` — `faion/knowledge/solo/dev/software-architect/trade-off-technical-debt` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `architecture-proposal-document-template` (expected tier: pro)
- `cost-model-spreadsheet-template` (expected tier: pro)
