---
slug: story-points-estimation-poker
tier: pro
group: delivery-ops
persona: P4
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "60-90 min poker session for the next sprint → offshore team scale calibrated with client scale, preventing 'why did your 3 take a week' debates."
content_id: f1c3d34af57f4474
methodology_refs:
  - acceptance-criteria
  - active-listening
  - feedback
  - cross-team-points-calibration-protocol
  - scrum-ceremonies
  - cost-estimation
  - spike-vs-estimate-decision-rule
---

# Story-points estimation poker with client team

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** light · **Angle:** atomic

## Why this playbook exists

60-90 min poker session for the next sprint → offshore team scale calibrated with client scale, preventing 'why did your 3 take a week' debates.

Atomic estimation ceremony with a joint offshore + client team. Output: each backlog item sized; offshore and client scales calibrated; explicit spike decisions for unknowns; estimation notes archived. Run weekly or bi-weekly per sprint cadence.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

Poker between an offshore team and a client team is calibration before estimation. Skip the calibration step and the two scales drift inside three sprints; the client team's 3 becomes the offshore team's 5; debates about velocity become debates about teams. Anchor stories, agreed live, prevent that drift.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Calibrate

**Intent:** Lock the scale before estimating anything new.

**Tasks**
- Pick 2 reference stories from previous sprint (one small, one medium)
- Recall how long they actually took
- Agree the scale anchor between offshore + client team
- Active-listening pass for any silent disagreement

**Outputs**
- Anchor reference stories
- Agreed scale

**Decision gate**

Advance only when both teams agree the anchors. If not, recalibrate.

Calibration is the highest-value 15 minutes of the ceremony. Two reference stories — one small, one medium — that both teams actually saw shipped. Recall how long each took. Agree the scale anchor. Without this the ceremony degenerates into a polite voting exercise.

### Stage 2 — Estimate

**Intent:** Run the poker; surface dissent fast.

**Tasks**
- Run poker per ticket; reveal estimates simultaneously
- Discuss outliers; do not average silently
- Use scrum-ceremonies discipline on time-boxing
- Apply cost-estimation patterns where points need defending

**Outputs**
- Estimates per ticket
- Outlier discussion notes

**Decision gate**

Advance only when outliers are resolved by discussion, not majority vote.

Estimation discipline matters. Reveal simultaneously. Discuss outliers loudly; do not let them average silently. Use cost-estimation patterns when one side defends a number — points are not money but they are an information signal that gets reconciled on Friday.

### Stage 3 — Spike or commit

**Intent:** Decide which unknowns become spikes vs estimates.

**Tasks**
- Identify tickets with high uncertainty
- Decide spike vs estimate per the spike-vs-estimate rule
- Tag spike tickets with a time-box
- Archive notes for retro

**Outputs**
- Spike tickets created
- Final estimates committed
- Archived poker notes

**Decision gate**

Ceremony closes only when each backlog item is either sized or spiked.

Spike-vs-estimate is the call most teams make wrong. If three estimators give wildly different numbers, the ticket is a spike — not a story. Tag it with a time-box; size it after the spike. Forcing an estimate on a real unknown produces a number nobody trusts.

## Common pitfalls

- Averaging votes silently — kills the calibration signal
- Estimating without an anchor — drift between teams compounds
- Skipping spikes on big unknowns — sprint then misses

## Quality checklist

- Did we calibrate on actual past stories, not theory?
- Did we resolve outliers by discussion?
- Did every risky item get a spike or an honest estimate?

## Related playbooks

- `jira-ticket-scoping-session`
- `client-demo-prep-and-run`

## Closing note

Schedule poker for the cadence the sprint needs, not the cadence the calendar imposes. Pair with JIRA scoping for ticket prep and with the weekly status report for tracking velocity drift over multiple sprints.

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `cross-team-points-calibration-protocol` (blocks stage 1)
- `spike-vs-estimate-decision-rule` (blocks stage 3)
