---
slug: methodology-versioning-and-changelog
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Methodology Versioning And Changelog: codified sdlc-ai practice that turns the recurring 'p7-llm-agent-developer/Make faion a programmatic context source for an agent' decision into a repeatable, auditable artefact.
content_id: "d0133f505d46a69f"
tags: [methodology-versioning-and-changelog, sdlc-ai, pro]
---
# Methodology Versioning And Changelog

## Summary

**One-sentence:** Methodology Versioning And Changelog: codified sdlc-ai practice that turns the recurring 'p7-llm-agent-developer/Make faion a programmatic context source for an agent' decision into a repeatable, auditable artefact.

**One-paragraph:** Methodology Versioning And Changelog addresses the gap identified by the p7-llm-agent-developer/Make faion a programmatic context source for an agent playbook: Methodologies mutate. Agents cache. Without `version` + `content_hash` + changelog, every faion update silently invalidates downstream agent caches and breaks citation contracts. Need semver-ish convention (breaking/non-breaking) and a `faion changelog --since vX.Y` surface. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p7-llm-agent-developer/Make faion a programmatic context source for an agent OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p7-llm-agent-developer/Make faion a programmatic context source for an agent task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdlc-ai/sdd` | parent role skill — provides the operating context for this methodology |

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
| `templates/methodology-versioning-and-changelog.json` | JSON schema for the Methodology Versioning And Changelog output contract |
| `templates/methodology-versioning-and-changelog.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodology-versioning-and-changelog.py` | Enforce Methodology Versioning And Changelog output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/sdlc-ai/sdd/`
- upstream playbook: `p7-llm-agent-developer/Make faion a programmatic context source for an agent`
