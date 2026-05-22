---
slug: test-coverage-rebuild-from-30-to-70-6-weeks
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
summary: A neglected codebase is brought from low / uneven test coverage to a defensible, layered test pyramid that protects deploys.
content_id: 6c4c4f328101ff7d
methodology_refs:
  - api-testing
  - code-coverage
  - e2e-testing
  - integration-testing
  - tdd-workflow
  - testing
  - mocking-strategies
  - test-fixtures
  - testing-go
  - testing-javascript
  - testing-patterns
  - testing-pytest
  - unit-testing
  - lint-staged-only-not-whole-tree
  - test-consumer-contract-from-spec
  - test-mutation-feedback-loop
  - test-property-based-llm-invariants
  - rust-testing-property
  - playwright-automation
  - trunk-based-ci-gates
  - performance-testing
  - security-testing
  - quality-gates-confidence
---

# Test-coverage rebuild from 30% to 70% (6 weeks)

**Persona:** software developer · **Tier:** solo · **Complexity:** deep · **Angle:** global

## Context

A neglected codebase is brought from low / uneven test coverage to a defensible, layered test pyramid that protects deploys.

This is a global-angle playbook. Deep complexity — expect the work to span multiple sessions if deep = deep, a focused interval if medium, and a single sitting if light. The persona is a software developer operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Test-coverage rebuild from 30% to 70% (6 weeks) ships with written success criteria met and evidence attached
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
- `free/dev/software-developer/api-testing` (tier: free)
- `free/dev/testing-developer/mocking-strategies` (tier: free)
- `geek/sdlc-ai/test-consumer-contract-from-spec` (tier: geek)
- `solo/dev/software-developer/security-testing` (tier: solo)

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
- `free/dev/software-developer/code-coverage` (tier: free)
- `free/dev/testing-developer/test-fixtures` (tier: free)
- `geek/sdlc-ai/test-mutation-feedback-loop` (tier: geek)
- `solo/dev/testing-developer/security-testing` (tier: solo)

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
- `free/dev/software-developer/e2e-testing` (tier: free)
- `free/dev/testing-developer/testing-go` (tier: free)
- `geek/sdlc-ai/test-property-based-llm-invariants` (tier: geek)
- `solo/sdd/sdd/quality-gates-confidence` (tier: solo)

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
- `free/dev/software-developer/integration-testing` (tier: free)
- `free/dev/testing-developer/testing-javascript` (tier: free)
- `pro/dev/backend-systems/rust-testing-property` (tier: pro)

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
- `free/dev/software-developer/tdd-workflow` (tier: free)
- `free/dev/testing-developer/testing-patterns` (tier: free)
- `solo/dev/api-developer/api-testing` (tier: solo)

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
- `free/dev/software-developer/testing` (tier: free)
- `free/dev/testing-developer/testing-pytest` (tier: free)
- `solo/dev/automation-tooling/playwright-automation` (tier: solo)

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
- `free/dev/testing-developer/e2e-testing` (tier: free)
- `free/dev/testing-developer/unit-testing` (tier: free)
- `solo/dev/automation-tooling/trunk-based-ci-gates` (tier: solo)

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
- `free/dev/testing-developer/integration-testing` (tier: free)
- `geek/sdlc-ai/lint-staged-only-not-whole-tree` (tier: geek)
- `solo/dev/software-developer/performance-testing` (tier: solo)

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

- `api-testing` — `faion/knowledge/free/dev/software-developer/api-testing` (tier: free)
- `code-coverage` — `faion/knowledge/free/dev/software-developer/code-coverage` (tier: free)
- `e2e-testing` — `faion/knowledge/free/dev/software-developer/e2e-testing` (tier: free)
- `integration-testing` — `faion/knowledge/free/dev/software-developer/integration-testing` (tier: free)
- `tdd-workflow` — `faion/knowledge/free/dev/software-developer/tdd-workflow` (tier: free)
- `testing` — `faion/knowledge/free/dev/software-developer/testing` (tier: free)
- `e2e-testing` — `faion/knowledge/free/dev/testing-developer/e2e-testing` (tier: free)
- `integration-testing` — `faion/knowledge/free/dev/testing-developer/integration-testing` (tier: free)
- `mocking-strategies` — `faion/knowledge/free/dev/testing-developer/mocking-strategies` (tier: free)
- `test-fixtures` — `faion/knowledge/free/dev/testing-developer/test-fixtures` (tier: free)
- `testing-go` — `faion/knowledge/free/dev/testing-developer/testing-go` (tier: free)
- `testing-javascript` — `faion/knowledge/free/dev/testing-developer/testing-javascript` (tier: free)
- `testing-patterns` — `faion/knowledge/free/dev/testing-developer/testing-patterns` (tier: free)
- `testing-pytest` — `faion/knowledge/free/dev/testing-developer/testing-pytest` (tier: free)
- `unit-testing` — `faion/knowledge/free/dev/testing-developer/unit-testing` (tier: free)
- `lint-staged-only-not-whole-tree` — `faion/knowledge/geek/sdlc-ai/lint-staged-only-not-whole-tree` (tier: geek)
- `test-consumer-contract-from-spec` — `faion/knowledge/geek/sdlc-ai/test-consumer-contract-from-spec` (tier: geek)
- `test-mutation-feedback-loop` — `faion/knowledge/geek/sdlc-ai/test-mutation-feedback-loop` (tier: geek)
- `test-property-based-llm-invariants` — `faion/knowledge/geek/sdlc-ai/test-property-based-llm-invariants` (tier: geek)
- `rust-testing-property` — `faion/knowledge/pro/dev/backend-systems/rust-testing-property` (tier: pro)
- `api-testing` — `faion/knowledge/solo/dev/api-developer/api-testing` (tier: solo)
- `playwright-automation` — `faion/knowledge/solo/dev/automation-tooling/playwright-automation` (tier: solo)
- `trunk-based-ci-gates` — `faion/knowledge/solo/dev/automation-tooling/trunk-based-ci-gates` (tier: solo)
- `performance-testing` — `faion/knowledge/solo/dev/software-developer/performance-testing` (tier: solo)
- `security-testing` — `faion/knowledge/solo/dev/software-developer/security-testing` (tier: solo)
- `security-testing` — `faion/knowledge/solo/dev/testing-developer/security-testing` (tier: solo)
- `quality-gates-confidence` — `faion/knowledge/solo/sdd/sdd/quality-gates-confidence` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `coverage-rebuild-playbook` (expected tier: solo)
- `characterization-test-recipes` (expected tier: solo)
- `mutation-testing-bootstrap` (expected tier: solo)
