---
slug: soc2-evidence-generator-cli
tier: pro
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "febf45cf77981cf2"
summary: Faion CLI command + template that converts each merged PR into a SOC 2 evidence stub (control IDs, actor, diff hash, approval link) so audit prep becomes a query, not a manual hunt.
---
# Soc2 Evidence Generator Cli

## Summary

**One-sentence:** Pro-tier `faion soc2 evidence` subcommand + template pack that emits a per-PR evidence stub linked to the controls the change touches, generated automatically at merge time.

**One-paragraph:** Compliance-grade delivery (FinTech, HIPAA, PCI) demands per-change evidence trails. Hand-curation by the developer drifts the moment urgency rises. This methodology defines the `faion soc2 evidence` CLI flow: at PR merge, a webhook (or pre-merge hook) extracts actor, diff hash, control labels, reviewer approvals, CI run IDs, and writes a signed JSON stub into the evidence store. A Pro-tier template pack covers control-label vocabulary, stub schema, and signing policy. Anchored to "Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)" for outsource specialists who must demonstrate audit-readiness without slowing delivery.

## Applies If (ALL must hold)

- The product is in scope of SOC 2 (or equivalent: PCI-DSS, HIPAA, ISO 27001).
- PRs are the unit of change for production code and IaC.
- A control vocabulary exists (e.g., from `geek/infra/soc2-control-to-repo-artifact-map/`).
- The pipeline can sign artifacts (Sigstore, GPG, KMS) — unsigned stubs are useless at audit time.

## Skip If (ANY kills it)

- Trunk-based development with no PR boundary — adopt the "change-record" alternative, not this PR-keyed flow.
- No control vocabulary yet — the labels would be free-form and unusable.
- Pre-revenue / pre-customer-data — premature; revisit when the first compliance-bound customer signs.

## Prerequisites

- `faion-cli` ≥ the version that ships the `soc2` subcommand group.
- A merge-time hook or webhook that calls the CLI with the merge commit SHA.
- Signing keys provisioned for the CI environment.
- Append-only evidence store (S3+Object Lock, immutable bucket, or git ref under tag protection).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/AGENTS.md` | Parent group context |
| `geek/infra/soc2-control-to-repo-artifact-map/` | Source of the control-label vocabulary the stubs must use |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every stub generation enforces | ~950 |

## Related

- parent skill: `pro/sdd/`
- triggering activity: `p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)`
- upstream: `geek/infra/soc2-control-to-repo-artifact-map`
