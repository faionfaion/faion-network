---
slug: cross-team-estimation-normalisation
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Cross Team Estimation Normalisation: codified pm practice that turns the recurring 'role-project-manager/Multi-team coordination program (continuous, weekly checkpoints)' decision into a repeatable, auditable artefact.
content_id: "61b2b6d3689685c3"
tags: [cross-team-estimation-normalisation, pm, geek]
---
# Cross Team Estimation Normalisation

## Summary

**One-sentence:** Cross Team Estimation Normalisation: codified pm practice that turns the recurring 'role-project-manager/Multi-team coordination program (continuous, weekly checkpoints)' decision into a repeatable, auditable artefact.

**One-paragraph:** Cross Team Estimation Normalisation addresses the gap surfaced by 'role-project-manager/Multi-team coordination program (continuous, weekly checkpoints)'. Story points are not comparable across teams, yet program rollups constantly pretend they are. No methodology covers calibration sessions, throughput-based forecasting at program tier, or how to communicate the non-comparability honestly to a steering committee. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-project-manager/Multi-team coordination program (continuous, weekly checkpoints)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-project-manager/Multi-team coordination program (continuous, weekly checkpoints)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/cross-team-estimation-normalisation.json` | JSON schema for the Cross Team Estimation Normalisation output contract |
| `templates/cross-team-estimation-normalisation.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-team-estimation-normalisation.py` | Enforce Cross Team Estimation Normalisation output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/project-manager/`
- upstream playbook: `role-project-manager/Multi-team coordination program (continuous, weekly checkpoints)`
- methodology family: `geek/pm/` (gap-p2 batch, F-059-063)
