---
slug: audit-grade-code-review-compliance
tier: pro
group: delivery-ops
persona: P4
goal: audit-comply
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Review a teammate's PR knowing it may land in a SOC 2 / HIPAA / PCI / banking audit binder → comments hold up under regulator scrutiny, not just 'LGTM'."
content_id: 4425a613b0eb0514
methodology_refs:
  - code-review-basics
  - code-review-process
  - requirements-traceability
  - code-review-cycle
  - code-review
  - tdd-workflow
  - unit-testing
  - clean-architecture
  - audit-grade-code-review-checklist
  - compliance-regime-review-matrix-soc2-hipaa-pci
  - living-documentation
  - lessons-learned
  - ai-generated-code-compliance-validation
---

# Audit-grade code review for compliance client

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

Review a teammate's PR knowing it may land in a SOC 2 / HIPAA / PCI / banking audit binder → comments hold up under regulator scrutiny, not just 'LGTM'.

Atomic PR review for a compliance-relevant change. Output: a review with explicit control-traceability comments, recorded test verification, AI-generated code flagged as such, and a verdict that survives later audit walk-through. Standard PR ceremony amplified, not replaced.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

A code review for a compliance client is not a quality check — it is evidence. Six months later an auditor may pull the PR and read your comments cold. If those comments cite control IDs and reference verified tests, the binder is clean. If they read 'LGTM, nice tests', the engagement gets a finding.

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

Framing the change starts with reading the linked ticket, not the diff. Compliance work cuts across files in ways that diff-first review misses. Trace which controls the change touches before you open the code window.

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

Reviewing against control intent — not just code style — is the discipline most reviewers lack. Clean-architecture violations matter, but a missing control test matters more. Comment with control IDs so the auditor can trace your reasoning later.

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

Documentation + verdict is where the AI-attestation lives. If teammates use AI for code, the auditor will ask how it was reviewed. Capture the attestation explicitly. Update living docs if the PR changes an invariant — drift between docs and code is the most common finding in mid-cycle audits.

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

## Closing note

This playbook scales to 2-5 PRs per sprint on a typical compliance engagement. Pair with the compliance-grade feature delivery synthesis playbook for end-to-end coverage from spec through evidence pack.

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `audit-grade-code-review-checklist` (blocks stage 2)
- `compliance-regime-review-matrix-soc2-hipaa-pci` (blocks stage 2)
- `ai-generated-code-compliance-validation` (blocks stage 3)
