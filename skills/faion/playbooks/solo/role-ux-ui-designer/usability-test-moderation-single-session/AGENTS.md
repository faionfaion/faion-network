---
slug: usability-test-moderation-single-session
tier: solo
group: role-ux-ui-designer
persona: Designer/researcher moderating one usability test session on a prototype
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "One moderated session on a prototype: task success/failure per task, behavioral observations, critical issues flagged same-day for fix triage."
content_id: 1fae2bf60060b54d
methodology_refs:
  - usability-testing
  - error-prevention
  - recognition-over-recall
---

# Usability-test moderation (single session)

## Context

Researcher moderates one usability session on a prototype. Includes brief, task-by-task moderation, observation capture, critical issue triage, and same-day fix-list update. Done when session log is filed and critical issues are flagged with engineering.

## Outcome

Untested prototype slot -> moderated session logged + same-day critical-issue triage. One moderated session on a prototype: task success/failure per task, behavioral observations, critical issues flagged same-day for fix triage.

## Steps

1. **Brief participant.** Set expectations + record consent. Tasks: Explain think-aloud + 'no wrong answers'; Confirm consent + recording; Show the prototype starting state.
2. **Run tasks.** Task-by-task moderation without leading. Tasks: Read each task verbatim; Observe without prompting; ask why after; Record success/fail + observed pain.
3. **Probe critical incidents.** Dig into the worst moments. Tasks: Ask follow-up on each fail or hesitation; Capture verbatim quotes; Cross-reference with prototype heuristics.
4. **Wrap + thank.** Close cleanly. Tasks: Final reflection question; Confirm compensation; Set follow-up expectation.
5. **Same-day triage.** Push critical issues into the team's queue today. Tasks: Flag critical issues to engineering / design lead; Open tickets for must-fix items; File session log + recording in repo.

## Decision points

- **After Brief participant:** Advance only when consent is confirmed.
- **After Run tasks:** Advance only when all tasks are run.
- **After Probe critical incidents:** Advance only after probes are exhausted.
- **After Wrap + thank:** Advance when participant is thanked and dismissed.
- **After Same-day triage:** Done when critical issues have tickets the same day.

## References

- `faion/knowledge/solo/ux/ux-researcher/usability-testing`
- `faion/knowledge/solo/ux/ux-ui-designer/error-prevention`
- `faion/knowledge/solo/ux/ux-ui-designer/recognition-over-recall`
- `faion/knowledge/solo/ux/ux-ui-designer/usability-testing`
- Related: `user-interview-prep-run-1-session`, `usability-test-cycle-end-to-end-3-weeks`
