# Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop

## Context

A feature moves through 5 roles with a single living artifact (spec + design + test-plan + runbook). Each role inherits prior context and emits a delta. Handoffs blocked if Definition-of-Ready not met

## Outcome

By the end of this playbook, the operator has run the 5 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 5 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. PM Handoff

Outcome doc, not a Jira link dump.

Tasks:
- PM writes the problem, audience, success signal, non-goals
- Architect reviews and signs off on the doc
- Anything ambiguous goes back to PM until clear

Outputs:
- PM outcome doc
- architect signoff
- ambiguity-resolution log

Decision gate: Advance only when architect signs the doc.

### 2. Architect Handoff

Design doc the dev can build from.

Tasks:
- Architect writes the design: API, data, components, tradeoffs
- Dev reviews; flags anything they can't build
- Address every blocking comment in writing

Outputs:
- design doc
- dev review notes
- blocker resolutions

Decision gate: Advance only when dev confirms they can build it as designed.

### 3. Dev → QA Handoff

Spec + acceptance + how to test.

Tasks:
- Dev hands QA the spec, AC, and test entry-points
- QA writes the test plan from the AC
- Dev unblocks anything that prevents the test plan

Outputs:
- spec + AC delivered
- test plan
- blocker resolutions

Decision gate: Advance only when QA confirms test plan covers every AC.

### 4. QA → DevOps Handoff

Deploy + observe + rollback agreed.

Tasks:
- QA hands DevOps the deploy plan and the rollback drill
- DevOps reviews capacity, monitoring, alerts
- Rollback drill is run before any prod deploy

Outputs:
- deploy + rollback plan
- DevOps review notes
- rollback drill log

Decision gate: Advance only when rollback drill ran clean.

### 5. Close the Loop

Every role signed at every gate.

Tasks:
- After launch, retro the handoff at each gate
- Patch the playbook template with any gap found
- Lock the new template version

Outputs:
- per-gate retro notes
- playbook diff
- new template version

Decision gate: Required output: a written updated handoff playbook.

## Decision points

- Stage 1 (PM Handoff): Advance only when architect signs the doc.
- Stage 2 (Architect Handoff): Advance only when dev confirms they can build it as designed.
- Stage 3 (Dev → QA Handoff): Advance only when QA confirms test plan covers every AC.
- Stage 4 (QA → DevOps Handoff): Advance only when rollback drill ran clean.
- Stage 5 (Close the Loop): Required output: a written updated handoff playbook.

## References

- `code-review`
- `inc-runbook-as-markdown-tagged-steps`
- `task-spec-kit-three-step`
- `test-tdd-red-green-split-agents`
- `architecture-decision-records`
- `backlog-grooming-roadmapping`
- `writing-design-documents`

Gaps (status: draft until empty):
- `definition-of-ready-template` (see `gaps[]` in `playbook.yaml`)
- `definition-of-done-template` (see `gaps[]` in `playbook.yaml`)
- `handoff-protocol-template` (see `gaps[]` in `playbook.yaml`)
- `qa-acceptance-signoff-template` (see `gaps[]` in `playbook.yaml`)
- `release-train-coordination` (see `gaps[]` in `playbook.yaml`)
- `on-call-handoff-protocol` (see `gaps[]` in `playbook.yaml`)
