# Figma AI Ecosystem Boundary

## Summary

**One-sentence:** Produces a decision record drawing the agent / human boundary across Figma's AI surfaces (Make, Draw, Sites, Image Tools) — REST + Webhooks for agents, UI-only for designers.

**One-paragraph:** Figma's AI suite (Make, Draw, Sites, Image Tools) has no agent API. Agents that pretend to drive these surfaces ship hallucinated workflows. The practical agent surfaces are REST API + Webhooks. Agent role: prompt preparation, validation, post-publish audits — never UI puppetry. This methodology produces a decision record that for each candidate workflow names whether it lives in UI (designer-driven), REST (agent-driven), or hybrid (agent prepares, designer commits).

**Ефективно для:** design ops lead, що ділить workflows на designer vs agent surfaces — і блокує hallucinated 'AI runs Figma Make' integrations.

## Applies If (ALL must hold)

- Designing a workflow that touches Figma Make, Draw, Sites, or Image Tools.
- Decision involves whether to automate vs keep manual.
- Stakeholders disagree on agent capability boundary.

## Skip If (ANY kills it)

- Workflow is purely REST-driven (no AI suite surface) — see [[ai-plugin-ecosystem]].
- Workflow is purely designer-driven (no automation candidate).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Workflow description (steps + actors) | markdown | ops |
| Surfaces involved | list (make/draw/sites/image) | ops |
| Frequency + scale | JSON | ops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-plugin-ecosystem]] | REST-based automation pattern. |
| [[ai-design-assistant-patterns]] | Assistant pattern catalogue. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-decision-record` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/decision-record.json` | JSON skeleton: workflow_id + per-step surface + actor + handoff. |
| `templates/surface-catalogue.md` | Reference list of Figma surfaces + agent-supported flag. |
| `templates/_smoke-test.json` | Filled hybrid-workflow decision record. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-figma-ai-ecosystem.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-plugin-ecosystem]]
- [[figma-vs-adobe-strategy-2026]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the decision-record; mis-routing leads to producing the wrong artefact shape.
