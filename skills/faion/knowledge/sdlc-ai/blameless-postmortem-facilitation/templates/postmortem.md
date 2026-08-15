<!--
purpose: blameless postmortem markdown skeleton
consumes: incident timeline + chat + dashboards
produces: report conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~400 tokens
variables:
  - name: incident_id
    type: string
    required: true
    description: The incident id from the tracker. Action items and dashboards cite this document by id, and an id that does not resolve turns both of those into dead ends within a quarter.
  - name: severity
    type: enum
    required: true
    options: [sev1, sev2, sev3]
    description: Severity as declared during the incident, not as it feels afterwards. Downgrading in the write-up is the quiet way an organisation stops noticing how often sev1s happen.
  - name: facilitator
    type: string
    required: true
    description: Who facilitates - and they must not have been on call for this one. That independence is the entire mechanism; a responder facilitating their own postmortem writes a defence.
  - name: responder
    type: string
    required: true
    description: Who was on call, named for context and never for cause. If the name is doing anything beyond establishing who holds the timeline detail, this is not a blameless postmortem.
  - name: first_contributing_factor
    type: text
    required: true
    description: The first factor, phrased as a condition of the system rather than a choice by a person - "the deploy path had no canary step", not "X deployed without checking".
  - name: lucky_break
    type: text
    required: true
    description: Where you got lucky - what would have made this far worse and simply did not happen. This section predicts the next incident better than the timeline does, so do not leave it empty.
-->

# Postmortem: {{incident_id}}

- Severity: {{severity}}
- Facilitator: {{facilitator}} (not on call for this incident)
- On-call responder: {{responder}}

## Timeline
- [HH:MM UTC] [event] ([evidence](url))

## Contributing factors
1. {{first_contributing_factor}}
2. [factor 2]
3. [factor 3]

## Action items

| Title | Owner | Deadline | Verifier |
|-------|-------|----------|----------|
| [item] | [handle] | YYYY-MM-DD | [handle] |

## What went well
- [observation]

## Where we got lucky
- {{lucky_break}}
