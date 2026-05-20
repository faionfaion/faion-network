# Audit-grade code review for compliance client

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

Review a teammate's PR knowing it may land in a SOC 2 / HIPAA / PCI / banking audit binder → comments hold up under regulator scrutiny, not just 'LGTM'.

Atomic PR review for a compliance-relevant change. Output: a review with explicit control-traceability comments, recorded test verification, AI-generated code flagged as such, and a verdict that survives later audit walk-through. Standard PR ceremony amplified, not replaced.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Frame the change

**Intent:** Understand what's being reviewed before commenting.

**Tasks**
- Read the PR description + linked ticket
- Trace requirements: which control(s) does this PR touch?
- Apply code-review basics (scope, intent, side-effects)
- Note the AI-agent involvement marker if present

**Outputs**
- PR framing note (controls touched, AI involvement)

**Decision gate**

Advance only after every touched control ID is listed.

### Stage 2 — Review against control + clean-arch

**Intent:** Compare the diff against the control intent, not just code style.

**Tasks**
- Apply clean-architecture review heuristics
- Comment on TDD / test coverage where AC ties to controls
- Use the compliance-regime matrix to surface regime-specific items
- Code-review pass with control IDs in comments

**Outputs**
- Review comments with control IDs
- Test verification log

**Decision gate**

Advance only when every finding cites a control ID.

### Stage 3 — Document + verdict

**Intent:** Leave evidence that holds up at the audit binder level.

**Tasks**
- Verify AI-generated portions against guardrails
- Update living documentation if the PR changes invariants
- Capture lessons-learned for the next reviewer
- Set verdict with defended rationale

**Outputs**
- Review verdict
- Updated living doc (if any)
- Lessons-learned note

**Decision gate**

Verdict only with defended rationale + AI-attestation if applicable.

## Common pitfalls

- Approving on style without checking control intent
- Failing to flag AI-generated code — auditors increasingly insist on provenance
- Comments worded for the author, not the auditor reading 6 months later

## Quality checklist

- Would the auditor understand my comments without me in the room?
- Did I verify the tests run, not just exist?
- Did I flag AI involvement explicitly?

## Related playbooks

- `compliance-grade-feature-delivery`
- `fintech-hipaa-compliance-audit-prep`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `audit-grade-code-review-checklist` (blocks stage 2)
- `compliance-regime-review-matrix-soc2-hipaa-pci` (blocks stage 2)
- `ai-generated-code-compliance-validation` (blocks stage 3)
