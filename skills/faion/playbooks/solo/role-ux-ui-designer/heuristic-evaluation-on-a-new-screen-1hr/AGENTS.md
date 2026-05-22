---
slug: heuristic-evaluation-on-a-new-screen-1hr
tier: solo
group: role-ux-ui-designer
persona: Designer running a heuristic eval on a new or changed screen
goal: discover-validate
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "One screen scored against Nielsen's 10 heuristics plus a11y rules; severity-rated issue list ready for engineering and design follow-up."
content_id: 16dba3e45e8f37c1
methodology_refs:
  - cog-walk-process
  - aesthetic-minimalist
  - consistency-standards
  - error-prevention
  - error-recovery
  - flexibility-efficiency
  - help-documentation
  - heuristic-evaluation
  - match-real-world
  - recognition-over-recall
  - user-control-freedom
  - visibility-of-system-status
---

# Heuristic evaluation on a new screen (1hr)

## Context

Designer runs a 1-hour heuristic evaluation on one screen. Walks each of Nielsen's 10 heuristics + project a11y rules, captures issues with severity, and queues follow-ups. Done when the issue list has severities and the top-severity items are queued.

## Outcome

New screen with no review -> severity-rated heuristic issues + ready for engineering follow-up. One screen scored against Nielsen's 10 heuristics plus a11y rules; severity-rated issue list ready for engineering and design follow-up.

## Steps

1. **Set context.** Know the screen's purpose before grading. Tasks: Note user role + task on this screen; Capture entry + exit points; Identify project-specific a11y rules to check.
2. **Walk core heuristics.** Visibility, match, user-control, consistency. Tasks: Check visibility of system status; Check match between system and real world; Check user control + freedom; Check consistency + standards.
3. **Walk error + memory heuristics.** Prevention, recognition, flexibility. Tasks: Check error prevention; Check recognition over recall; Check flexibility + efficiency; Check error recovery.
4. **Walk aesthetic + help.** Minimalism + help paths. Tasks: Check aesthetic + minimalist design; Check help + documentation; Flag content + microcopy issues.
5. **Score severity.** Rank what needs to ship. Tasks: Apply 0-4 severity rubric per issue; Add evidence references (screenshots / quotes); Sort by severity.
6. **Queue + file.** Push top severities into the build queue. Tasks: Open tickets for top-severity items; Tag pattern issues for design-system follow-up; File issue list in the repo.

## Decision points

- **After Set context:** Advance only with context written.
- **After Walk core heuristics:** Advance only after all 4 are walked.
- **After Walk error + memory heuristics:** Advance only after all 4 are walked.
- **After Walk aesthetic + help:** Advance only after both heuristics are walked.
- **After Score severity:** Advance only when severities are assigned.
- **After Queue + file:** Done when top-severity items have tickets.

## References

- `faion/knowledge/pro/ux/ux-researcher/cog-walk-process`
- `faion/knowledge/solo/ux/ux-ui-designer/aesthetic-minimalist`
- `faion/knowledge/solo/ux/ux-ui-designer/consistency-standards`
- `faion/knowledge/solo/ux/ux-ui-designer/error-prevention`
- `faion/knowledge/solo/ux/ux-ui-designer/error-recovery`
- `faion/knowledge/solo/ux/ux-ui-designer/flexibility-efficiency`
- `faion/knowledge/solo/ux/ux-ui-designer/help-documentation`
- `faion/knowledge/solo/ux/ux-ui-designer/heuristic-evaluation`
- `faion/knowledge/solo/ux/ux-ui-designer/match-real-world`
- `faion/knowledge/solo/ux/ux-ui-designer/recognition-over-recall`
- `faion/knowledge/solo/ux/ux-ui-designer/user-control-freedom`
- `faion/knowledge/solo/ux/ux-ui-designer/visibility-of-system-status`
- Related: `a11y-audit-on-one-screen-1hr`, `weekly-design-review-meeting-1hr`
