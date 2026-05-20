---
slug: ai-sprint-planning-agent
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai Sprint Planning Agent: codified delivery-management practice that turns the recurring 'role-project-manager/AI-assisted sprint planning with capacity reality-check' decision into a repeatable, auditable artefact.
content_id: "8cb6d427feabd658"
tags: [ai-sprint-planning-agent, pm, geek]
---
# Ai Sprint Planning Agent

## Summary

**One-sentence:** Ai Sprint Planning Agent: codified delivery-management practice that turns the recurring 'role-project-manager/AI-assisted sprint planning with capacity reality-check' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai Sprint Planning Agent addresses the gap identified by the role-project-manager/AI-assisted sprint planning with capacity reality-check playbook: Existing agile-ceremonies-setup gives a template; nothing runs an agent that ingests velocity + calendar + carryover and proposes realistic capacity. Brief calls out 'AI Gantt without people-dynamics' — this is the antidote. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-project-manager/AI-assisted sprint planning with capacity reality-check OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-project-manager/AI-assisted sprint planning with capacity reality-check task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/ai-sprint-planning-agent.json` | JSON schema for the Ai Sprint Planning Agent output contract |
| `templates/ai-sprint-planning-agent.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-sprint-planning-agent.py` | Enforce Ai Sprint Planning Agent output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- upstream playbook: `role-project-manager/AI-assisted sprint planning with capacity reality-check`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
