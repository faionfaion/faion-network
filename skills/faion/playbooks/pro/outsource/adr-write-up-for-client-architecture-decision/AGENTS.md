---
slug: adr-write-up-for-client-architecture-decision
tier: pro
group: outsource
persona: P4
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Capture one architectural decision in a way the client's architecture review board accepts, AI agent can replay, and the next dev finds 18 months later. Used 1-3 times per sprint."
content_id: 44ef3544aa2575ed
methodology_refs:
  - requirements-traceability
  - architecture-decision-records
  - quality-attributes-analysis
  - living-documentation
  - stakeholder-engagement
  - business-storytelling
  - selling-ideas
---

# ADR write-up for client architecture decision

## Context

This playbook covers the atomic flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Capture one architectural decision in a way the client's architecture review board accepts, AI agent can replay, and the next dev finds 18 months later. Used 1-3 times per sprint.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/requirements-traceability`
- `solo/sdd/sdd/architecture-decision-records`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `pro/dev/software-architect/quality-attributes-analysis`
- `solo/sdd/sdd/living-documentation`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `pro/pm/pm-traditional/stakeholder-engagement`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `solo/comms/communicator/business-storytelling`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `solo/comms/communicator/selling-ideas`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `solo/dev/software-architect/architecture-decision-records`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `pro/ba/business-analyst/requirements-traceability` — methodology cited inside the stages above.
- `pro/dev/software-architect/quality-attributes-analysis` — methodology cited inside the stages above.
- `pro/pm/pm-traditional/stakeholder-engagement` — methodology cited inside the stages above.
- `solo/comms/communicator/business-storytelling` — methodology cited inside the stages above.
- `solo/comms/communicator/selling-ideas` — methodology cited inside the stages above.
- `solo/dev/software-architect/architecture-decision-records` — methodology cited inside the stages above.
