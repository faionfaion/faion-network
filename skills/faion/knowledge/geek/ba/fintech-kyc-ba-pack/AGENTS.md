---
slug: fintech-kyc-ba-pack
tier: geek
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a domain-specific BA pack for a FinTech KYC engagement: regulation-anchored requirements (FATF / AML / CDD), compliance traceability, identity-evidence inventory, and PEP / sanctions-screen control map."
content_id: "5422f753018c41be"
complexity: deep
produces: spec
est_tokens: 4500
tags: [ba, fintech, kyc, aml, compliance, geek]
---

# FinTech KYC BA Pack

## Summary

**One-sentence:** Produces a domain-specific BA pack for a FinTech KYC engagement: regulation-anchored requirements (FATF / AML / CDD), compliance traceability, identity-evidence inventory, and PEP / sanctions-screen control map.

**Ефективно для:** BAs running FinTech KYC discovery / requirements; compliance officers gating KYC implementations; PMs negotiating regulator-anchored scope.

**One-paragraph:** This methodology pins the recurring decision around "fintech-kyc-ba-pack" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Engagement is FinTech with KYC / CDD / EDD scope.
- Applicable regulation list available (FATF + local AMLA).
- Identity / sanctions / PEP screening in scope.
- Owner exists for the pack.

## Skip If (ANY kills it)

- Engagement is non-FinTech or has no KYC scope.
- KYC handled by a vendor with vendor-supplied artefacts (link out).
- Pilot with no production launch.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Applicable AML regulation list | Markdown | legal |
| Customer-segment risk matrix | Markdown / CSV | compliance |
| Identity evidence sources | CSV | operations |
| Sanctions + PEP screening provider | config | engineering |
| BA pack owner | handle / email | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[compliance-traceability-pack]]` | compliance-traceability pack pattern |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_requirement_map` | sonnet | Regulation-to-requirement mapping. |
| `synthesize_risk_matrix` | sonnet | Per-segment risk classification. |
| `escalate_jurisdiction_conflict` | opus | Cross-jurisdiction conflict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fintech-kyc-ba-pack.json` | JSON Schema for the FinTech KYC BA Pack output contract |
| `templates/fintech-kyc-ba-pack.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a fintech-kyc-ba-pack record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fintech-kyc-ba-pack.py` | Enforce the FinTech KYC BA Pack output contract | After subagent returns, before downstream consumer reads |

## Related

- [[compliance-traceability-pack]] — parent pack methodology.
- [[healthtech-fhir-ba-pack]] — sibling domain pack.
- [[govtech-foia-ba-pack]] — sibling domain pack.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
