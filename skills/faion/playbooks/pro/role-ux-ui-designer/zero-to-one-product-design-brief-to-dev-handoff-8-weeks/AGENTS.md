---
slug: zero-to-one-product-design-brief-to-dev-handoff-8-weeks
tier: pro
group: role-ux-ui-designer
persona: Product designer leading a greenfield product or major new module
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Greenfield product taken from problem brief to validated hi-fi prototype, design tokens wired, dev handoff package shipped, first build sprint supported.
content_id: 7cfcf2fa4f7b09d8
methodology_refs:
  - ai-design-assistant-patterns
  - generative-ui-design
  - accessibility-first-design
  - wcag-22-compliance
  - cross-platform-token-distribution
  - design-system-success-factors
  - semantic-tokens-and-modes
  - w3c-design-tokens-standard
  - design-tokens-fundamentals
  - prototyping
  - wireframing
  - jobs-to-be-done
  - problem-validation-2026
  - success-metrics-definition
  - value-proposition-design
  - ab-testing
  - card-sorting
  - design-critique
  - heuristic-evaluation
  - information-architecture
  - journey-mapping
  - usability-testing
---

# Zero-to-one product design: brief to dev handoff (8 weeks)

## Context

Product designer takes a greenfield product or new module across 8 weeks. Covers discovery, IA, wireframes, hi-fi, design tokens, a11y baseline, handoff package, and first-sprint support. Done when engineering is in build, the handoff package answers their questions, and at least one design QA pass has run.

## Outcome

Brief on a blank canvas -> validated hi-fi prototype + shipped dev handoff package + first sprint supported. Greenfield product taken from problem brief to validated hi-fi prototype, design tokens wired, dev handoff package shipped, first build sprint supported.

## Steps

1. **Problem framing.** Convert the brief into a problem worth solving. Tasks: Run JTBD interviews to validate the problem; Define success metrics for the product; Capture value proposition + non-goals.
2. **IA + journeys.** Map the spine before drawing pixels. Tasks: Card-sort to validate IA; Sketch primary user journeys; Identify flagship flows for hi-fi investment.
3. **Wireframes + heuristics.** Low-fi structure before high-fi polish. Tasks: Wireframe flagship flows; Self-run heuristic evaluation; Critique session with peers.
4. **Design tokens + a11y baseline.** Wire the visual system before hi-fi sprawl. Tasks: Pick design-token taxonomy (W3C-compliant); Define semantic tokens + light/dark modes; Bake a11y baseline (contrast, focus, semantics) into tokens.
5. **Hi-fi prototype.** Pixel-true prototype on flagship flows. Tasks: Build hi-fi screens with tokens applied; Wire interactive prototype; Use AI design-assist patterns to accelerate variants.
6. **Validate.** Real users, real tasks, real signal. Tasks: Run >=3 usability sessions; Run quick A/B on a contested decision; Capture severity-ranked findings.
7. **Handoff package.** Engineering can build without re-asking. Tasks: Compile spec: states, tokens, motion, a11y, edge cases; Annotate Figma <-> code mappings; Run a handoff review with engineering.
8. **First sprint support.** Stay close during the first build sprint. Tasks: Run a daily design-QA pass on PRs; Resolve open questions in <24h; Log learnings for next-cycle handoff template.

## Decision points

- **After Problem framing:** Advance only if the problem is articulated as a JTBD with measurable success.
- **After IA + journeys:** Advance when IA tests >=80% findability and flagship flows are agreed.
- **After Wireframes + heuristics:** Advance only when heuristic issues are fixed or accepted.
- **After Design tokens + a11y baseline:** Advance only when tokens build clean to code targets and a11y checklist passes.
- **After Hi-fi prototype:** Advance when prototype walks through flagship flows without dead ends.
- **After Validate:** Advance only when critical issues are fixed.
- **After Handoff package:** Advance only when engineering signs off on the package.
- **After First sprint support:** Done when sprint ends with >=80% design fidelity on flagship flows.

## References

- `faion/knowledge/geek/ux/ui-designer/ai-design-assistant-patterns`
- `faion/knowledge/geek/ux/ui-designer/generative-ui-design`
- `faion/knowledge/pro/ux/accessibility-specialist/accessibility-first-design`
- `faion/knowledge/pro/ux/accessibility-specialist/wcag-22-compliance`
- `faion/knowledge/pro/ux/ui-designer/cross-platform-token-distribution`
- `faion/knowledge/pro/ux/ui-designer/design-system-success-factors`
- `faion/knowledge/pro/ux/ui-designer/semantic-tokens-and-modes`
- `faion/knowledge/pro/ux/ui-designer/w3c-design-tokens-standard`
- `faion/knowledge/solo/ux/ui-designer/design-tokens-fundamentals`
- `faion/knowledge/solo/ux/ui-designer/prototyping`
- `faion/knowledge/solo/ux/ui-designer/wireframing`
- `faion/knowledge/solo/ux/user-researcher/jobs-to-be-done`
- `faion/knowledge/solo/ux/user-researcher/problem-validation-2026`
- `faion/knowledge/solo/ux/user-researcher/success-metrics-definition`
- `faion/knowledge/solo/ux/user-researcher/value-proposition-design`
- `faion/knowledge/solo/ux/ux-ui-designer/ab-testing`
- `faion/knowledge/solo/ux/ux-ui-designer/card-sorting`
- `faion/knowledge/solo/ux/ux-ui-designer/design-critique`
- `faion/knowledge/solo/ux/ux-ui-designer/heuristic-evaluation`
- `faion/knowledge/solo/ux/ux-ui-designer/information-architecture`
- `faion/knowledge/solo/ux/ux-ui-designer/journey-mapping`
- `faion/knowledge/solo/ux/ux-ui-designer/usability-testing`
- Related: `design-system-v1-to-v2-migration-12-weeks`, `user-research-sprint-discovery-to-recommendations-4-weeks`, `dev-handoff-doc-writing-per-feature`
