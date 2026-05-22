---
slug: fintech-hipaa-compliance-audit-prep
tier: pro
group: devops-cicd
persona: P4
goal: audit-comply
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Client triggers a compliance audit (SOC 2, PCI DSS QSA, HIPAA, or banking-core) → vendor delivers gap analysis, remediated controls, evidence pack, owners, and audit-day runbook with zero steerco-e...
content_id: 31c9e7ca459280bd
methodology_refs:
  - requirements-traceability
  - strategy-analysis
  - strategy-analysis-current-state
  - strategy-analysis-gap-analysis
  - raci-matrix
  - soc2-control-map-vendor-side
  - azure-nsg-rules
  - azure-private-link
  - backup-basics
  - backup-database-postgres
  - backup-verification-dr
  - secrets-management
  - cicd-cert-rotation-pipeline
  - cicd-mtls-deployment
  - security-sast
  - security-dast
  - security-container-scanning
  - security-supply-chain
  - security-policy-as-code
  - ai-coding-agent-compliance-guardrails
  - api-monitoring-logging
  - quality-management
  - risk-management
  - risk-register
  - pci-dss-vendor-evidence-pack
  - hipaa-baa-vendor-checklist
  - banking-core-data-residency-rules
  - communications-management
  - weekly-status-report
---

# FinTech / HIPAA compliance audit prep (4 weeks)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

Client triggers a compliance audit (SOC 2, PCI DSS QSA, HIPAA, or banking-core) → vendor delivers gap analysis, remediated controls, evidence pack, owners, and audit-day runbook with zero steerco-escalating findings.

Four-week sprint that runs in parallel to delivery. By end of week 4 the vendor side of the audit passes without any findings that escalate to the client steerco. Covers SOC 2 mid-cycle, PCI DSS QSA, HIPAA, or banking-core regulatory scopes. The vendor delivers gap analysis, remediated controls, evidence pack, named owners, and an audit-day runbook.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Scope & control mapping

**Intent:** Lock the exact list of in-scope controls; nothing more, nothing less.

**Tasks**
- Read the regime catalogue with client compliance lead
- Trace each vendor-owned control to its requirement source
- Strategy-analysis: current vs future state per control family
- Open a RACI for audit-day responsibilities

**Outputs**
- Vendor-side control map
- RACI for audit-day
- Out-of-scope list (countersigned)

**Decision gate**

Advance only after client compliance lead signs the vendor-side scope. Else loop back.

### Stage 2 — Gap remediation - infra & secrets

**Intent:** Close the obvious infra gaps before evidence collection starts.

**Tasks**
- Network segmentation review (NSG rules, private link)
- Backup + DR posture (DB backups, verification, RTO/RPO)
- Rotate secrets; document the rotation
- Pipe certificate lifecycle into CI/CD
- Enforce mTLS where data crosses tenants

**Outputs**
- Network diagrams with segmentation evidence
- Backup verification log
- Secrets rotation log
- mTLS deployment evidence

**Decision gate**

Advance when the highest-severity infra gap is closed AND backup verification has at least one successful drill.

### Stage 3 — Gap remediation - SDLC & supply chain

**Intent:** Make the build pipeline auditable end-to-end.

**Tasks**
- SAST + DAST results integrated into CI
- Container scanning gating production deploys
- Supply-chain attestations (SBOM, signatures)
- Policy-as-code for environment promotion
- Coding-agent compliance guardrails so AI-generated PRs are auditable

**Outputs**
- SAST/DAST + scan reports archived
- SBOM + signing evidence
- Policy-as-code repo
- AI-agent guardrails documented

**Decision gate**

Advance when CI gates production deploys on every required scan AND AI guardrails are merged.

### Stage 4 — Evidence pack assembly

**Intent:** Collect, label, and version every artifact the auditor will ask for.

**Tasks**
- Map every control to ≥1 piece of evidence
- Centralise API monitoring logging samples
- Quality-management documentation for the in-scope work
- PCI / HIPAA / banking-specific evidence checklist
- Regulator-aware risk register update

**Outputs**
- Evidence index (control ID → file)
- Risk register refreshed
- Regulator-specific checklists complete

**Decision gate**

Advance when every in-scope control has ≥1 piece of evidence pinned, labelled, and accessible to the auditor.

### Stage 5 — Audit-day & retro

**Intent:** Show up, answer cleanly, close findings, log the lessons.

**Tasks**
- Communications plan: who says what, in what channel
- Run audit-day with RACI in hand
- Capture findings and close them inside the agreed window
- Status report to client steerco (no surprises)
- Lessons-learned retro inside the vendor team

**Outputs**
- Audit-day briefing pack
- Findings register
- Status report to steerco
- Lessons-learned doc

**Decision gate**

Engagement-close criterion: zero findings escalated to steerco AND all minor findings closed inside the agreed window.

## Common pitfalls

- Treating SAST/DAST as ticked boxes — auditors read the findings AND the disposition
- Ignoring AI-generated code; auditors increasingly ask about provenance
- Skipping a dry-run audit — the real audit is the worst place to discover gaps

## Quality checklist

- Could the auditor pull any control ID and find evidence in <2 minutes?
- Did we attribute every AI-generated PR to a human reviewer?
- Were findings discussed BEFORE steerco, not at?

## Related playbooks

- `compliance-grade-feature-delivery`
- `weekly-status-report`
- `production-cicd-pipeline`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `soc2-control-map-vendor-side` (blocks stage 1)
- `pci-dss-vendor-evidence-pack` (blocks stage 4)
- `hipaa-baa-vendor-checklist` (blocks stage 4)
- `banking-core-data-residency-rules` (blocks stage 4)
- `ai-coding-agent-compliance-guardrails` (blocks stage 3)
- `weekly-status-report` (blocks stage 5)
