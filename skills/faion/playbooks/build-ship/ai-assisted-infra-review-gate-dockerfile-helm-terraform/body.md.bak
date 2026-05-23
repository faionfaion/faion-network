# AI-assisted infra review gate (Dockerfile + Helm + Terraform)

## Context

Three checklists wired as CI gates that catch the canonical AI-coder mistakes (root user, latest tag, missing limits, missing securityContext, wildcard IAM, unbounded count loops, hardcoded ARNs). PR comment bot uses them.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Three checklists wired as CI gates that catch the canonical AI-coder mistakes (root user, latest tag, missing limits, missing securityContext, wildcard IAM, unbounded count loops, hardcoded ARNs).
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: AI-assisted infra review gate (Dockerfile + Helm + Terraform).

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `geek/sdlc-ai/lint-shellcheck-hadolint-iac-floor`

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
- `geek/sdlc-ai/sec-codeql-autofix-on-pr`

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
- `pro/infra/devops-engineer/docker-security-hardening`

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
- `pro/_gaps/ai-dockerfile-review-checklist` (gap)

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
- `pro/_gaps/ai-helm-chart-review-checklist` (gap)

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
- `pro/_gaps/ai-infra-review-feedback-loop` (gap)

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
- `pro/_gaps/ai-terraform-review-checklist` (gap)

Outputs:
- Runbook + on-call notes
- SLO + alert config in source control

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.
- **Rollout** → Advance to the next cohort only after the previous is stable for the agreed window.
- **Operate** → Advance when on-call can resolve the top-3 likely incidents without the original author.

## References

- `geek/sdlc-ai/lint-shellcheck-hadolint-iac-floor`
- `geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `pro/infra/devops-engineer/docker-security-hardening`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `ai-dockerfile-review-checklist` — bare-slug reference from source; methodology not yet authored
- `ai-helm-chart-review-checklist` — bare-slug reference from source; methodology not yet authored
- `ai-infra-review-feedback-loop` — bare-slug reference from source; methodology not yet authored
- `ai-terraform-review-checklist` — bare-slug reference from source; methodology not yet authored
