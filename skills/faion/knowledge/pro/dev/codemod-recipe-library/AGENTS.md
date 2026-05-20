---
slug: codemod-recipe-library
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Codemod Recipe Library: codified dev practice that turns the recurring 'role-software-developer/Survive a Major Framework Upgrade Without a Big-Bang Branch' decision into a repeatable, auditable artefact.
content_id: "5bcf8f614d1debca"
tags: [codemod-recipe-library, dev, pro]
---
# Codemod Recipe Library

## Summary

**One-sentence:** Codemod Recipe Library: codified dev practice that turns the recurring 'role-software-developer/Survive a Major Framework Upgrade Without a Big-Bang Branch' decision into a repeatable, auditable artefact.

**One-paragraph:** Codemod Recipe Library addresses the gap surfaced by 'role-software-developer/Survive a Major Framework Upgrade Without a Big-Bang Branch'. jscodeshift / ast-grep / Bowler / libcst recipes for common migrations. No methodology covers writing and validating codemods. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-software-developer/Survive a Major Framework Upgrade Without a Big-Bang Branch' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-software-developer/Survive a Major Framework Upgrade Without a Big-Bang Branch' task (last 30 days of activity)
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
| `templates/codemod-recipe-library.json` | JSON schema for the Codemod Recipe Library output contract |
| `templates/codemod-recipe-library.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-codemod-recipe-library.py` | Enforce Codemod Recipe Library output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `role-software-developer/Survive a Major Framework Upgrade Without a Big-Bang Branch`
- methodology family: `pro/dev/` (gap-p2 batch, F-059-063)
