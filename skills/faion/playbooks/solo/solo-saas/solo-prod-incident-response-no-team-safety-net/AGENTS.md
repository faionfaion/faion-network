---
slug: solo-prod-incident-response-no-team-safety-net
tier: solo
group: solo-saas
persona: P1
goal: fix-incident
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: From alert ping at 3am to root-caused, mitigated, postmortem-documented incident — designed for one person, not a SRE rotation.
content_id: 7a0c5ebd66360c58
methodology_refs:
  - cd-pipelines
  - feature-flags-rollout-targeting
  - health-checks-autoheal
  - monitoring-logging
  - mistake-memory
  - reflexion-learning
---

# Solo prod incident response (no team safety net)

## Intent

From alert ping at 3am to root-caused, mitigated, postmortem-documented incident — designed for one person, not a SRE rotation.

## Scope

From alert ping at 3am to root-caused, mitigated, postmortem-documented incident — designed for one person, not a SRE rotation.

## Stages

### 1. Alert triage

Decide in 60 seconds: real or noise.

Tasks:
- Read the alert payload and recent deploys
- Cross-check status page + health endpoint
- Tag the incident: P0 / P1 / noise

Outputs:
- Triage call
- Health endpoint snapshot
- Initial severity tag

Decision gate: Advance only if confirmed real. If noise: silence alert, return to bed.

### 2. Stop the bleed

Mitigate now, root-cause later.

Tasks:
- Flip the kill switch / disable bad flag / roll back
- Confirm error rate drops
- Post a public status update

Outputs:
- Mitigation action taken
- Error rate delta
- Status page update

Decision gate: Advance only when error rate is below alert threshold.

### 3. Containment + customer comms

Keep trust while you investigate.

Tasks:
- Send a quick we know we are on it message
- Set a follow-up time commitment
- Identify any affected paying customers for direct contact

Outputs:
- Public message
- Follow-up window
- Affected customer list

Decision gate: Advance only when comms are posted with a time commitment.

### 4. Root cause

Find the why, not just the what.

Tasks:
- Replay logs around the incident window
- Check recent deploys, config changes, traffic spikes
- Write a 5-whys for the root cause

Outputs:
- Log replay notes
- Change correlation
- 5-whys doc

Decision gate: Advance only with a named root cause.

### 5. Permanent fix + monitor

Ship the real fix and prove it sticks.

Tasks:
- Ship the code fix with tests
- Add a regression test or monitor
- Verify in production over the next cohort

Outputs:
- Fix commit
- New monitor or test
- Production verification

Decision gate: Advance only when the fix is live AND the new monitor would have caught it.

### 6. Blameless postmortem

Write the doc even when you are the only blamer.

Tasks:
- Fill the blameless postmortem template
- Capture timeline, contributing factors, lessons
- Schedule follow-up backlog items

Outputs:
- Postmortem doc
- Follow-up backlog
- Updated alerting noise budget

Decision gate: Cycle closes when postmortem is committed and follow-ups are scheduled.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
