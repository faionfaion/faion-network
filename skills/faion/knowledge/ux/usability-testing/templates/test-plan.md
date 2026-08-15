<!--
purpose: usability test plan skeleton (scope + segments + tasks + success criteria)
consumes: feature spec + recruitment pool
produces: a usability-testing artefact validating against scripts/validate-usability-testing.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600-1500 tokens once filled
variables:
  - name: product_feature
    type: string
    required: true
    description: The product or flow under test, named as users would find it. One flow per plan - a study covering "the app" produces findings nobody can act on before the next release.
  - name: researcher
    type: string
    required: true
    description: Who runs and writes this up. Moderation style changes results, so the name matters when two studies of the same flow disagree with each other.
  - name: session_type
    type: enum
    required: true
    options: [moderated, unmoderated]
    description: Moderated buys you the "why" through follow-up questions; unmoderated buys volume and removes your influence. Pick on which of those two you are short of, not on calendar space.
  - name: session_format
    type: enum
    required: true
    options: [in-person, remote]
    description: Where sessions happen. Remote changes what you can observe - you lose the room, the phone on the desk and the colleague who interrupts, which is often where the finding was.
  - name: participant_count
    type: integer
    required: true
    description: How many participants per segment. Five per segment finds most severe issues; if you have three segments that is fifteen sessions, so decide now rather than after recruiting.
  - name: participant_profile
    type: text
    required: true
    description: Who qualifies, in screener terms - the behaviour they must already have, not the demographic. "Has invoiced a client in the last month" recruits better than "small business owner".
  - name: objective_one
    type: text
    required: true
    description: The first question this study answers, phrased so a result could contradict it. "Can a new user complete first invoice setup unaided?" is answerable; "is the UX good?" is not.
-->
# Usability Test Plan: {{product_feature}}

**Version:** [X.X]
**Date:** [Date]
**Researcher:** {{researcher}}

## Objectives

What questions will this study answer?
1. {{objective_one}}
2. [Question 2]

## Methodology

- **Type:** {{session_type}}
- **Format:** {{session_format}}
- **Duration:** [X] minutes per session
- **Think-aloud:** Yes / No

## Participants

- **Number:** {{participant_count}} per segment
- **Profile:** {{participant_profile}}
- **Recruitment:** [How recruited]
- **Compensation:** [Incentive]

## Tasks

### Task 1: [Name]

**Scenario:** [Context for user — real situation, no UI hints]
**Task:** [What to accomplish]
**Success criteria:** [Observable completion behavior]
**Time limit:** [X minutes]

### Task 2: [Name]

[Same structure]

## Metrics

| Metric | How Measured |
|--------|--------------|
| Task success rate | % completing task without facilitator help |
| Time on task | Duration from task read to completion |
| Error rate | Distinct wrong paths taken |
| Satisfaction | Post-task 1-5 rating |

## Schedule

| Date | Time | Participant |
|------|------|-------------|
| [Date] | [Time] | P1 |

## Deliverables

- [ ] Session recordings
- [ ] Findings report with severity ratings
- [ ] Ranked recommendations for the engineering backlog
