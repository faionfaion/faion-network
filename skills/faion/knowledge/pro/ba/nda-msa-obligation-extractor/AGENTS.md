---
slug: nda-msa-obligation-extractor
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Nda Msa Obligation Extractor: codified ba practice that turns the recurring 'p4-outsource-specialist/Foreign-Client Engagement Bootstrap' decision into a repeatable, auditable artefact.
content_id: "6c5835268fd73ead"
tags: [nda-msa-obligation-extractor, ba, pro]
---
# Nda Msa Obligation Extractor

## Summary

**One-sentence:** Nda Msa Obligation Extractor: codified ba practice that turns the recurring 'p4-outsource-specialist/Foreign-Client Engagement Bootstrap' decision into a repeatable, auditable artefact.

**One-paragraph:** Nda Msa Obligation Extractor addresses the gap identified by the p4-outsource-specialist/Foreign-Client Engagement Bootstrap playbook: Outsource specialists juggle 3–5 client contracts. Manually re-reading NDAs/MSAs is error-prone. A methodology + prompt pack that extracts obligations into a per-engagement checklist (data residency, IP assignment, sub-processor list, breach SLA) is missing. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p4-outsource-specialist/Foreign-Client Engagement Bootstrap OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p4-outsource-specialist/Foreign-Client Engagement Bootstrap task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

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
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/nda-msa-obligation-extractor.json` | JSON schema for the Nda Msa Obligation Extractor output contract |
| `templates/nda-msa-obligation-extractor.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nda-msa-obligation-extractor.py` | Enforce Nda Msa Obligation Extractor output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/business-analyst/`
- upstream playbook: `p4-outsource-specialist/Foreign-Client Engagement Bootstrap`
