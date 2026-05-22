---
slug: test-pyramid-rebalance-too-many-e2e-to-contract-unit
tier: solo
group: role-qa-engineer
persona: QA engineer / test lead in an indie or small-team product context.
goal: optimize-tune
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Test pyramid rebalance: too-many-e2e to contract + unit. Existing suite dominated by slow flaky e2e."
content_id: f7b4df152e203227
methodology_refs:
  - code-coverage
  - e2e-testing
  - integration-testing
  - mocking-strategies
  - tdd-workflow
  - test-fixtures
  - testing-patterns
  - unit-testing
  - test-consumer-contract-from-spec
  - test-mutation-feedback-loop
  - test-self-healing-locators-audited
  - rust-testing-property
  - api-contract-first
  - playwright-automation
  - contract-first-development
---

# Test pyramid rebalance: too-many-e2e to contract + unit

## Context

Existing suite dominated by slow flaky e2e. Done when: e2e count cut by 60–80%, replaced by contract + integration + unit tests with equivalent or greater real coverage, total CI wall-time reduced, escape rate flat or better, and a rule set is in place to prevent re-drift.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Existing suite dominated by slow flaky e2e.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Test pyramid rebalance: too-many-e2e to contract + unit.

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
- `free/dev/testing-developer/e2e-testing`

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
- `free/dev/testing-developer/integration-testing`

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
- `free/dev/testing-developer/mocking-strategies`

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
- `free/dev/testing-developer/tdd-workflow`

Outputs:
- Pilot metrics vs. acceptance criteria
- Rollback decision criteria in writing

### 6. Rollout

Move from pilot to general availability with confidence.

Tasks:
- Stage the rollout in defined cohorts / regions / risk bands
- Hold each stage open until telemetry is clean
- Communicate state to stakeholders at each step

Methodologies:
- `free/dev/testing-developer/test-fixtures`

Outputs:
- Rollout log (cohort-by-cohort)
- Stakeholder update record

### 7. Operate

Hand off as a steady-state operation, not a hero ticket.

Tasks:
- Document the runbook for on-call
- Define the SLO + alert + escalation chain
- Schedule the next review cycle

Methodologies:
- `free/dev/testing-developer/testing-patterns`

Outputs:
- Runbook + on-call notes
- SLO + alert config in source control

### 8. Review

Close the loop with a written retro and clear next-cycle bets.

Tasks:
- Compile evidence trail + metrics from rollout
- Write retro: what worked, what didn't, what we are changing
- Decide explicit continue / iterate / kill for the next cycle

Methodologies:
- `free/dev/testing-developer/unit-testing`
- `geek/sdlc-ai/test-consumer-contract-from-spec`
- `geek/sdlc-ai/test-mutation-feedback-loop`
- `geek/sdlc-ai/test-self-healing-locators-audited`
- `pro/dev/backend-systems/rust-testing-property`
- `solo/dev/api-developer/api-contract-first`
- `solo/dev/automation-tooling/playwright-automation`
- `solo/dev/software-developer/contract-first-development`

Outputs:
- Retro doc with evidence
- Continue / iterate / kill decision for next cycle

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.
- **Rollout** → Advance to the next cohort only after the previous is stable for the agreed window.
- **Operate** → Advance when on-call can resolve the top-3 likely incidents without the original author.
- **Review** → A written decision is mandatory; no 'see how it goes'.

## References

- `free/dev/code-quality/code-coverage`
- `free/dev/testing-developer/e2e-testing`
- `free/dev/testing-developer/integration-testing`
- `free/dev/testing-developer/mocking-strategies`
- `free/dev/testing-developer/tdd-workflow`
- `free/dev/testing-developer/test-fixtures`
- `free/dev/testing-developer/testing-patterns`
- `free/dev/testing-developer/unit-testing`
- `geek/sdlc-ai/test-consumer-contract-from-spec`
- `geek/sdlc-ai/test-mutation-feedback-loop`
- `geek/sdlc-ai/test-self-healing-locators-audited`
- `pro/dev/backend-systems/rust-testing-property`
- `solo/dev/api-developer/api-contract-first`
- `solo/dev/automation-tooling/playwright-automation`
- `solo/dev/software-developer/contract-first-development`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `test-pyramid-policy-enforcement` — listed in gaps_for_this_playbook from source brainstorm
- `page-object-pattern-guide` — listed in gaps_for_this_playbook from source brainstorm
- `e2e-to-contract-migration-recipe` — listed in gaps_for_this_playbook from source brainstorm
