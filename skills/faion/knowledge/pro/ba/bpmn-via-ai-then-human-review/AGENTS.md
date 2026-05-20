---
slug: bpmn-via-ai-then-human-review
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Bpmn Via Ai Then Human Review: codified business-analysis practice that turns the recurring 'role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability' decision into a repeatable, auditable artefact.
content_id: "c6e20a5eaef14701"
tags: [bpmn-via-ai-then-human-review, ba, pro]
---
# Bpmn Via Ai Then Human Review

## Summary

**One-sentence:** Bpmn Via Ai Then Human Review: codified business-analysis practice that turns the recurring 'role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability' decision into a repeatable, auditable artefact.

**One-paragraph:** Bpmn Via Ai Then Human Review addresses the gap identified by the role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability playbook: pro/ba-modeling/business-process-analysis covers BPMN modeling assuming a human modeler. The gap is the AI-first workflow: transcript / SOP doc → AI-generated draft BPMN → BA review for swimlane correctness, gateway logic, message events. This is the dominant modern workflow and there is no methodology. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding, r5-acceptance-criteria | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/bpmn-via-ai-then-human-review.json` | JSON schema for the Bpmn Via Ai Then Human Review output contract |
| `templates/bpmn-via-ai-then-human-review.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bpmn-via-ai-then-human-review.py` | Enforce Bpmn Via Ai Then Human Review output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/FinTech KYC engagement: regulatory-anchored requirements with compliance traceability`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
