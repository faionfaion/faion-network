# Consistency and Standards

## Summary

Nielsen's Usability Heuristic #4: users should not have to wonder whether different words,
situations, or actions mean the same thing. Apply in five layers — internal, external, visual,
functional, and verbal — prioritizing industry conventions over product-specific ones. Enforce
through a design system and regular consistency audits that count distinct variations of each
UI element.

## Why

Inconsistency forces users to relearn the interface for each section, increasing cognitive load
and error rates. When the same action behaves differently in different parts of the product,
users lose confidence and slow down. A design system that governs components and terminology
eliminates drift and makes consistency measurable (count variation instances, not subjective
"feels consistent").

## When To Use

- When starting a design system from scratch — define the consistency hierarchy before building
  components.
- When auditing an existing product for usability issues — inconsistency is often the root cause
  of user confusion.
- When onboarding a new designer or developer — the design system is the reference.
- Before a brand refresh — audit all touchpoints against the new standards before shipping.

## When NOT To Use

- When intentional differentiation is the goal — e.g., a destructive action that must look
  visually distinct from standard actions. Purposeful inconsistency for contrast is valid.
- In early-stage exploration where standards have not been established — do not prematurely lock
  in patterns before validating with users.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Consistency types, hierarchy, implementation patterns for visual/functional/verbal layers |
| `content/02-antipatterns.xml` | Inconsistent terminology, layout reversals, design drift, platform violations with examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/consistency-audit.md` | Audit table: element, consistent Y/N, variations found, recommendation |
| `templates/button-component.md` | Design system component spec: variants, sizes, states, usage rules |
