# Design Tokens

## Summary

**One-sentence:** Author primitive → semantic → component design tokens as one JSON source of truth that emits per-platform outputs via Style Dictionary.

**One-paragraph:** Design tokens are the atomic values of a design system stored as structured data with a three-tier hierarchy: primitive (raw values: colors, spacing scales), semantic (purpose-based aliases: text/primary, surface/raised), component (usage-specific: button/text/hover). One JSON source emits per-platform outputs (CSS vars, JS constants, iOS Swift, Android XML) via Style Dictionary. Output is the token spec + build pipeline that designers and engineers consume from one source.

**Ефективно для:**

- Building or extending a design system across web + mobile.
- Introducing dark mode or white-label theming.
- Bridging Figma to code so design and engineering stay in sync.
- Standardising brand across multiple apps in a monorepo.

## Applies If (ALL must hold)

- Design system spans more than one product or platform.
- Theming (dark mode, white-label, brand variants) is on the roadmap.
- Designers work in Figma and engineering needs the values in code.
- Token churn is bounded (not hourly iteration on a prototype).

## Skip If (ANY kills it)

- Single one-off marketing page — overhead beats payoff.
- Apps fully delegating to a UI library (Material, Mantine) with no re-skinning.
- Prototype work where designers iterate hourly — token churn outpaces pipeline cost.
- Pure server-rendered emails using external template SaaS that owns tokens.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Figma file with frames + variables (or equivalent design source) | Figma URL | design lead |
| Target platforms list (web, iOS, Android, email) | list | tech-lead |
| Style Dictionary or similar emitter chosen + version pinned | config | platform |
| Brand identity decisions (primary, neutral, semantic colour roles) | ADR | design lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tailwind-architecture]] | Token output often consumed by Tailwind config. |
| [[ui-component-library]] | Components consume the component-tier tokens. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (3-tier hierarchy, one source of truth, semantic aliases, no hex in components, per-platform emission, Figma parity) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for token spec artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: primitives → semantics → components → emit → audit | 800 |
| `content/05-examples.xml` | essential | Worked example: dark-mode-ready button tokens | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primitive_extraction` | sonnet | Mechanical: pull values from Figma variables. |
| `semantic_mapping` | opus | Naming semantic aliases requires deep design synthesis. |
| `component_token_authoring` | sonnet | Component-tier names follow predictable conventions. |
| `emitter_pipeline` | sonnet | Wire Style Dictionary build to CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/primitive.json` | Primitive-tier raw values (colors, spacing, type scale) |
| `templates/semantic.json` | Semantic-tier aliases referencing primitives |
| `templates/build-tokens.mjs` | Style Dictionary build pipeline |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-tokens.py` | Validate the token spec artefact metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[tailwind-architecture]]
- [[ui-component-library]]
- [[frontend-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps platform count, theming need, and design-source authority to a rule from `01-core-rules.xml`, telling the agent whether to invoke the full token pipeline or skip when overhead exceeds value. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
