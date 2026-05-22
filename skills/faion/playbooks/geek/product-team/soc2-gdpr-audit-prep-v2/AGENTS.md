---
slug: soc2-gdpr-audit-prep-v2
tier: geek
group: product-team
persona: p6-product-dev-team
goal: audit-comply
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Audit deadline approaches; control evidence is current, gaps closed, auditor walkthrough scripted. Every required control has a tagged artifact in the repo, every secret has a verified custodian, s...
content_id: 3da15aa9bddcadc7
methodology_refs:
  - eu-ai-act-compliance
  - gov-approval-token-signed-jwt
  - gov-conventional-commits-enforced
  - gov-license-compliance-scan
  - gov-sonarqube-ai-code-gate
  - sec-secrets-defense-in-depth
  - sec-trivy-pinned-supply-chain-scan
  - data-analysis
  - interface-analysis
  - process-mining-automation
  - strategy-analysis-current-state
  - strategy-analysis-gap-analysis
  - backup-verification-dr
  - secrets-management
  - security-container-scanning
  - security-policy-as-code
  - security-supply-chain
  - benefits-realization
  - change-control
  - communications-management
  - lessons-learned
  - procurement-management
  - project-closure
  - quality-management
  - risk-register
  - stakeholder-register
  - stakeholder-engagement-advanced
---

# SOC2 / GDPR audit prep (annual)

## Context

Audit deadline approaches; control evidence is current, gaps closed, auditor walkthrough scripted. Every required control has a tagged artifact in the repo, every secret has a verified custodian, supply chain is provably scanned. Output: audit binder, internal walkthrough rehearsed, exceptions logged with remediation owner + date.

## Outcome

By the end of this playbook, the operator has run the 5 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 5 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Define Scope

Which standard, which controls, which systems.

Tasks:
- List the standard(s) in scope (SOC2 type, GDPR articles)
- Identify the systems, vendors, and data flows in scope
- Pick the auditor and the audit window

Outputs:
- scope memo
- system + data-flow map
- auditor + window booked

Decision gate: Advance only when scope and auditor are signed off.

### 2. Map Controls

What controls do we already have; what's missing.

Tasks:
- Map current controls to the standard's requirements
- Identify gaps and pick the owner per gap
- Build the evidence-collection plan

Outputs:
- controls-to-requirements map
- gap list with owners
- evidence plan

Decision gate: Advance when every gap has an owner and a target close date.

### 3. Close Gaps

Implement the missing controls.

Tasks:
- Implement controls per the gap list
- Update policies, code, and vendor agreements as needed
- Train the team on the new controls

Outputs:
- closed gaps log
- updated policies/code/vendor docs
- training records

Decision gate: Advance only when every gap is closed in writing.

### 4. Collect Evidence

Auditors run on evidence, not adjectives.

Tasks:
- Collect evidence per the plan (logs, screenshots, signed docs)
- Run internal pre-audit against the evidence pack
- Fix any pre-audit findings

Outputs:
- evidence pack
- pre-audit report
- fix log

Decision gate: Advance only when pre-audit comes back clean.

### 5. Audit & Remediate

Run the real audit; close findings.

Tasks:
- Host the auditor through the audit window
- Respond to findings within the agreed SLA
- Get the report and the letter / certificate

Outputs:
- audit response log
- remediation log
- final report + letter

Decision gate: Required output: a clean (or remediated) audit letter.

## Decision points

- Stage 1 (Define Scope): Advance only when scope and auditor are signed off.
- Stage 2 (Map Controls): Advance when every gap has an owner and a target close date.
- Stage 3 (Close Gaps): Advance only when every gap is closed in writing.
- Stage 4 (Collect Evidence): Advance only when pre-audit comes back clean.
- Stage 5 (Audit & Remediate): Required output: a clean (or remediated) audit letter.

## References

- `eu-ai-act-compliance`
- `gov-approval-token-signed-jwt`
- `gov-conventional-commits-enforced`
- `gov-license-compliance-scan`
- `gov-sonarqube-ai-code-gate`
- `sec-secrets-defense-in-depth`
- `sec-trivy-pinned-supply-chain-scan`
- `data-analysis`
- `interface-analysis`
- `process-mining-automation`
- `strategy-analysis-current-state`
- `strategy-analysis-gap-analysis`
- `backup-verification-dr`
- `secrets-management`
- `security-container-scanning`
- `security-policy-as-code`
- `security-supply-chain`
- `benefits-realization`
- `change-control`
- `communications-management`
- `lessons-learned`
- `procurement-management`
- `project-closure`
- `quality-management`
- `risk-register`
- `stakeholder-register`
- `stakeholder-engagement-advanced`

Gaps (status: draft until empty):
- `soc2-control-to-repo-artifact-map` (see `gaps[]` in `playbook.yaml`)
- `gdpr-dsar-runbook-product-dev-team` (see `gaps[]` in `playbook.yaml`)
- `vendor-risk-assessment-template` (see `gaps[]` in `playbook.yaml`)
