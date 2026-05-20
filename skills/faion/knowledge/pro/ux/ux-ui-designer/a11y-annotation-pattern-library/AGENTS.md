---
slug: a11y-annotation-pattern-library
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c2a6ca187ea325f6"
summary: A reusable library of accessibility annotations keyed to component archetypes so a11y is specified during design, not bolted on after.
tags: [a11y, design-handoff, annotations, figma, component-library, aria]
---
# Accessibility Annotation Pattern Library

## Summary

**One-sentence:** A reusable library of accessibility annotations keyed to component archetypes so a11y is specified during design, not bolted on after.

**One-paragraph:** "A11y is bolted-on" is the dominant pain point for UX designers handing off to dev. Mechanism: a library of pre-written annotation snippets — role / name / state / focus order / keyboard map — keyed to common component archetypes (button, link, dialog, menu, tabs, combobox, form field, data table). Designer drops the annotation onto the Figma layer; dev reads off the snippet and implements verbatim. The library covers WCAG 2.2 AA + the 8 ARIA Authoring Practices Guide patterns most teams need. Outcome: a11y annotations exist for every interactive component before any code is written. Primary output: an annotated design file + a dev-handoff doc with the annotation snippets resolved.

## Applies If (ALL must hold)

- a design system or library of reusable components exists OR is being built
- design handoff goes from Figma / Sketch / XD / Penpot to dev (or to another designer for spec extension)
- the product targets WCAG 2.1 AA or higher
- designer is responsible for specifying interaction (not just visual)
- there is a dev partner who will read the annotations

## Skip If (ANY kills it)

- pure marketing-page design (static, no interactive components) — annotations would be theater
- code-first design (designer hands off only static visual) — the library has no consumer
- post-launch retrofit on legacy product — use `wcag-22-compliance` + `wcag-severity-rubric` instead
- AR/VR / spatial design — use `spatial-accessibility` (the patterns differ)
- product team has dedicated a11y specialist authoring custom annotations per screen — overkill for solo designer

## Prerequisites (must be true before starting)

- a list of component archetypes the design uses (button, link, dialog, etc.)
- a design tool that supports annotations or comments anchored to layers
- WCAG 2.2 + ARIA APG references available
- at least one example component fully annotated as a calibration reference
- agreed annotation schema (role / name / state / keyboard / focus)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/accessibility-specialist/wcag-22-compliance` | Source of SC mappings the annotations reference |
| `pro/ux/ux-ui-designer/design-system-success-factors` | Annotation library is part of the design system, not a one-off |
| `pro/dev/software-developer/wcag-severity-rubric` | Dev triage path when annotations are missed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: archetype-keyed library, annotation-before-handoff, role/name/state minimum, focus-order explicit, keyboard map per interactive | ~900 |
| `content/02-output-contract.xml` | essential | Per-component annotation schema, handoff-doc schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (drift, generic copy, missing states, wrong ARIA role, focus-order amnesia, library rot) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `archetype_detection_per_component` | sonnet | Pattern match: this dropdown is a "combobox", not a "select" |
| `annotation_snippet_synthesis` | sonnet | Compose role+name+state+keyboard for the archetype |
| `cross_screen_focus_order_synthesis` | opus | Multi-screen tab-order reasoning across modals + drawers |
| `handoff_doc_first_draft` | sonnet | Roll annotations into a dev-readable doc |

## Templates

| File | Purpose |
|------|---------|
| `templates/annotation-snippet-library.md` | The full library: archetype → annotation template |
| `templates/handoff-doc.md` | Dev-handoff doc structure with annotation resolutions |
| `templates/figma-annotation-component.json` | Figma component spec for the annotation stamp |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/audit-design-for-missing-annotations.py` | Scan design file for interactive layers without annotations | Before handoff |
| `scripts/lint-annotation-snippet.py` | Verify snippet has role + name + state + keyboard fields populated | After authoring |

## Related

- parent skill: `pro/ux/ux-ui-designer/`
- peer methodologies: `wcag-22-compliance`, `design-system-success-factors`, `accessibility-evaluation`
- external: [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) · [Stark - a11y annotation kit](https://www.getstark.co/) · [Figma A11y Annotation Kit](https://www.figma.com/community/file/953682768192596304)
