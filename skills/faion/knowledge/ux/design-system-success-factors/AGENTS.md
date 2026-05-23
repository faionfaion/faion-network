# Design System Success Factors

## Summary

**One-sentence:** Produces a governance + adoption health report for a design system covering ownership, documentation freshness, contribution model, adoption metrics, and component coverage.

**One-paragraph:** Design systems fail more often from governance and adoption gaps than from technical debt: no single owner, documentation that drifts from source, components teams work around, and metrics absent. This methodology produces a quarterly health report tracking ownership, docs freshness, contribution model, per-team adoption %, and component coverage relative to the product surface.

**Ефективно для:**

- Quarterly health report для design system щоб уникнути silent rot.
- Adoption tracking — які team's working around the system.
- Ownership clarity: single accountable owner vs split-and-hope.
- Docs/code drift detection — лютий ворог design systems.

## Applies If (ALL must hold)

- An organisation operates a design system across >=2 teams.
- Components, tokens, and docs exist as identifiable artefacts.
- Adoption can be measured (component imports, design library usage).

## Skip If (ANY kills it)

- No formal design system yet — author one before measuring its health.
- Single-team / single-product context where governance overhead exceeds value.
- Greenfield day-1 system with no adoption history.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component inventory | Storybook/library export | design system |
| Per-team usage data | import analytics | monorepo / package registry |
| Docs source | MDX/Storybook stories | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[design-tokens-fundamentals]] | Token health is part of the system health |
| [[a11y-annotation-pattern-library]] | A11y is a design-system pillar |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ds-coverage.mjs` | Node script computing per-team adoption + system coverage from import graph |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-system-success-factors.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[design-tokens-fundamentals]]
- [[a11y-annotation-pattern-library]]
- [[cross-platform-token-distribution]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
