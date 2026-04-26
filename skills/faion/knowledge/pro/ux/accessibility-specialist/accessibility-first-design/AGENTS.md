# Accessibility-First Design

## Summary

Methodology for embedding accessibility requirements at the design stage — color contrast ratios, semantic structure, touch target sizing, motion controls, and focus management — before a single line of code is written. The core rule: 70-80% of accessibility defects are preventable at design time; retrofitting costs far more than getting it right first.

## Why

Accessibility defects found in development cost 10-100x more to fix than those caught in design. Designing with WCAG AA contrast ratios, semantic heading hierarchies, visible focus states, and 44×44px touch targets removes entire categories of defects. It also expands the addressable user base and satisfies legal compliance requirements in the EU, US (ADA), and UK.

## When To Use

- Starting a new UI design (web, mobile, or desktop)
- Adding a new component or page to an existing design system
- Conducting a design review before dev handoff
- Evaluating a Figma/Sketch file for accessibility gaps
- Writing design spec annotations for developers

## When NOT To Use

- Post-production audits where design files no longer exist — use code-level audit tools (axe, Lighthouse) instead
- Back-end or API work with no visual output
- Content writing (separate content accessibility concerns apply)

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-rules.xml` | Contrast ratios, touch targets, motion, focus states, semantic structure — concrete testable thresholds |
| `content/02-patterns.xml` | Common accessible patterns: forms, modal dialogs, skip links, buttons vs links, progressive enhancement |

## Templates

none
