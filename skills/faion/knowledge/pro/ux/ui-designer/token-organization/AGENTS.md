# Token Organization

## Summary

A three-layer taxonomy — primitives (raw values) → semantic (purpose-based) → component (exceptions only) — plus a strict naming convention `{category}.{property}.{variant}.{state}`. Token names describe purpose, not appearance (`color.surface.primary`, not `blue-500`). Keep the set lean: add a new token only when an existing semantic token cannot cover the case; run a duplicate-value detector in CI.

## Why

Token bloat reduces discoverability and defeats the purpose of systematization. Symmetric naming produced by LLMs (`color.brand.primary.light.hover.disabled`) creates Cartesian explosions nobody uses. Names that describe appearance encode the current design decision into every consumer, making redesigns painful. A lean three-layer model with a naming linter prevents both failure modes.

## When To Use

- Bootstrapping a new design system's token taxonomy.
- Auditing an existing token set for bloat, naming inconsistency, or aliasing depth.
- Renaming tokens across a large repo without breaking references.
- Reviewing PRs that add new tokens to enforce the lean-first principle.

## When NOT To Use

- A 5-token brand palette for a single landing page — overhead exceeds benefit.
- Mid-rebrand with source of truth in flux — stabilize visuals before systematizing.
- Pure component library without theming — indirection adds no payoff.
- Brand-driven marketing assets that change weekly — naming churn kills ROI.

## Content

| File | What's inside |
|------|---------------|
| `content/01-taxonomy-and-naming.xml` | Three-layer model, naming convention rules, examples of good/bad names. |
| `content/02-gotchas.xml` | Agent pitfalls, duplicate detection, aliasing depth limit, rename codemod guidance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/token-name-lint.py` | Linter that flags names not matching convention and tokens with duplicate values. |

## Scripts

none
