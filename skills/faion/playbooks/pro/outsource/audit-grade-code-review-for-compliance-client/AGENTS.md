---
slug: audit-grade-code-review-for-compliance-client
tier: pro
group: outsource
persona: P4
goal: audit-comply
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Senior reviews a teammate's PR knowing it may end up in a SOC2 / HIPAA / PCI / banking audit binder. Output is a review that holds up under regulator scrutiny, not just 'LGTM'."
content_id: 4e647f1245134cc5
methodology_refs:
  - code-review-basics
  - clean-architecture
  - code-review-process
  - lessons-learned
  - code-review
  - code-review-cycle
  - tdd-workflow
  - living-documentation
  - unit-testing
  - requirements-traceability
---

# Audit-grade code review for compliance client

## Context

This playbook covers the atomic flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Senior reviews a teammate's PR knowing it may end up in a SOC2 / HIPAA / PCI / banking audit binder. Output is a review that holds up under regulator scrutiny, not just 'LGTM'.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `free/dev/code-quality/code-review-basics`
- `pro/dev/code-quality/clean-architecture`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `free/dev/code-quality/code-review-process`
- `pro/pm/pm-traditional/lessons-learned`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `free/dev/software-developer/code-review`
- `solo/sdd/sdd/code-review-cycle`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `free/dev/testing-developer/tdd-workflow`
- `solo/sdd/sdd/living-documentation`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `free/dev/testing-developer/unit-testing`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/requirements-traceability`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `free/dev/code-quality/code-review-basics` — methodology cited inside the stages above.
- `free/dev/code-quality/code-review-process` — methodology cited inside the stages above.
- `free/dev/software-developer/code-review` — methodology cited inside the stages above.
- `free/dev/testing-developer/tdd-workflow` — methodology cited inside the stages above.
- `free/dev/testing-developer/unit-testing` — methodology cited inside the stages above.
- `pro/ba/business-analyst/requirements-traceability` — methodology cited inside the stages above.
