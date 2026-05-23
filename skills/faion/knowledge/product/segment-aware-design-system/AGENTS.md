# Segment-Aware Design System

## Summary

**One-sentence:** Defines a design system where tokens, components, and copy variants are partitioned by user segment so a single codebase serves multiple audiences without forking.

**One-paragraph:** Defines a design system where tokens, components, and copy variants are partitioned by user segment so a single codebase serves multiple audiences without forking. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Один продукт для 2-5 сегментів (B2B/B2C, dev/exec) без форку кодбази.
- Token-level theming замість per-segment forked CSS.
- Component variants з explicit segment prop замість feature flags spaghetti.
- Copy variants централізовані в i18n + segment dimension, не у компонентах.

## Applies If (ALL must hold)

- ≥2 user segments з різним tone/density/copy при тому ж функціональному ядрі.
- Існує design system з токенами (Style Dictionary / Tokens Studio).
- Команда дизайну + фронту узгоджена на token-driven workflow.

## Skip If (ANY kills it)

- Один сегмент — segment dimension зайвий.
- Сегменти різняться функцією, а не UI — потрібен SaaS multi-tenancy, не дизайн-система.
- Прототип <100 користувачів — рано формалізувати сегменти.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| segment definitions | YAML list of segments with attributes | research / PM |
| token source | Style Dictionary JSON | design system |
| component inventory | Storybook stories list | frontend |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-assisted-persona-building]] | segments validated by research |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/segments.yaml` | Segment registry consumed by tokens + i18n |
| `templates/button-variants.stories.tsx` | Storybook stories showing Button across segments |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-segment-aware-design-system.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[vendor-evaluation-scorecard]]
- [[ai-assisted-persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Does the product serve ≥2 user segments with differing tone/copy on the same functional core?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
