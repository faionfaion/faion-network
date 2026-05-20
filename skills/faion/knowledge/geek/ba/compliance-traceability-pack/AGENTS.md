---
slug: compliance-traceability-pack
tier: geek
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Compliance Traceability Pack: codified ba practice that turns the recurring 'role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability' decision into a repeatable, auditable artefact.
content_id: "c21fbff7109c3a53"
tags: [compliance-traceability-pack, ba, geek]
---
# Compliance Traceability Pack

## Summary

**One-sentence:** Compliance Traceability Pack: codified ba practice that turns the recurring 'role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability' decision into a repeatable, auditable artefact.

**One-paragraph:** Compliance Traceability Pack addresses the gap surfaced by 'role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability'. Regulated work (FinTech, HealthTech, GovTech) needs traceability extended to regulation clause IDs and audit-ready evidence export. pro/ba-core/requirements-traceability covers the generic matrix only. Compliance pack adds clause-versioning, evidence attachments, auditor walkthrough format. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/compliance-traceability-pack.json` | JSON schema for the Compliance Traceability Pack output contract |
| `templates/compliance-traceability-pack.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-compliance-traceability-pack.py` | Enforce Compliance Traceability Pack output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ba/business-analyst/`
- upstream playbook: `role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability`
- methodology family: `geek/ba/` (gap-p2 batch, F-059-063)
