---
slug: ai-pm-tool-evaluation-framework
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai Pm Tool Evaluation Framework: codified AI-in-SDLC practice that turns the recurring 'role-project-manager/Annual delivery-process maturity review' decision into a repeatable, auditable artefact.
content_id: "268e6be9d6cde58f"
tags: [ai-pm-tool-evaluation-framework, sdlc-ai, geek]
---
# Ai Pm Tool Evaluation Framework

## Summary

**One-sentence:** Ai Pm Tool Evaluation Framework: codified AI-in-SDLC practice that turns the recurring 'role-project-manager/Annual delivery-process maturity review' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai Pm Tool Evaluation Framework addresses the gap identified by the role-project-manager/Annual delivery-process maturity review playbook: ai-powered-pm-tools methodology is a survey, not a buyer's evaluation framework. PMs evaluating Linear-AI, Atlassian-Intelligence, Notion-AI, custom-LLM dashboards need a comparable scoring approach including risk of metric-gaming and people-dynamic blind spots. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-project-manager/Annual delivery-process maturity review OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-project-manager/Annual delivery-process maturity review task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/sdlc-ai-operator` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding | ~900 |
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
| `templates/ai-pm-tool-evaluation-framework.json` | JSON schema for the Ai Pm Tool Evaluation Framework output contract |
| `templates/ai-pm-tool-evaluation-framework.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pm-tool-evaluation-framework.py` | Enforce Ai Pm Tool Evaluation Framework output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/sdlc-ai/`
- upstream playbook: `role-project-manager/Annual delivery-process maturity review`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
