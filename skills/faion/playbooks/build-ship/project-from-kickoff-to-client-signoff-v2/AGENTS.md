# Project from kickoff to client signoff (8–12 weeks)

## Context

A signed SOW becomes a delivered project: kickoff, requirements baseline, delivery in waves, change-controlled scope, final acceptance, retainer-or-referral conversation. Net margin and NPS measured.

## Outcome

By the end of this playbook, the operator has run the 6 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 6 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Kickoff

Translate signed SOW into a baselined plan.

Tasks:
- Run a 60-min kickoff covering scope, RACI, success criteria, change process
- Baseline schedule, scope, and acceptance criteria into the project doc
- Set the weekly status cadence and channel

Outputs:
- kickoff deck
- baselined plan
- status cadence calendar

Decision gate: Advance only when client has signed the kickoff summary acknowledging scope.

### 2. Requirements Baseline

Lock the requirements at a level of detail you can deliver against.

Tasks:
- Run elicitation sessions for any ambiguous spec items
- Write acceptance criteria for every deliverable
- Map traceability from requirements to deliverables

Outputs:
- requirements doc
- acceptance criteria table
- traceability matrix

Decision gate: Advance when every deliverable has acceptance criteria and a traceability row.

### 3. Delivery Wave 1

First slice ships under cadence with risk register live.

Tasks:
- Deliver the first wave per the schedule with weekly demos
- Run a risk register; review weekly with one mitigation per top-3 risk
- Send the weekly client status report on a fixed day

Outputs:
- wave-1 demo
- live risk register
- weekly status reports

Decision gate: Advance when wave-1 acceptance criteria are signed off by the client.

### 4. Change-Controlled Scope

Any new ask flows through change control.

Tasks:
- Tag every new request as in-scope, change-request, or rejected
- Price change requests using the rubric; no free additions
- Update the baseline only when a CR is signed

Outputs:
- CR log
- priced CRs
- updated baselines

Decision gate: Advance only when no in-flight unpriced work exists at end of stage.

### 5. Final Acceptance

Pass UAT and get the signoff signature.

Tasks:
- Run UAT against the acceptance-criteria table
- Fix UAT findings until criteria pass at the agreed bar
- Get written client signoff and final invoice paid

Outputs:
- UAT results
- fix log
- signoff + paid invoice

Decision gate: Advance only when signoff is in writing AND final invoice is paid.

### 6. Retainer or Referral Conversation

Convert delivery into recurring or referral.

Tasks:
- Hold the post-delivery review with the buyer; ask for a referral
- Pitch a retainer or maintenance plan with a starting number
- Measure project margin and NPS; log lessons learned

Outputs:
- referral asks
- retainer proposal
- margin + NPS + lessons doc

Decision gate: Required output: explicit yes/no on retainer AND a logged lessons-learned doc.

## Decision points

- Stage 1 (Kickoff): Advance only when client has signed the kickoff summary acknowledging scope.
- Stage 2 (Requirements Baseline): Advance when every deliverable has acceptance criteria and a traceability row.
- Stage 3 (Delivery Wave 1): Advance when wave-1 acceptance criteria are signed off by the client.
- Stage 4 (Change-Controlled Scope): Advance only when no in-flight unpriced work exists at end of stage.
- Stage 5 (Final Acceptance): Advance only when signoff is in writing AND final invoice is paid.
- Stage 6 (Retainer or Referral Conversation): Required output: explicit yes/no on retainer AND a logged lessons-learned doc.

## References

- `acceptance-criteria`
- `elicitation-techniques`
- `requirements-documentation`
- `requirements-prioritization`
- `requirements-traceability`
- `requirements-validation`
- `solution-assessment`
- `ops-customer-success-metrics`
- `ops-upselling-cross-selling`
- `kanban-scaled-agile-ceremonies`
- `scrum-ceremonies`
- `benefits-realization`
- `change-control`
- `communications-management`
- `earned-value-management`
- `lessons-learned`
- `project-closure`
- `quality-management`
- `raci-matrix`
- `risk-management`
- `risk-register`
- `schedule-development`
- `scope-management`
- `stakeholder-engagement`
- `stakeholder-engagement-advanced`
- `team-development`

Gaps (status: draft until empty):
- `agency-kickoff-deck-template` (see `gaps[]` in `playbook.yaml`)
- `agency-status-report-cadence` (see `gaps[]` in `playbook.yaml`)
- `change-request-pricing-rubric` (see `gaps[]` in `playbook.yaml`)
- `agency-uat-checklist` (see `gaps[]` in `playbook.yaml`)
