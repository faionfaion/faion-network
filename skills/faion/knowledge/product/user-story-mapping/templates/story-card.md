<!--
purpose: Single story card — placement, story frame, acceptance criteria, error path, size.
consumes: one task from the story grid, its activity and release slice
produces: one story row of the map artefact (r3, r6)
depends-on: content/01-core-rules.xml, templates/story-map.md
token-budget-impact: ~150 tokens once filled
variables:
  - name: task_name
    type: string
    required: true
    description: The task as it appears on the map, in the user's verb - "Upload receipt". Not a component name; a card named after a screen cannot be sliced out of a release.
  - name: activity
    type: string
    required: true
    description: Which backbone activity this sits under. If it does not obviously belong to one, either the backbone is wrong or this task is really two - both worth finding out before estimating.
  - name: release_slice
    type: enum
    required: true
    options: [walking-skeleton, release-1, release-2, parking-lot]
    description: Which slice this card is in. walking-skeleton means the thinnest end-to-end path - if everything looks like it belongs there, nobody has yet been made to choose.
  - name: persona
    type: string
    required: true
    description: The named persona this serves, from your persona set. "As a user" is the phrase that lets a card serve everyone and satisfy no one; name the person.
  - name: user_action
    type: text
    required: true
    description: What they want to do, in their language and at their level of detail. Not the implementation - "attach a photo of the receipt", not "POST multipart to /receipts".
  - name: user_benefit
    type: text
    required: true
    description: What becomes possible or cheaper for them once this exists, measurably if you can. "So that I can use the feature" is a tautology and means nobody asked why this card exists.
  - name: size
    type: enum
    required: true
    options: [XS, S, M, L, XL]
    description: Relative size from the people who will build it. An L or XL on a story map is usually a card that has not been split, and splitting it is the point of the map.
-->

# User Story: {{task_name}}

## Placement
- **Activity:** {{activity}}
- **Release:** {{release_slice}}
- **Priority:** [1-N within release column]

## Story
**As a** {{persona}}
**I want to** {{user_action}}
**So that** {{user_benefit}}

## Acceptance Criteria
- [ ] Given [context], when [action], then [observable result]
- [ ] Given [context], when [action], then [observable result]

## Error/Recovery Path
- [ ] Given [error condition], when [action], then [recovery result]

## Dependencies
- Depends on: [Other stories / backbone items]
- Blocks: [Other stories]

## Estimate
{{size}}

## Notes
[Additional context, error paths, edge cases]
