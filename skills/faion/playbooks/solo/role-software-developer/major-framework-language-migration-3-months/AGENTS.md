---
slug: major-framework-language-migration-3-months
tier: solo
group: role-software-developer
persona: software developer
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: An established service is moved across a major version boundary (e.g. Django 4 to 5, React class to hooks, Go 1.x mod restructure) without losing behaviour, with zero unplanned downtime.
content_id: 84cbda08bcdd6224
methodology_refs:
  - code-decomposition-patterns
  - refactoring-patterns
  - tech-debt-basics
  - code-coverage
  - e2e-testing
  - integration-testing
  - mr-codemod-refactor-agent
  - test-golden-master-legacy-rewrite
  - api-monitoring-metrics
  - continuous-delivery
  - perf-test-basics
  - perf-test-tools
  - trunk-based-branch-by-abstraction
  - trunk-based-feature-flags
  - framework-decomposition-patterns
  - tech-debt-management
  - architecture-decision-records
  - trade-off-technical-debt
  - contract-first-development
  - feature-flags
  - performance-testing
  - technical-debt
  - trunk-based-development
  - living-documentation
---

# Major framework / language migration (3 months)

**Persona:** software developer · **Tier:** solo · **Complexity:** deep · **Angle:** global

## Context

An established service is moved across a major version boundary (e.g. Django 4 to 5, React class to hooks, Go 1.x mod restructure) without losing behaviour, with zero unplanned downtime.

This is a global-angle playbook. Deep complexity — expect the work to span multiple sessions if deep = deep, a focused interval if medium, and a single sitting if light. The persona is a software developer operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Major framework / language migration (3 months) ships with written success criteria met and evidence attached
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
- `free/dev/code-quality/code-decomposition-patterns` (tier: free)
- `geek/sdlc-ai/test-golden-master-legacy-rewrite` (tier: geek)
- `solo/dev/code-quality/tech-debt-management` (tier: solo)
- `solo/sdd/sdd/living-documentation` (tier: solo)

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
- `free/dev/code-quality/refactoring-patterns` (tier: free)
- `pro/dev/software-developer/api-monitoring-metrics` (tier: pro)
- `solo/dev/software-architect/architecture-decision-records` (tier: solo)

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
- `free/dev/code-quality/tech-debt-basics` (tier: free)
- `solo/dev/automation-tooling/continuous-delivery` (tier: solo)
- `solo/dev/software-architect/trade-off-technical-debt` (tier: solo)

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
- `free/dev/software-developer/code-coverage` (tier: free)
- `solo/dev/automation-tooling/perf-test-basics` (tier: solo)
- `solo/dev/software-developer/contract-first-development` (tier: solo)

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
- `free/dev/software-developer/e2e-testing` (tier: free)
- `solo/dev/automation-tooling/perf-test-tools` (tier: solo)
- `solo/dev/software-developer/feature-flags` (tier: solo)

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
- `free/dev/software-developer/integration-testing` (tier: free)
- `solo/dev/automation-tooling/trunk-based-branch-by-abstraction` (tier: solo)
- `solo/dev/software-developer/performance-testing` (tier: solo)

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
- `free/dev/software-developer/refactoring-patterns` (tier: free)
- `solo/dev/automation-tooling/trunk-based-feature-flags` (tier: solo)
- `solo/dev/software-developer/technical-debt` (tier: solo)

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
- `geek/sdlc-ai/mr-codemod-refactor-agent` (tier: geek)
- `solo/dev/code-quality/framework-decomposition-patterns` (tier: solo)
- `solo/dev/software-developer/trunk-based-development` (tier: solo)

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

- `code-decomposition-patterns` — `faion/knowledge/free/dev/code-quality/code-decomposition-patterns` (tier: free)
- `refactoring-patterns` — `faion/knowledge/free/dev/code-quality/refactoring-patterns` (tier: free)
- `tech-debt-basics` — `faion/knowledge/free/dev/code-quality/tech-debt-basics` (tier: free)
- `code-coverage` — `faion/knowledge/free/dev/software-developer/code-coverage` (tier: free)
- `e2e-testing` — `faion/knowledge/free/dev/software-developer/e2e-testing` (tier: free)
- `integration-testing` — `faion/knowledge/free/dev/software-developer/integration-testing` (tier: free)
- `refactoring-patterns` — `faion/knowledge/free/dev/software-developer/refactoring-patterns` (tier: free)
- `mr-codemod-refactor-agent` — `faion/knowledge/geek/sdlc-ai/mr-codemod-refactor-agent` (tier: geek)
- `test-golden-master-legacy-rewrite` — `faion/knowledge/geek/sdlc-ai/test-golden-master-legacy-rewrite` (tier: geek)
- `api-monitoring-metrics` — `faion/knowledge/pro/dev/software-developer/api-monitoring-metrics` (tier: pro)
- `continuous-delivery` — `faion/knowledge/solo/dev/automation-tooling/continuous-delivery` (tier: solo)
- `perf-test-basics` — `faion/knowledge/solo/dev/automation-tooling/perf-test-basics` (tier: solo)
- `perf-test-tools` — `faion/knowledge/solo/dev/automation-tooling/perf-test-tools` (tier: solo)
- `trunk-based-branch-by-abstraction` — `faion/knowledge/solo/dev/automation-tooling/trunk-based-branch-by-abstraction` (tier: solo)
- `trunk-based-feature-flags` — `faion/knowledge/solo/dev/automation-tooling/trunk-based-feature-flags` (tier: solo)
- `framework-decomposition-patterns` — `faion/knowledge/solo/dev/code-quality/framework-decomposition-patterns` (tier: solo)
- `tech-debt-management` — `faion/knowledge/solo/dev/code-quality/tech-debt-management` (tier: solo)
- `architecture-decision-records` — `faion/knowledge/solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `trade-off-technical-debt` — `faion/knowledge/solo/dev/software-architect/trade-off-technical-debt` (tier: solo)
- `contract-first-development` — `faion/knowledge/solo/dev/software-developer/contract-first-development` (tier: solo)
- `feature-flags` — `faion/knowledge/solo/dev/software-developer/feature-flags` (tier: solo)
- `performance-testing` — `faion/knowledge/solo/dev/software-developer/performance-testing` (tier: solo)
- `technical-debt` — `faion/knowledge/solo/dev/software-developer/technical-debt` (tier: solo)
- `trunk-based-development` — `faion/knowledge/solo/dev/software-developer/trunk-based-development` (tier: solo)
- `living-documentation` — `faion/knowledge/solo/sdd/sdd/living-documentation` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `migration-impact-mapping` (expected tier: solo)
- `framework-migration-playbook-template` (expected tier: solo)
- `behavior-parity-verification` (expected tier: solo)
