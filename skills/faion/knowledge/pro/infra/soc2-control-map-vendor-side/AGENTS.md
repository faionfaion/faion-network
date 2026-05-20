---
slug: soc2-control-map-vendor-side
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: SOC 2 Control Map (Vendor Side) — a one-page artefact mapping faion's existing SAST/DAST/supply-chain controls onto SOC 2 Trust Services Criteria so audit prep is incremental, not a panic project.
content_id: "a9cf41e340ebd727"
tags: [soc2-control-map-vendor-side, infra, pro]
---
# SOC 2 Control Map Vendor Side

## Summary

**One-sentence:** A one-page control map that lines up the vendor's existing technical controls (SAST, DAST, SBOM, secrets-rotation, access-review, backup) against the SOC 2 Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy) so audit prep becomes a gap analysis instead of a from-scratch lift.

**One-paragraph:** Faion has individual SAST/DAST/supply-chain knowledge but no control-map artefact that lines them up against SOC 2 trust services criteria from the vendor's side of the audit. Service vendors entering FinTech/HIPAA-adjacent procurement keep paying consultants to rebuild this same table. The methodology codifies (a) the five TSC sections, (b) which existing methodologies satisfy each control, (c) the evidence artefact the auditor will request, and (d) which gaps need new methodologies before audit.

## Applies If (ALL must hold)

- the vendor (your team / company) is the one being audited (Type 1 readiness or Type 2 evidence collection)
- the vendor already has at least some technical controls in place (SAST/DAST/secrets-management/access-control) — not greenfield
- there is a real audit driver (enterprise customer asking, procurement gate, regulated industry)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- you are the customer / buyer evaluating someone else's SOC 2 — use the customer-side vendor due-diligence checklist instead
- the vendor has no technical controls yet — start with `pro/infra/pci-dss-vendor-evidence-pack` foundations first
- a SOC 2 control map is already in place and current — extend rather than rebuild

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: TSC coverage, one-control-one-evidence, named owner per control, gap explicit, last_reviewed cadence |

## Related

- upstream playbook: `p4-outsource-specialist/FinTech / HIPAA compliance audit prep (4 weeks)`
- parent skill: `pro/infra/`
- related methodologies: `pro/infra/pci-dss-vendor-evidence-pack`, `pro/infra/secrets-rotation-end-to-end`, `pro/infra/cve-exception-template`
