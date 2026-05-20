# Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)

## Context

This playbook covers the synthesis flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Pick up a client-mandated feature in a regulated domain (FinTech payment flow, HIPAA PHI handling, PCI cardholder data path) and ship it with a defensible audit trail. 'Done' = merged PR, evidence pack attached, traceable to the client's control catalogue, and the AI agent did not invent unsafe patterns mid-way.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `free/dev/code-quality/code-review-process`
- `pro/dev/code-quality/domain-driven-design`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `free/dev/software-developer/code-review`
- `pro/dev/software-architect/quality-attributes-analysis`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `geek/sdlc-ai/gov-license-compliance-scan`
- `pro/dev/software-developer/api-gateway-patterns`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `solo/dev/software-developer/api-contract-first`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/requirements-validation`
- `solo/dev/software-developer/api-versioning`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/stakeholder-analysis`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

### 7. Close

Capture lessons, archive the artefacts, and trigger the next-step pipeline.

Tasks:
- Restate the close outcome for this engagement in one sentence.
- Identify who owns the close output and who must approve it.
- Produce the close artefact in the agreed format.

Methodologies:
- `pro/dev/code-quality/clean-architecture`

Decision gate: Advance to the next stage when the close artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `free/dev/code-quality/code-review-process` — methodology cited inside the stages above.
- `free/dev/software-developer/code-review` — methodology cited inside the stages above.
- `geek/sdlc-ai/gov-license-compliance-scan` — methodology cited inside the stages above.
- `geek/sdlc-ai/mr-graph-vs-diff-reviewer` — methodology cited inside the stages above.
- `pro/ba/business-analyst/requirements-validation` — methodology cited inside the stages above.
- `pro/ba/business-analyst/stakeholder-analysis` — methodology cited inside the stages above.
