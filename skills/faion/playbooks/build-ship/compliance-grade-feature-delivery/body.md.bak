# Compliance-grade feature delivery (FinTech / HIPAA / PCI)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** synthesis

## Why this playbook exists

Ship a regulated-domain feature → merged PR + evidence pack + traceable to control catalogue + AI agent did not invent unsafe patterns.

Synthesis playbook: a single feature in a regulated domain (FinTech payment flow, HIPAA PHI handling, PCI cardholder data path) shipped with a defensible audit trail. 'Done' = merged PR, evidence pack attached, traceable to client control catalogue, AI agent contained.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Spec to control

**Intent:** Map the feature to controls before any code.

**Tasks**
- Validate requirements + stakeholder list
- Map feature to client control IDs
- Design API contract first
- Identify versioning impact for any external consumer

**Outputs**
- Control mapping
- API contract
- Versioning note

**Decision gate**

Advance only when every AC is mapped to a control ID.

### Stage 2 — Design for audit

**Intent:** Choose patterns that an auditor likes.

**Tasks**
- Apply clean-architecture and DDD where boundaries matter
- Apply API gateway patterns at security perimeter
- Capture quality attributes impact
- Threat-model the change as code

**Outputs**
- Design doc with control mapping
- Threat model as code artifact

**Decision gate**

Advance only after threat model has been peer-reviewed.

### Stage 3 — Build + audit-grade review

**Intent:** Code the change with reviewable guard rails.

**Tasks**
- Implement with code-review process discipline
- Use MR-graph vs diff reviewer where the platform supports
- Run government/license compliance scan in CI
- Audit-grade code review on the resulting PR

**Outputs**
- Reviewed PR ready to merge

**Decision gate**

Advance only when review references control IDs.

### Stage 4 — Evidence + ship

**Intent:** Attach evidence the auditor will pull later.

**Tasks**
- Run SOC 2 evidence generator if available
- Attach evidence pack to the PR
- Update living docs for the new control posture
- Merge with control IDs in the squash message

**Outputs**
- Evidence pack attached
- Merged PR with control IDs
- Living docs updated

**Decision gate**

Ship only when evidence is attached AND merge message references control IDs.

## Common pitfalls

- Treating compliance as a post-merge concern — evidence gets reconstructed from memory
- AI-generated code with no attestation — auditors disallow it implicitly
- Threat models stored as ad-hoc diagrams — drift before next sprint

## Quality checklist

- Could the auditor pull this PR and trace to a control in <60s?
- Did we attest AI involvement explicitly?
- Did the threat model survive review by someone outside the change?

## Related playbooks

- `audit-grade-code-review-compliance`
- `fintech-hipaa-compliance-audit-prep`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `audit-grade-api-design` (blocks stage 2)
- `hipaa-phi-data-flow-design` (blocks stage 2)
- `pci-dss-scope-minimisation` (blocks stage 2)
- `soc2-evidence-generator-cli` (blocks stage 4)
- `threat-model-as-code` (blocks stage 2)
- `client-control-id-mapping` (blocks stage 1)
- `compliance-aware-code-review-checklist` (blocks stage 3)
