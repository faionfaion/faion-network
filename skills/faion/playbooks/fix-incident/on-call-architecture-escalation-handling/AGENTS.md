# On-call architecture escalation handling

**Persona:** software architect · **Tier:** geek · **Complexity:** deep · **Angle:** atomic

## Context

Done = an architecture escalation during an incident is resolved without short-circuiting the IC: architect provides options + trade-offs in writing, IC chooses, decision is logged and links into the postmortem; no irreversible decisions are made on a phone call without a 2-line written summary.

This is a atomic-angle playbook. Deep complexity — expect the work to span multiple sessions if deep = deep, a focused interval if medium, and a single sitting if light. The persona is a software architect operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- On-call architecture escalation handling ships with written success criteria met and evidence attached
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
- `geek/sdlc-ai/inc-read-only-investigation-default` (tier: geek)

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
- `pro/dev/software-architect/reliability-architecture` (tier: pro)

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
- `solo/dev/software-architect/architecture-decision-records` (tier: solo)

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
- `solo/dev/software-architect/trade-off-decision-methods` (tier: solo)

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
- `solo/dev/software-architect/trade-off-stakeholder-communication` (tier: solo)

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
- `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` (tier: geek)

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
- `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` (tier: geek)

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

- `inc-postmortem-auto-draft-no-publish` — `faion/knowledge/geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` (tier: geek)
- `inc-read-only-investigation-default` — `faion/knowledge/geek/sdlc-ai/inc-read-only-investigation-default` (tier: geek)
- `reliability-architecture` — `faion/knowledge/pro/dev/software-architect/reliability-architecture` (tier: pro)
- `architecture-decision-records` — `faion/knowledge/solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `trade-off-decision-methods` — `faion/knowledge/solo/dev/software-architect/trade-off-decision-methods` (tier: solo)
- `trade-off-stakeholder-communication` — `faion/knowledge/solo/dev/software-architect/trade-off-stakeholder-communication` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `incident-decision-template` (expected tier: geek)
- `one-way-door-flagging-protocol` (expected tier: geek)
