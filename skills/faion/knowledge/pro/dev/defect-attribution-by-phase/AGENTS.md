---
slug: defect-attribution-by-phase
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defect Attribution By Phase: codified dev practice that turns the recurring 'role-qa-engineer/Major release QA cycle: regression + smoke + UAT' decision into a repeatable, auditable artefact.
content_id: "15b58ea42d3f2ef1"
complexity: medium
produces: report
est_tokens: 4400
tags: [defect-attribution-by-phase, dev, pro]
---
# Defect Attribution By Phase

## Summary

**One-sentence:** Defect Attribution By Phase: codified dev practice that turns the recurring 'role-qa-engineer/Major release QA cycle: regression + smoke + UAT' decision into a repeatable, auditable artefact.

**One-paragraph:** Defect Attribution By Phase codifies a recurring "major release QA cycle" decision into a report artefact with a typed input contract, a JSON-schema-checked output, and a decision tree that routes between the operational variants. It exists because adjacent methodologies cover the surrounding topic without pinning the precise output shape this task produces. The artefact carries owner, version, last-reviewed date, and citations to every input used, so downstream agents and human reviewers can consume it without re-deriving the rationale.

**Ефективно для:**

- A team that already runs the parent activity but has no canonical report shape.
- Multi-agent workflows that need a contract-checked artefact instead of free-form prose.
- Pre-merge / pre-release gates where a missing field must block the pipeline.
- Audit scenarios — every decision must trace to a named input + a named owner.

## Applies If (ALL must hold)

- Task is an instance of "major release QA cycle" or a closely-adjacent variant.
- All Prerequisites artefacts exist or can be produced before the run starts.
- Output will be consumed by a downstream agent or human reviewer (not discarded).
- Tier `pro` or higher is unlocked for the operator (gating enforced by tier-manifest).

## Skip If (ANY kills it)

- A working team-owned artefact already covers this gap — replace, do not duplicate.
- The decision being made is a greenfield prototype with no production users.
- Regulatory or legal context overrides any in-methodology guidance — defer to counsel.
- Single-use throwaway task — overhead of the contract is not justified.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent context for the parent activity | Markdown / JSON | last 30 days of activity |
| Write access to artefact store | repo / wiki / decision log | platform owner |
| Named accountable owner | string (handle / email / role) | RACI / org chart |
| Baseline conventions | `CLAUDE.md` / `AGENTS.md` / `CONVENTIONS.md` | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/05-examples.xml` | essential | 1 worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_artefact` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/defect-attribution-by-phase.json` | JSON Schema for the report output contract |
| `templates/defect-attribution-by-phase.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-defect-attribution-by-phase.py` | Enforce Defect Attribution By Phase output contract against the JSON Schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream activity: `major release QA cycle`
- methodology family: `pro/dev/` (gap-p2 batch, F-059..F-066)

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions satisfied, stake level, downstream-consumer presence, regime overlay) to a concrete rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, defer to a peer, or skip outright.
