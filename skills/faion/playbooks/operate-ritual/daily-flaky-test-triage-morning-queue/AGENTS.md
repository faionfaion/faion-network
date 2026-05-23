# Daily flaky-test triage (morning queue)

## Context

Triage overnight CI flakes; quarantine, root-cause one, log the rest with reproducer hypotheses so the trust delta is positive by standup.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Triage overnight CI flakes; quarantine, root-cause one, log the rest with reproducer hypotheses so the trust delta is positive by standup.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Daily flaky-test triage (morning queue).

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `free/dev/code-quality/code-coverage`

Outputs:
- Written current-state map (1 page)
- Top-3 risk list with owners

### 2. Plan

Convert audit findings into a defensible execution plan with explicit cuts.

Tasks:
- Define done-state acceptance criteria
- Sequence the smallest set of changes that ship the outcome
- Cut everything that does not block the done state

Methodologies:
- `free/dev/code-quality/tech-debt-basics`

Outputs:
- 1-page plan with sequenced steps
- Non-goals list (what we are NOT doing)

### 3. Build

Land the first vertical slice end-to-end in a real environment.

Tasks:
- Implement the slice behind a flag or in a sandbox
- Wire telemetry from day one
- Get a real human (not just CI) to use it

Methodologies:
- `free/dev/testing-developer/mocking-strategies`

Outputs:
- Working slice in a non-prod environment
- Telemetry dashboard for the slice

### 4. Harden

Find the failure modes before users do.

Tasks:
- Run failure-mode tests against the slice (load, edge cases, abuse)
- Close every must-fix; ticket every nice-to-fix
- Re-run telemetry to confirm no regression

Methodologies:
- `free/dev/testing-developer/test-fixtures`

Outputs:
- Failure-mode report + closure log
- Ticketed nice-to-fix backlog

### 5. Pilot

Run with a controlled blast radius before broad rollout.

Tasks:
- Roll out to a controlled subset (canary, beta team, single client)
- Measure against acceptance criteria with real traffic / real work
- Capture rollback signal in writing

Methodologies:
- `free/dev/testing-developer/testing-patterns`
- `solo/_gaps/qa-flaky-test-root-cause-taxonomy` (gap)

Outputs:
- Pilot metrics vs. acceptance criteria
- Rollback decision criteria in writing

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.

## References

- `free/dev/code-quality/code-coverage`
- `free/dev/code-quality/tech-debt-basics`
- `free/dev/testing-developer/mocking-strategies`
- `free/dev/testing-developer/test-fixtures`
- `free/dev/testing-developer/testing-patterns`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `qa-flaky-test-root-cause-taxonomy` — bare-slug reference from source; methodology not yet authored
- `qa-flake-ledger-template` — listed in gaps_for_this_playbook from source brainstorm
