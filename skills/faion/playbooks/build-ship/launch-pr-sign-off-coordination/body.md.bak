# Launch PR sign-off + coordination

## Context

Feature or release ships with the launch-readiness checklist green, comms drafted, metrics instrumented, and a rollback path documented.

Tier: **solo**. Complexity: **deep**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Readiness checklist green across functions.
- Comms kit reviewed and signed off.
- Launch dashboard receiving live events.
- Rollback rehearsed end-to-end.
- 72h checkpoint note delivered.

## Steps

### 1. Readiness checklist

Walk every function to green before the launch window.

Tasks:
- Confirm engineering ship-readiness (tests, feature flag, rollback path).
- Confirm support has FAQ + triage scripts.
- Confirm marketing has the launch comms drafted.

Outputs:
- Readiness checklist with green/red per function.

Decision gate: Advance when every function is green or has a named owner working a red item.

### 2. Comms draft

Draft the launch comms across channels.

Tasks:
- Draft the blog post + email + in-app message.
- Pressure-test against positioning.
- Get one reviewer per channel.

Outputs:
- Comms kit (blog + email + in-app).

Decision gate: Advance when each comm has a reviewer sign-off.

### 3. Instrument metrics

Confirm the launch is measurable.

Tasks:
- Wire instrumentation for the primary metric.
- Stage a test event end-to-end.
- Build a launch dashboard.

Outputs:
- Live launch dashboard.

Decision gate: Advance when the dashboard receives test events.

### 4. Rollback path

Document and rehearse the rollback.

Tasks:
- Document the rollback steps.
- Rehearse the rollback on staging.
- Name the on-call who will pull the trigger.

Outputs:
- Rollback runbook + named on-call.

Decision gate: Advance when rollback was rehearsed end-to-end.

### 5. Sign-off + ship

Final sign-offs and ship.

Tasks:
- Collect sign-off from product, eng, marketing, support.
- Open a launch chat room.
- Ship at the scheduled launch window.

Outputs:
- Sign-off log + launch chat room.

Decision gate: Advance when every stakeholder signed off in writing.

### 6. 72h watch

Watch the launch closely for the first 72 hours.

Tasks:
- Watch the launch dashboard hourly for the first 24h.
- Triage incoming feedback in the launch chat room.
- Convene a 72h post-launch checkpoint.

Outputs:
- 72h watch log + checkpoint notes.

Decision gate: Required: a written 72h checkpoint note.

## Decision points

- Ship vs hold — a single red in readiness is enough to slip a launch; reds are not opinions.
- Roll back vs forward-fix — roll back if user-facing impact exceeds the documented threshold; forward-fix only for cosmetic bugs.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/product/product-manager/competitive-positioning`
- `pro/product/product-manager/experimentation-at-scale`
- `pro/product/product-manager/feedback-management`
- `pro/product/product-manager/release-planning`
- `pro/product/product-manager/stakeholder-management`
- `solo/product/product-manager/product-launch`
- `solo/product/product-operations/product-analytics`
