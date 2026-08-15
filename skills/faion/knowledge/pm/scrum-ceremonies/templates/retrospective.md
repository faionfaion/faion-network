<!--
purpose: Retro structure with metrics, formats (Start-Stop-Continue, 4Ls, Mad-Sad-Glad, Sailboat) and action table
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-1000 tokens when loaded as context
variables:
  - name: sprint_number
    type: string
    required: true
    description: Which sprint this covers. Retros only compound as a series - an unnumbered one cannot be lined up against the retro where the team agreed the same action and forgot it.
  - name: date
    type: string
    required: true
    description: Date the session ran, ISO. Actions below have due dates measured from here, and a retro written up two weeks later is a reconstruction, not a record.
  - name: facilitator
    type: string
    required: true
    description: Who ran the session. Record it and rotate it - a retro facilitated by the same person every sprint quietly becomes that person's agenda with the team's names on it.
  - name: retro_format
    type: enum
    required: true
    options: [start-stop-continue, 4Ls, mad-sad-glad, sailboat]
    description: Which format you ran. Format shapes what surfaces - a team running one format for a year stops finding new problems and concludes it has none.
  - name: attendees
    type: text
    required: true
    description: Everyone present, by name. Absences matter: an action assigned to somebody who was not in the room is an assignment, not a commitment, and it will be back next sprint.
-->

# Sprint {{sprint_number}} Retrospective

**Date:** {{date}}
**Facilitator:** {{facilitator}}
**Format:** {{retro_format}}
**Attendees:** {{attendees}}

## Sprint Metrics

| Metric | Value | Trend |
|--------|-------|-------|
| Velocity | [N] pts | up/down/same |
| Commitment ratio | [N]% | up/down/same |
| Bugs escaped | [N] | up/down/same |

## What Went Well
- [Item 1]
- [Item 2]

## What Could Improve
- [Item 1]
- [Item 2]

## Action Items (owner + due date + linked issue required)

| Action | Owner | Due Date | Issue | Status |
|--------|-------|----------|-------|--------|
| [Action 1] | @name | [Date] | #NNN | Pending |

## Previous Action Items Review

| Action | Owner | Status |
|--------|-------|--------|
| [Previous action] | @name | Done/Not Done |

## Team Health Check

| Dimension | Score (1-5) |
|-----------|-------------|
| Team morale | |
| Process clarity | |
| Technical health | |
