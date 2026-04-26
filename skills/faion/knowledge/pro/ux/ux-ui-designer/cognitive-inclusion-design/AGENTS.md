# Cognitive Inclusion Design

## Summary

A design methodology that reduces cognitive load and adapts interfaces for users with ADHD,
autism spectrum, dyslexia, dyscalculia, anxiety, low literacy, and aging cognition — through
structural patterns (chunking, predictability, progress indicators) and optional settings
(focus mode, dyslexia font, reduced motion, extended time limits).

## Why

Traditional accessibility focuses on visual and motor impairments; cognitive disabilities are
larger in population but underserved by WCAG 2.2. Forms, tax workflows, healthcare portals,
and government services lose significant user populations to cognitive friction that automated
tools cannot detect. W3C COGA Task Force and WCAG 3.0 working draft add specific cognitive
guidelines that will become compliance targets; designing for them now prevents retrofitting.

## When To Use

- Designing for users with ADHD, autism, dyslexia, dyscalculia, anxiety, or aging cognition.
- Adding plain-language, focus mode, reduced-motion, or time-extension features to an existing product.
- Reviewing high-friction flows: multi-step forms, tax, healthcare, legal, government portals.
- Aligning with WCAG 3.0 cognitive guidelines or W3C COGA Task Force gap analysis.

## When NOT To Use

- Pure visual or motor accessibility — address via WCAG 2.2 AA + assistive-technology testing first.
- Single-action marketing surfaces (CTA + form) — cognitive customization is overkill.
- Highly regulated technical interfaces where literal labeling is already required by law.
- As a substitute for plain-language editing — cognitive design assumes the content is already plain.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Design patterns per cognitive profile: ADHD, autism, dyslexia, general cognitive load reduction. |
| `content/02-rules.xml` | Testable rules for each pattern; evidence caveats (e.g., dyslexia fonts); agent limitations. |

## Templates

none
