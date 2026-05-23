# Sentry / Datadog alert triage (in-hours)

## Context

An alert fires in production. On-call engineer triages within minutes using AI-classified context, decides: noise / known / new incident. New incidents enter a runbook flow; known issues get cross-linked. Outcome: every alert closes with a verdict + audit log.

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Receive & Acknowledge

Acknowledge inside the SLA window.

Tasks:
- On-call ack within the SLA (e.g., 5 minutes)
- Open an incident channel + scratchpad
- Page secondary if scope is unclear

Outputs:
- ack timestamp
- incident channel
- page log if any

Decision gate: Advance only when incident channel is live and ack is on the clock.

### 2. Diagnose

Bound the blast radius before fixing.

Tasks:
- Pull dashboards (errors, latency, saturation, deploy log)
- Hypothesize root cause; test cheapest hypothesis first
- Decide: hotfix, rollback, or feature-flag off

Outputs:
- dashboard snapshots
- hypothesis log
- fix-path decision

Decision gate: Advance only when the fix path is chosen with evidence.

### 3. Mitigate

Stop the bleed.

Tasks:
- Execute the chosen mitigation (rollback / flag / hotfix)
- Verify error and latency dashboards recover
- Confirm user-impact has stopped

Outputs:
- mitigation actions log
- recovery dashboard
- impact-end note

Decision gate: Advance only when dashboards are green for 15 consecutive minutes.

### 4. Postmortem

Write the blameless postmortem within 48h.

Tasks:
- Document timeline, root cause, contributing factors
- Define action items with owners and dates
- Share postmortem to engineering at large

Outputs:
- postmortem doc
- action items with owners
- share log

Decision gate: Required output: a published blameless postmortem.

## Decision points

- Stage 1 (Receive & Acknowledge): Advance only when incident channel is live and ack is on the clock.
- Stage 2 (Diagnose): Advance only when the fix path is chosen with evidence.
- Stage 3 (Mitigate): Advance only when dashboards are green for 15 consecutive minutes.
- Stage 4 (Postmortem): Required output: a published blameless postmortem.

## References

- `inc-postmortem-auto-draft-no-publish`
- `inc-read-only-investigation-default`
- `inc-runbook-as-markdown-tagged-steps`
- `inc-tool-tier-approval-gate`
- `task-agent-fixable-triage-gate`
- `tracker-ai-triage-classify-route`
- `api-monitoring-alerting`
- `api-monitoring-logging`
- `api-monitoring-metrics`
- `mistake-memory`

Gaps (status: draft until empty):
- `alert-triage-decision-tree` (see `gaps[]` in `playbook.yaml`)
- `service-ownership-map-template` (see `gaps[]` in `playbook.yaml`)
