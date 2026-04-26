# Cognitive Inclusion Design

## Summary

Design patterns for cognitive accessibility covering ADHD, autism, dyslexia, anxiety, and learning disabilities — conditions affecting 15-20% of the population and underserved by traditional WCAG visual/motor focus. Key interventions: auto-save, progress indicators, predictable navigation, plain language, dyslexia-friendly typography, reduced-motion defaults, non-blaming error messages, and opt-in sensory-friendly modes.

## Why

WCAG 2.1 addressed cognitive accessibility only thinly; WCAG 2.2 added 3.2.6 Consistent Help, 3.3.7 Redundant Entry, and 3.3.8 Accessible Authentication as direct cognitive accommodations. The remaining gap is large: form abandonment, cognitive overload in dashboards, and anxiety from blame-language errors affect millions of users with ADHD, autism, dyslexia, or anxiety who do not appear in standard AT usage statistics. EU EAA now expects WCAG 2.2 AA plus applicable cognitive guidance for covered product categories.

## When To Use

- Designing or auditing forms, dashboards, learning tools, government services, or healthcare apps used by a non-expert public.
- Reducing form abandonment or support load on complex multi-step flows.
- Auditing copy, error messages, and microcopy for plain language and non-blaming tone.
- Working in EU (EAA) where WCAG 2.2 AA + cognitive guidance is expected.
- Accommodating neurodiverse employees in internal tools (HR platforms, intranets).

## When NOT To Use

- Pure visual/motor a11y audit — use `a11y-testing` and `wcag-22-compliance`.
- Performance-driven, expert-only tooling (CLI dashboards for SREs) — minimalism trumps scaffolding.
- Marketing landing pages where brand voice is intentionally playful — idioms acceptable in moderation.
- Game design where challenge is the point — apply selectively (settings menu, onboarding only).

## Content

| File | What's inside |
|------|---------------|
| `content/01-adhd-autism-dyslexia.xml` | Design patterns per condition: ADHD (auto-save, bookmarks, reduced motion), autism (predictability, literal language, sensory palette), dyslexia (font, spacing, alignment, text-to-speech). |
| `content/02-anxiety-and-checklists.xml` | Anxiety-friendly patterns (error prevention, reassuring feedback, exit points), learning disability support (scaffolding, multi-modal), implementation checklist, testing guidelines. |

## Templates

| File | Purpose |
|------|---------|
| `templates/readability-gate.py` | Python CI script failing the build if any UI string in locales/ has Flesch reading ease below 60. |
