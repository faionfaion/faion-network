---
slug: threat-model-as-code
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c0a6e2b7c120cae8"
summary: "Threat Model As Code: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)'."
tags: [threat-model-as-code, dev, pro]
---
# Threat Model As Code

## Summary

**One-sentence:** Threat Model As Code: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)'.

**One-paragraph:** Addresses the gap surfaced by 'p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)': Faion has quality-attributes-analysis and reliability-architecture but no STRIDE/LINDDUN-as-code methodology that the AI agent can diff against PR diffs. Critical for regulated outsource work where threat-model drift = audit finding. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a threat model as code artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working threat model as code artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Threat Model As Code |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/threat-model-as-code.json` | JSON schema for the Threat Model As Code output contract |
| `templates/threat-model-as-code.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-threat-model-as-code.py` | Enforce Threat Model As Code output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)`
- pro/dev/p4-outsource-specialist
