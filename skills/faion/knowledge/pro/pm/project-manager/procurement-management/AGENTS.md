---
slug: procurement-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Six-step framework for engaging external vendors: make-or-buy, SOW, contract-type, weighted evaluation, negotiation, ongoing management — with mandatory clause checklist before signing.
content_id: "ab9e4524d6787be5"
complexity: medium
produces: spec
est_tokens: 4700
tags: [procurement, vendor-management, contracts, sow, vendor-evaluation]
---
# Procurement Management Framework

## Summary

**One-sentence:** Six-step framework for engaging external vendors: make-or-buy, SOW, contract-type, weighted evaluation, negotiation, ongoing management — with mandatory clause checklist before signing.

**One-paragraph:** Six-step framework for engaging external vendors. Steps: make-or-buy decision (always include build-internal/do-nothing as baseline), draft SOW with explicit acceptance criteria, select contract type (Fixed Price / T&M / Cost Plus) matched to scope clarity, run weighted vendor scoring with sensitivity analysis, negotiate, and operate ongoing vendor management. Every contract passes a clause checklist (IP, sub-processor, DPA, termination, audit, SLA, indemnity, warranty) before signing. Output: signed SOW + vendor matrix + clause-status table.

**Ефективно для:**

- Engaging external vendor for a defined feature, not staff augmentation
- Need a Fixed-Price / T&M / Cost-Plus decision before RFP
- Drafting SOW that must hold up against vendor reinterpretation
- Weighted scoring across 3+ candidate vendors

## Applies If (ALL must hold)

- Defining a make-or-buy framework before engaging external vendors
- Drafting SOW, Master Services Agreement (MSA), or Data Processing Addendum (DPA) skeletons
- Running RFI / RFP / RFQ process: vendor list, evaluation matrix, weighted scoring
- Selecting contract type for a defined scope and risk profile
- Vendor risk and security review (SOC 2, ISO 27001, GDPR DPA) intake

## Skip If (ANY kills it)

- Spot purchases under PO threshold (e.g. under $5K) where formal procurement is overhead
- Highly regulated industries with established central procurement and legal teams — defer to org policy
- SaaS tools the engineering team can self-onboard with monthly billing (security review still needed, but not a full RFP)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | product / engineering |
| Acceptance criteria | Markdown | business analyst |
| Vendor longlist | CSV | procurement / desk research |
| Scoring rubric | YAML | team consensus before proposals arrive |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scope-management]] | SOW acceptance criteria flow from scope baseline |
| [[risk-management]] | Vendor risks feed the project risk register |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: baseline-included, contract-type-matches-scope, pre-published-weights, clause-checklist-pass, milestone-gated-payments | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-sow` | sonnet | Template fill from spec + AC; bounded judgment |
| `score-vendors` | haiku | Mechanical weight × score arithmetic in script |
| `clause-audit` | sonnet | Pattern-match against checklist; flag missing/weak |

## Templates

| File | Purpose |
|------|---------|
| `templates/sow.md` | Statement of Work template with acceptance criteria and clause checklist |
| `templates/vendor-matrix.md` | Weighted evaluation matrix with scoring scale and sensitivity check |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/vendor_score.py` | Weighted vendor scoring with sensitivity analysis | On every vendor scoring run; sensitivity check pre-decision |

## Related

- parent skill: `pro/pm/project-manager/`
- [[scope-management]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
