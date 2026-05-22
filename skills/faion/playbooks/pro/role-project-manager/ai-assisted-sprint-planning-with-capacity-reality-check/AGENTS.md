---
slug: ai-assisted-sprint-planning-with-capacity-reality-check
tier: pro
group: role-project-manager
persona: PM/Scrum Master running sprint planning with AI assistance
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Each sprint produces a committable plan the team actually finishes, based on observed capacity, not nominal.
content_id: 460bb0db9d60a7cf
methodology_refs:
  - ai-in-project-management
  - scrum-ceremonies
  - resource-management
  - scope-management
  - agile-ceremonies-setup
  - predictive-analytics-pm
---

# AI-assisted sprint planning with capacity reality-check

## Context

PM runs sprint planning across an Agile team. This playbook embeds an AI assistant in the loop: pre-grooming readiness check, observed-capacity calculation, must-vs-stretch split, and predictive risk callouts. Done when the rolling 4-sprint commitment-to-completion ratio holds >=0.85.

## Outcome

Sprint planning chaos -> committable plan with >=0.85 commitment-to-completion ratio over rolling 4 sprints. Each sprint produces a committable plan the team actually finishes, based on observed capacity, not nominal.

## Steps

1. No item enters planning if it is not Ready. Run an automated DoR check on candidate items; Flag items missing acceptance criteria or unsized; Push unready items back to refinement
2. Plan against the team you actually have, not the team on paper. Calculate effective capacity using last 4 sprints' completion ratio; Apply known leave / on-call deductions; Reserve buffer for unplanned work (15-20%)
3. Separate what we will finish from what we hope to. Define the Must set that fits within 70-80% of capacity; Define a Stretch set for the remaining 20-30%; Mark each item must/stretch explicitly in the tracker
4. Surface predictable failure modes before commit. Run AI risk scan over commit set; Flag dependency conflicts, sizing outliers, and capacity hotspots; Drop or de-risk items the team cannot defend
5. Record commitments so retros can compare reality. Lock the sprint commit in the tracker; Snapshot the Must + Stretch sets; Append commit set to the predictive analytics log

## Decision points

- **Pre-flight readiness** -> Advance only with all candidate items marked Ready.
- **Observed capacity** -> Advance with one numeric capacity figure everyone agreed to.
- **Must vs stretch** -> Advance when the team commits to Must out loud.
- **AI risk callouts** -> Advance only when all high-severity risks are accepted or mitigated.
- **Commit + log** -> Done when commitment is locked and the log is updated.

## References

- `faion/knowledge/geek/pm/pm-agile/ai-in-project-management`
- `faion/knowledge/pro/pm/pm-agile/scrum-ceremonies`
- `faion/knowledge/pro/pm/pm-traditional/resource-management`
- `faion/knowledge/pro/pm/pm-traditional/scope-management`
- `faion/knowledge/pro/pm/project-manager/agile-ceremonies-setup`
- `faion/knowledge/pro/pm/project-manager/predictive-analytics-pm`
- Related: `async-cross-timezone-delivery-cadence-p4-outsource`, `run-a-30-minute-resource-allocation-review`
