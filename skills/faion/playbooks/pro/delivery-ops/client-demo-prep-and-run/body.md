# Client demo prep + run

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

End-of-sprint demo to client stakeholders (often non-technical) → explicit acceptance per AC, action items captured, senior dev runs it solo (not the PM).

Atomic ceremony: end-of-sprint demo with the offshore senior leading. Output: per-AC explicit acceptance, captured action items, recording archived, narrative tailored to executive audience where present. Avoids 'great, send a recording' non-decisions.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Prep narrative

**Intent:** Build the story arc before opening the IDE.

**Tasks**
- Identify primary stakeholder + their question
- Stakeholder-engagement pass for executive comms
- Storytelling frame: problem → choice → outcome
- Selling-ideas patterns for non-tech audience

**Outputs**
- Demo narrative draft (3-5 beats)
- Stakeholder note

**Decision gate**

Advance only when narrative answers the primary stakeholder's question.

### Stage 2 — Script + dry-run

**Intent:** Make sure the demo runs the same in front of the client as in rehearsal.

**Tasks**
- Write demo script tied to AC
- Dry-run end-to-end with team
- Verify environment + data look real, not synthetic
- Prepare fallback for any flaky path
- Scrum-ceremonies discipline on time-box

**Outputs**
- Demo script
- Dry-run notes

**Decision gate**

Advance only after a clean dry-run.

### Stage 3 — Run + collect acceptance

**Intent:** Drive the demo, surface acceptance per AC, capture actions.

**Tasks**
- Run demo; call out AC explicitly per ticket
- Use requirements-validation prompts to lock acceptance
- Capture action items with named owners + dates
- Record the session and archive

**Outputs**
- AC checkmarks per ticket
- Action item list
- Recording archived

**Decision gate**

Done only when acceptance per AC is explicit. 'Looks good' without per-AC sign is incomplete.

## Common pitfalls

- Showing features without tying them to the AC
- Letting acceptance default to 'send the recording'
- Demo-driven development — building flashy things instead of valid ones

## Quality checklist

- Did the primary stakeholder get an answer to their question?
- Did I close every AC live?
- Did I leave with named action owners and dates?

## Related playbooks

- `weekly-client-status-report-outsource`
- `story-points-estimation-poker`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `executive-stakeholder-demo-narrative-frame` (blocks stage 1)
- `sprint-demo-script-template` (blocks stage 2)
