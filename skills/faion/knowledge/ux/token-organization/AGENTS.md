# Token Organization: Three-Tier Hierarchy and Naming Convention

## Summary

**One-sentence:** Produces a design-token configuration with three-tier hierarchy (primitives / semantic / component) and a `{category}.{property}.{variant}.{state}` naming convention that makes tokens self-documenting and prevents bloat.

**One-paragraph:** Design-token systems collapse when names are ad-hoc and primitives leak into component code. This methodology enforces a strict three-tier hierarchy — primitives (raw values), semantic tokens (role-based aliases), component tokens (scoped overrides) — combined with a `{category}.{property}.{variant}.{state}` naming convention. Output is a config artefact + lint rules that reject component-layer references to primitives, enforce naming dots, and forbid raw hex/px in semantic or component layers. Output drives Style Dictionary or similar pipelines.

**Ефективно для:**

- Bootstrapping token system before component library scales past ~30 components.
- Refactoring legacy tokens to a three-tier hierarchy without a full rewrite.
- Lint rule: ban primitive references from component layer.
- Cross-platform token export with consistent naming convention.

## Applies If (ALL must hold)

- Component library has ≥30 components or expected to grow there.
- Multi-platform export targets exist (web + native).
- Team can adopt new naming convention without breaking shipped UI.

## Skip If (ANY kills it)

- Single-theme small library — overhead exceeds savings.
- Pure marketing pages outside the system.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing token list | JSON / CSS variables | design system team |
| Component inventory | list | FE engineering |
| Platform targets | list | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[design-tokens-fundamentals]] | upstream conceptual baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: three-tier-required, no-primitive-in-component, naming-convention-dots, no-raw-values-after-primitives, state-suffix-mandatory | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-tokens` | haiku | Mechanical classification. |
| `rename-codemod` | haiku | Mechanical renaming. |
| `fill-states` | sonnet | Light judgment on derived values. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens-three-tier.json` | Skeleton three-tier token config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-token-organization.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[semantic-tokens-and-modes]]
- [[design-tokens-fundamentals]]
- [[w3c-design-tokens-standard]]
- [[cross-platform-token-distribution]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by token role and assigns tier + naming pattern. Interactive-state branch enforces state-suffix coverage. Each leaf cites a rule from `01-core-rules.xml`.
