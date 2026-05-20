---
slug: tool-consolidation-decision-rule
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2237242926a3667e"
summary: "Tool Consolidation Decision Rule: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Vendor / tool consolidation review'."
tags: [tool-consolidation-decision-rule, pm, pro]
---
# Tool Consolidation Decision Rule

## Summary

**One-sentence:** Tool Consolidation Decision Rule: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Vendor / tool consolidation review'.

**One-paragraph:** Addresses the gap surfaced by 'p5-micro-agency-founder/Vendor / tool consolidation review': Cross-tool-migration covers mechanics but not the decision logic (cut / consolidate / replace / renegotiate). Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tool consolidation decision rule artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/Vendor / tool consolidation review' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tool consolidation decision rule artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p5-micro-agency-founder/Vendor / tool consolidation review' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Tool Consolidation Decision Rule |

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
| `templates/tool-consolidation-decision-rule.json` | JSON schema for the Tool Consolidation Decision Rule output contract |
| `templates/tool-consolidation-decision-rule.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-consolidation-decision-rule.py` | Enforce Tool Consolidation Decision Rule output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p5-micro-agency-founder/Vendor / tool consolidation review`
- pro/pm/p5-micro-agency-founder
