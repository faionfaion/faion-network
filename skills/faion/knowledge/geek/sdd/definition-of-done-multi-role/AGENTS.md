---
slug: definition-of-done-multi-role
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Definition Of Done Multi Role: codified sdd practice that turns the recurring 'p6-product-dev-team/RFC → Production: feature delivery (3-6 weeks)' decision into a repeatable, auditable artefact.
content_id: "23ec851694d86bbc"
tags: [definition-of-done-multi-role, sdd, geek]
---
# Definition Of Done Multi Role

## Summary

**One-sentence:** Definition Of Done Multi Role: codified sdd practice that turns the recurring 'p6-product-dev-team/RFC → Production: feature delivery (3-6 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Definition Of Done Multi Role addresses the gap surfaced by 'p6-product-dev-team/RFC → Production: feature delivery (3-6 weeks)'. SDD docs imply DoD but never spell it out across roles. Product team needs a per-role DoD checklist (PM done, BA done, Dev done, QA done, DevOps done, PdM done) tied to feature lifecycle. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/RFC → Production: feature delivery (3-6 weeks)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p6-product-dev-team/RFC → Production: feature delivery (3-6 weeks)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdd/sdd` | parent role skill — provides the operating context for this methodology |

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
| `templates/definition-of-done-multi-role.json` | JSON schema for the Definition Of Done Multi Role output contract |
| `templates/definition-of-done-multi-role.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-definition-of-done-multi-role.py` | Enforce Definition Of Done Multi Role output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/sdd/sdd/`
- upstream playbook: `p6-product-dev-team/RFC → Production: feature delivery (3-6 weeks)`
- methodology family: `geek/sdd/` (gap-p2 batch, F-059-063)
