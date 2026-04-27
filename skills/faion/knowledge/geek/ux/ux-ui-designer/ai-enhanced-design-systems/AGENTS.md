# AI-Enhanced Design Systems

## Summary

AI tooling for scaling design systems with a solid token foundation: automated documentation generation from component source, token violation scanning, Figma-to-code diff, and variant generation. AI amplifies what exists — it will not fix an inconsistent or poorly structured system.

## Why

Documentation drifts from implementation silently; token violations accumulate as codebase grows; Figma and code desync over weeks. Automated agents (weekly doc-gen jobs, per-PR token audits) catch these before they compound. The prerequisite is a canonical token format and consistent naming — without it, agents propagate inconsistency at scale.

## When To Use

- Design system has a solid token foundation and needs to scale component variants
- Documentation perpetually lags implementation — agent auto-generates from component source
- Design-to-code gap causes inconsistency — agent reconciles Figma tokens vs. CSS/Tailwind variables
- Team growing and consistency enforcement needs automation beyond manual design review
- Component adoption metrics are missing

## When NOT To Use

- Weak or inconsistent design system foundation — AI amplifies existing problems
- No structured token system exists — generated variations will be arbitrary
- Component naming is inconsistent across Figma and codebase — AI propagates inconsistency at scale
- Fewer than ~30 components — automation overhead exceeds manual maintenance cost
- No agreed single source of truth (Figma vs. code tokens)

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles-and-rules.xml` | AI amplification principle, prerequisites, token-first rules |
| `content/02-workflow-and-gotchas.xml` | Agent workflow, tool ecosystem, gotchas, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/token-violation-scanner.py` | Scan CSS/component files for hardcoded color and spacing values |
| `templates/prompt-doc-generator.txt` | Agent prompt: generate Storybook stories and MDX docs from component source |
| `templates/prompt-token-audit.txt` | Agent prompt: audit component library for token usage violations |
