---
slug: compliance-regime-review-matrix-soc2-hipaa-pci
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Compliance Regime Review Matrix Soc2 Hipaa Pci: codified dev practice that turns the recurring 'p4-outsource-specialist/Audit-grade code review for compliance client' decision into a repeatable, auditable artefact.
content_id: "b8df777a8132612e"
tags: [compliance-regime-review-matrix-soc2-hipaa-pci, dev, pro]
---
# Compliance Regime Review Matrix Soc2 Hipaa Pci

## Summary

**One-sentence:** Compliance Regime Review Matrix Soc2 Hipaa Pci: codified dev practice that turns the recurring 'p4-outsource-specialist/Audit-grade code review for compliance client' decision into a repeatable, auditable artefact.

**One-paragraph:** Compliance Regime Review Matrix Soc2 Hipaa Pci addresses the gap surfaced by 'p4-outsource-specialist/Audit-grade code review for compliance client'. Senior outsource devs ship into clients across multiple regimes per year. A per-regime quick-lookup matrix (what gets logged, what gets encrypted, what gets blocked) does not exist in faion. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/Audit-grade code review for compliance client' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p4-outsource-specialist/Audit-grade code review for compliance client' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/compliance-regime-review-matrix-soc2-hipaa-pci.json` | JSON schema for the Compliance Regime Review Matrix Soc2 Hipaa Pci output contract |
| `templates/compliance-regime-review-matrix-soc2-hipaa-pci.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-compliance-regime-review-matrix-soc2-hipaa-pci.py` | Enforce Compliance Regime Review Matrix Soc2 Hipaa Pci output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `p4-outsource-specialist/Audit-grade code review for compliance client`
- methodology family: `pro/dev/` (gap-p2 batch, F-059-063)
