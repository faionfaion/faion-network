# Consistency and Standards

## Summary

Nielsen Heuristic #4: users should not wonder whether different words, situations, or
actions mean the same thing. Follow platform and industry conventions. Apply to audit
visual, functional, and verbal consistency across a product, or to enforce design system
compliance in code and component specs.

## Why

Inconsistency forces users to relearn the interface for each section, raising error rates
and cognitive load. A consistent product lets learned behavior transfer across screens.
Design systems encode consistency as enforceable rules — without them, each page drifts
independently and audits become full-product exercises.

## When To Use

- Auditing a codebase or design for visual, functional, or verbal inconsistencies before a release
- Scanning UI copy across a product to surface synonym clusters and establish a canonical term glossary
- Reviewing a new component against an existing design system to flag deviations
- Enforcing design token usage in code (no hardcoded color or spacing values)

## When NOT To Use

- Intentional brand differentiation from convention — consistency auditing does not adjudicate that decision
- Brand-new products with no design system — nothing to be consistent against yet
- Single-screen tools where cross-screen consistency is irrelevant

## Content

| File | What's inside |
|------|---------------|
| `content/01-types.xml` | Five consistency types (internal, external, visual, functional, verbal); consistency hierarchy |
| `content/02-patterns.xml` | Implementation patterns: color/type/spacing standards, navigation behavior, canonical verb set |
| `content/03-examples.xml` | Good examples (iOS, Material Design); bad examples (inconsistent labels, reversed button order) |

## Templates

| File | Purpose |
|------|---------|
| `templates/consistency-audit.md` | Audit table: visual, functional, terminology, platform convention compliance |
| `templates/component-spec.md` | Design system component documentation: variants, sizes, states, usage rules |
| `templates/audit-colors.sh` | Bash script: scan a codebase for hardcoded hex colors outside design tokens |
| `templates/prompt-audit.txt` | LLM prompt for generating a terminology audit from a list of button labels |
