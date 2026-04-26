# Token Organization

## Summary

A three-tier hierarchy for design tokens — primitives (raw values), semantic tokens (role-based
aliases), and component tokens (scoped overrides) — combined with a `{category}.{property}.{variant}.{state}`
naming convention that makes tokens self-documenting and prevents bloat.

## Why

Token sets without hierarchy create two failure modes: engineers reference raw `blue-1` values
directly (bypassing theming), or component-level tokens explode as every developer adds
`button.primary.padding.left.hover.large`. A clear three-tier contract ensures primitives are
never referenced in components, semantic tokens carry intent, and component tokens are used only
when a component genuinely deviates from the semantic layer.

## When To Use

- Bootstrapping a new design system: establishing hierarchy before writing the first token.
- Auditing a sprawling token set (500+ tokens) to collapse aliases, kill duplicates, rename raw-value tokens.
- Onboarding a second platform (mobile after web) where existing names leak platform assumptions.
- Preparing for theming (light/dark/brand) — the semantic layer is mandatory before mode switching.

## When NOT To Use

- Single-page marketing site with 8 colors and 3 font sizes — CSS variables in one file suffice.
- Mid-flight design system rewrite when engineers are blocked — global rename without deprecation destroys velocity.
- Without buy-in from at least one designer and one engineer — naming conventions abandoned without authority.

## Content

| File | What's inside |
|------|---------------|
| `content/01-hierarchy.xml` | Three-tier model: primitives, semantic, component; naming convention; examples. |
| `content/02-rules.xml` | Rules for lean token sets, governance, tooling drift risks, agent-specific guidance. |

## Templates

none
