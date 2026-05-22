---
slug: daily-contractor-standup-v2
tier: pro
group: micro-agency
persona: p5-micro-agency-founder
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Founder runs a 10-minute async standup with 1-3 contractors. Output: blockers surfaced, day's deliverables confirmed, founder unblocked from being the bottleneck."
content_id: 450f66e692278bd3
methodology_refs:
  - scrum-ceremonies
  - communications-management
  - risk-management
  - active-listening
  - feedback
  - stakeholder-communication
---

# Daily contractor standup (async Slack)

## Context

Founder runs a 10-minute async standup with 1-3 contractors. Output: blockers surfaced, day's deliverables confirmed, founder unblocked from being the bottleneck.

## Outcome

By the end of this playbook, the operator has run the 3 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 3 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Set Async Norms

Define what 'standup' means in Slack.

Tasks:
- Pick the channel, the time window, and the template
- Decide what counts as a blocker that needs synchronous escalation
- Tell every contractor in writing

Outputs:
- written async norms
- blocker rule
- contractor acknowledgements

Decision gate: Advance when every active contractor has acknowledged the norms.

### 2. Run the Loop Daily

Hit the template every working day.

Tasks:
- Each contractor posts: yesterday, today, blockers — in template
- Founder reads within the 2-hour window and unblocks where needed
- Anything that exceeds the async window gets a same-day call

Outputs:
- daily posts logged
- founder unblocks logged
- synchronous-call log

Decision gate: Advance only when the loop has run 5 consecutive working days.

### 3. Weekly Review

Use the week's posts as the operating signal.

Tasks:
- Aggregate the week's blockers and recurring overruns
- Spot pattern blockers and fix them at the root
- Adjust contractor scope where signal repeats

Outputs:
- blockers digest
- root-fix list
- scope adjustments

Decision gate: Required output: a weekly written adjustment from the standup signal.

## Decision points

- Stage 1 (Set Async Norms): Advance when every active contractor has acknowledged the norms.
- Stage 2 (Run the Loop Daily): Advance only when the loop has run 5 consecutive working days.
- Stage 3 (Weekly Review): Required output: a weekly written adjustment from the standup signal.

## References

- `scrum-ceremonies`
- `communications-management`
- `risk-management`
- `active-listening`
- `feedback`
- `stakeholder-communication`

Gaps (status: draft until empty):
- `async-standup-template-micro-agency` (see `gaps[]` in `playbook.yaml`)
