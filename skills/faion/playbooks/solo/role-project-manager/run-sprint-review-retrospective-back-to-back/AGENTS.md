---
slug: run-sprint-review-retrospective-back-to-back
tier: solo
group: role-project-manager
persona: role-project-manager
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Two ceremonies at sprint close: review (showcase plus stakeholder feedback) and retro (team-internal improvement). Exit with a reviewed increment plus 1-3 concrete action items owned by named people."
content_id: 772453d7d659dccb
methodology_refs:
  - scrum-ceremonies
  - communications-management
  - lessons-learned
  - quality-management
  - stakeholder-engagement
  - team-development
  - notion-pm
---

# Run sprint review + retrospective back-to-back

## Context

Two ceremonies at sprint close: review (showcase plus stakeholder feedback) and retro (team-internal improvement). Exit with a reviewed increment plus 1-3 concrete action items owned by named people.

Tier: **solo**. Complexity: **medium**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Demo path passes a dry run.
- Stakeholder feedback captured against framing questions.
- 1-3 action items with named owners.
- Actions visible in next sprint board.

## Steps

### 1. Review prep

Bring the right artifact to demo.

Tasks:
- Pick the smallest end-to-end slice to demo.
- Test the demo path on staging once.
- Prepare a 3-question framing for stakeholder feedback.

Outputs:
- Demo path + framing questions.

Decision gate: Advance when demo path passes a dry run.

### 2. Run the review

Showcase the increment + capture feedback.

Tasks:
- Demo the increment live (not slides).
- Probe stakeholders with the framing questions.
- Capture feedback in a structured doc.

Outputs:
- Review session feedback.

Decision gate: Advance when feedback is captured against the framing questions.

### 3. Switch context to retro

Reset the room for team-internal work.

Tasks:
- Release client/stakeholder attendees.
- Re-frame the next hour as team-internal.
- Open with a quick energy check.

Outputs:
- Retro setup.

Decision gate: Advance when the room is team-only and energy-checked.

### 4. Rotate retro format

Use a different lens each cycle.

Tasks:
- Pick a retro format (mad-sad-glad, start-stop-continue, 4Ls).
- Run timeboxed gather + group + decide.
- Capture themes, not raw items.

Outputs:
- Retro themes.

Decision gate: Advance when 3-5 themes are surfaced (not raw vent).

### 5. Pick action items

End with 1-3 concrete actions, not 10.

Tasks:
- Pick 1-3 actions the team will actually do.
- Assign each to a named owner.
- Carry over only actions that survived from last retro.

Outputs:
- Action item list (1-3).

Decision gate: Advance when each action has a named owner + check-back.

### 6. Publish + carry forward

Make the actions visible.

Tasks:
- Post the actions to the team channel.
- Add them to the next sprint as visible items.
- Log review feedback for product/PM follow-up.

Outputs:
- Published action items.

Decision gate: Required: actions visible in the next sprint's board.

## Decision points

- Demo live vs slides — live always; slides only when the increment is genuinely non-demoable (infra, security).
- Carry-over actions vs reset — carry over only if the action is still relevant; otherwise close and re-pick.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/scrum-ceremonies`
- `pro/pm/pm-traditional/communications-management`
- `pro/pm/pm-traditional/lessons-learned`
- `pro/pm/pm-traditional/quality-management`
- `pro/pm/pm-traditional/stakeholder-engagement`
- `pro/pm/project-manager/team-development`
- `solo/pm/pm-agile/notion-pm`
