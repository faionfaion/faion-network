<!--
purpose: Card sort study plan — method, participants, card set, analysis thresholds
consumes: content inventory + participant screener
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
variables:
  - name: project_name
    type: string
    required: true
    description: The site, app or section whose information architecture is being tested. One IA per study - sorting cards from two different products produces clusters that describe neither.
  - name: researcher
    type: string
    required: true
    description: Who runs the study and writes the labels. Card wording is the single biggest source of bias here, so the author of the cards should be on the record.
  - name: sort_type
    type: enum
    required: true
    options: [open, closed, hybrid]
    description: Open discovers the users' own groupings and their names for them; closed tests an IA you already have. Running closed first is how you validate a structure you never questioned.
  - name: tool
    type: string
    required: true
    description: The tool or physical setup used. It decides what analysis you get - some export a co-occurrence matrix, some only a dendrogram, and the analysis plan below assumes the matrix.
  - name: participant_count
    type: integer
    required: true
    description: How many participants. Roughly 15-20 for an open sort, 30 or more for a closed one. Under that the co-occurrence percentages below are not stable enough to draw a boundary with.
  - name: card_count
    type: integer
    required: true
    description: How many cards, 30 to 60. Fewer than 30 rarely shows structure; more than 60 and participants fatigue and start sorting by first letter, which looks like a real finding.
  - name: objective_one
    type: text
    required: true
    description: The first question this answers, phrased so the result could contradict your current navigation. "Do users group billing with account or with reports?" - not "is our IA intuitive?"
-->
# Card Sort Plan: {{project_name}}

**Date:** [Date]
**Researcher:** {{researcher}}

## Objectives

What questions will this study answer?
1. {{objective_one}}
2. [Question 2]

## Method

- **Type:** {{sort_type}}
- **Format:** In-person / Remote
- **Tool:** {{tool}}
- **Duration:** [X] minutes per session

## Participants

- **Number:** {{participant_count}} participants
- **Profile:** [Target user description]
- **Recruitment:** [How recruited]

## Cards

Total: {{card_count}} cards, in user vocabulary rather than internal jargon.

| # | Card Label | Notes |
|---|------------|-------|
| 1 | [User-language label] | [If card needs context] |
| 2 | [User-language label] | |

## Categories (Closed Sort Only)

- [Category 1]
- [Category 2]
- [Does Not Fit] (always include this option)

## Analysis Plan

- Compute the co-occurrence matrix for all card pairs
- Apply thresholds: >70% group together, 40-70% investigate, <40% keep separate
- Report outlier cards (no co-occurrence above 40% with any partner)
- Generate a candidate IA structure from the strong clusters

## Follow-up

- [ ] Tree test on the proposed IA structure before building
