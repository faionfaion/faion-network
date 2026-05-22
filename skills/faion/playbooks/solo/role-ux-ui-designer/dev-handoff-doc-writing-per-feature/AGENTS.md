---
slug: dev-handoff-doc-writing-per-feature
tier: solo
group: role-ux-ui-designer
persona: Designer writing the handoff spec engineering will build from
goal: plan-design
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Engineering can implement without re-asking; spec covers states, tokens, motion, a11y, edge cases, and Figma <-> code mapping."
content_id: 83120fca2a930b0a
methodology_refs:
  - ai-design-assistant-patterns
  - figma-ai-ecosystem
  - accessibility-first-design
  - wcag-22-compliance
  - semantic-tokens-and-modes
  - design-tokens-fundamentals
  - tailwind-design-tokens
  - mobile-ux
---

# Dev handoff doc writing (per feature)

## Context

Designer writes a handoff doc for one feature. Covers screen states, design tokens, motion, a11y annotations, edge cases, and Figma <-> code mappings. Done when engineering signs off and a build can start without follow-up questions.

## Outcome

Approved design -> handoff doc engineering can build from cold. Engineering can implement without re-asking; spec covers states, tokens, motion, a11y, edge cases, and Figma <-> code mapping.

## Steps

1. **States + structure.** Cover the screen lifecycle. Tasks: Document default, empty, loading, error, success states; Capture responsive + mobile behavior; Specify keyboard + focus order.
2. **Tokens + motion.** Visual + interactive system locked. Tasks: Map values to semantic tokens; Document motion durations + easing; Mark microinteractions explicitly.
3. **A11y annotations.** AT behavior is not guessed. Tasks: Document landmarks + heading order; Annotate ARIA labels + roles; Specify focus + announce behavior.
4. **Edge cases.** Anticipate what production will hit. Tasks: List edge content (long text, empty data, rate-limited); Specify offline + error recovery; Cover internationalization concerns.
5. **Code mapping + AI assist.** Map design to code so updates flow. Tasks: Annotate Figma <-> code (Code Connect or equivalent); Use AI design-assist patterns to generate variant tables; Validate the mapping with engineering.
6. **Sign-off.** Capture acceptance. Tasks: Walk engineering through the spec; Address questions inline; update doc; Get a written sign-off.

## Decision points

- **After States + structure:** Advance only when all states are documented.
- **After Tokens + motion:** Advance only when off-token values are zero.
- **After A11y annotations:** Advance only when AT behavior is concrete.
- **After Edge cases:** Advance only when each edge case has a documented response.
- **After Code mapping + AI assist:** Advance only when engineering confirms mapping is usable.
- **After Sign-off:** Done when engineering signs the doc.

## References

- `faion/knowledge/geek/ux/ui-designer/ai-design-assistant-patterns`
- `faion/knowledge/geek/ux/ui-designer/figma-ai-ecosystem`
- `faion/knowledge/pro/ux/accessibility-specialist/accessibility-first-design`
- `faion/knowledge/pro/ux/accessibility-specialist/wcag-22-compliance`
- `faion/knowledge/pro/ux/ui-designer/semantic-tokens-and-modes`
- `faion/knowledge/solo/ux/ui-designer/design-tokens-fundamentals`
- `faion/knowledge/solo/ux/ui-designer/tailwind-design-tokens`
- `faion/knowledge/solo/ux/ux-ui-designer/mobile-ux`
- Related: `zero-to-one-product-design-brief-to-dev-handoff-8-weeks`, `prototype-iteration-on-one-flow-13hr`
