---
slug: secret-rotation-drill-runbook
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Quarterly secret-rotation drill and breakglass runbook producing audit-grade evidence that satisfies SOC2 / ISO 27001 / PCI DSS rotation controls."
content_id: "d64136e54622f994"
tags: [secret-rotation-drill-runbook, infra, pro]
---
# Secret Rotation Drill Runbook

## Summary

**One-sentence:** A scheduled drill that exercises secret rotation end-to-end against a non-prod environment and emits a signed evidence pack auditors accept.

**One-paragraph:** Faion's `secrets-rotation-end-to-end` covers the backend mechanics (Vault, KMS, SOPS), but auditors don't ask "can you rotate?" — they ask "show me you have rotated, recently, with no production loss." This methodology fills that gap with a 6-rule drill protocol: pre-drill freeze window, simulated rotation against a clone environment, breakglass path verification (what if the rotation system itself is down), MTTR measurement, post-drill restoration check, and a signed evidence artefact (`drill-record.yaml` + timeline). Output is replayed quarterly and stored in the compliance evidence vault.

## Applies If (ALL must hold)

- you are in a regulated context (SOC2, ISO 27001, HIPAA, PCI DSS) OR have a customer demanding rotation evidence
- you have a non-production clone environment that mirrors prod's secret consumers
- a quarterly cadence is acceptable to your auditor
- tier == pro or higher

## Skip If (ANY kills it)

- a real rotation incident happened in the last 90 days with full evidence (the real event counts as the drill)
- the organisation has no production secrets (early prototype, no customers)
- compliance regime explicitly requires a different drill template (defer to legal)

## Prerequisites

- a current consumer registry (see `secret-consumer-discovery`)
- non-prod clone reachable from drill operator
- breakglass credentials stored OUT-of-band (paper safe, separate KMS, etc.)
- prior rotation runbook tested at least once for real

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/secrets-rotation-end-to-end` | mechanics this drill exercises |
| `pro/infra/secret-consumer-discovery` | input registry the drill uses |
| `pro/infra/dr-drill-script-template` | sibling pattern for disaster-recovery drills |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable drill rules + 1 evidence-pack example | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pre_drill_checklist` | haiku | template fill from runbook |
| `narrate_drill_timeline` | sonnet | bounded narration of operator actions |
| `assemble_evidence_pack` | sonnet | merge logs + screenshots + sign-offs |

## Related

- parent skill: `pro/infra/`
- `pro/infra/secrets-rotation-end-to-end`
- `pro/infra/secret-consumer-discovery`
- upstream playbook: `role-devops-engineer/Secrets-management migration: Vault / KMS / SOPS (4 weeks)`
