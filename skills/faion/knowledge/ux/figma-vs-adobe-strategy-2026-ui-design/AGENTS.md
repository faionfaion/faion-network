# Figma vs Adobe Strategy 2026

## Summary

**One-sentence:** Produces a scored toolchain decision record selecting Figma, Adobe CC, or the Figma+Firefly hybrid for a product team, revisited every 6 months.

**One-paragraph:** Standardising on a single design platform is a multi-year cost commitment. Most 2026 product teams benefit from Figma (design + collaboration + handoff) + Firefly API (commercial-safe asset generation) — they are not mutually exclusive. This methodology produces a scored recommendation document based on team size, task types, budget, agent automation needs, and migration cost. Decision MUST be revisited every 6 months because both vendors ship major capability changes annually.

**Ефективно для:** head of design / VP product, що замикає toolchain рішення для команди ≥10 designers на 12–24 місяці.

## Applies If (ALL must hold)

- Toolchain audit for a product team deciding which design platform to standardise on.
- Annual or biennial procurement review with budget impact ≥$10k.
- Agent automation requirements are explicit (REST APIs, webhooks, batch generation).

## Skip If (ANY kills it)

- Team of one — pick by personal preference.
- Decision was made <6 months ago and nothing material changed.
- Lock-in cost (existing component libraries) is so high migration is impossible.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Team size + roles | JSON | ops |
| Task-type distribution (design / asset gen / handoff / prototyping) | JSON % | PM |
| Annual budget | USD | finance |
| Agent automation requirements | list | engineering |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[figma-ai-ecosystem]] | Figma agent boundary. |
| [[adobe-firefly-integration]] | Firefly API + commercial-safe imagery. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
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
| `templates/decision-record.json` | JSON skeleton: recommendation + scores + migration_cost + agent_endpoints + revisit + rationale. |
| `templates/score-rubric.md` | Five-axis scoring rubric definition. |
| `templates/_smoke-test.json` | Filled figma+firefly recommendation example. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-figma-vs-adobe-strategy-2026.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[figma-ai-ecosystem]]
- [[adobe-firefly-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the decision-record; mis-routing leads to producing the wrong artefact shape.
