---
slug: two-hour-refactor-block-on-one-module
tier: solo
group: role-software-developer
persona: software developer
goal: optimize-tune
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "One module is measurably cleaner after the session: smaller functions, removed dead code, types tightened, OR an extracted seam that unblocks a follow-up. NO behavior change, all tests still green."
content_id: 87c7d4a008e7d2d3
methodology_refs:
  - code-decomposition-patterns
  - code-decomposition-principles
  - code-review
  - refactoring-patterns
  - framework-decomposition-patterns
  - tech-debt-management
  - technical-debt
---

# Two-hour refactor block on one module

**Persona:** software developer · **Tier:** solo · **Complexity:** medium · **Angle:** atomic

## Context

One module is measurably cleaner after the session: smaller functions, removed dead code, types tightened, OR an extracted seam that unblocks a follow-up. NO behavior change, all tests still green.

This is a atomic-angle playbook. Medium complexity — expect the work to span multiple sessions if medium = deep, a focused interval if medium, and a single sitting if light. The persona is a software developer operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Two-hour refactor block on one module ships with written success criteria met and evidence attached
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
- `solo/dev/software-developer/technical-debt` (tier: solo)

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
- `free/dev/code-quality/code-decomposition-principles` (tier: free)

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
- `free/dev/software-developer/code-review` (tier: free)

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
- `free/dev/software-developer/refactoring-patterns` (tier: free)

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
- `solo/dev/code-quality/framework-decomposition-patterns` (tier: solo)

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
- `solo/dev/code-quality/tech-debt-management` (tier: solo)

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

- `code-decomposition-patterns` — `faion/knowledge/free/dev/code-quality/code-decomposition-patterns` (tier: free)
- `code-decomposition-principles` — `faion/knowledge/free/dev/code-quality/code-decomposition-principles` (tier: free)
- `code-review` — `faion/knowledge/free/dev/software-developer/code-review` (tier: free)
- `refactoring-patterns` — `faion/knowledge/free/dev/software-developer/refactoring-patterns` (tier: free)
- `framework-decomposition-patterns` — `faion/knowledge/solo/dev/code-quality/framework-decomposition-patterns` (tier: solo)
- `tech-debt-management` — `faion/knowledge/solo/dev/code-quality/tech-debt-management` (tier: solo)
- `technical-debt` — `faion/knowledge/solo/dev/software-developer/technical-debt` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `timeboxed-refactor-session-template` (expected tier: solo)
- `refactor-baseline-metrics-script` (expected tier: solo)
