# Accessibility Annotation Pattern Library

## Summary

**One-sentence:** Produces an archetype-keyed library of a11y annotations + a dev-handoff doc resolving each annotation to role/name/state/keyboard/focus.

**One-paragraph:** "A11y is bolted-on" is the dominant pain point for designers handing off to dev. The library covers WCAG 2.2 AA + the 8 ARIA Authoring Practices Guide patterns most teams need: button, link, dialog, menu, tabs, combobox, form field, data table. Designer drops the annotation snippet on the Figma layer; dev reads off the snippet and implements verbatim. Outcome: annotations exist for every interactive component before any code is written. Primary output is an annotated design file + a dev-handoff doc with snippets resolved.

**Ефективно для:**

- Design system з reusable component library — анотації прив'язуються до archetype.
- Figma/Sketch handoff designer → dev: dev читає snippet verbatim.
- Продукт з WCAG 2.1 AA+ target — анотації покривають role/name/state/keyboard/focus.
- Solo designer без a11y-спеціаліста — бібліотека шаблонів замінює custom annotations.

## Applies If (ALL must hold)

- A design system or library of reusable components exists OR is being built.
- Design handoff goes from Figma/Sketch/XD/Penpot to dev or to another designer.
- The product targets WCAG 2.1 AA or higher.

## Skip If (ANY kills it)

- Pure marketing-page design (static, no interactive components) — annotations would be theatre.
- Code-first design (designer hands off only static visual) — the library has no consumer.
- AR/VR/spatial design — use `spatial-accessibility` (the patterns differ).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component archetype list | YAML list | design system inventory |
| Annotation schema | role/name/state/keyboard/focus | this methodology |
| WCAG 2.2 + ARIA APG refs | URL list | W3C |
| Calibration reference | fully-annotated example component | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wcag-22-compliance]] | SC mappings the annotations reference |
| [[design-system-success-factors]] | Library is part of the design system, not a one-off |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: archetype-keyed library, annotation-before-handoff, role/name/state minimum, focus-order explicit, keyboard map per interactive | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema per-component annotation + handoff-doc | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: drift, generic copy, wrong ARIA role, focus-order amnesia | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory → snippet → annotate → cross-screen focus → handoff doc | 800 |
| `content/05-examples.xml` | essential | Worked example: annotated combobox + dialog | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree: component archetype → snippet path | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `archetype-detection-per-component` | sonnet | Pattern match: this dropdown is a combobox, not a select. |
| `annotation-snippet-synthesis` | sonnet | Compose role+name+state+keyboard for the archetype. |
| `cross-screen-focus-order` | opus | Multi-screen tab-order reasoning across modals + drawers. |
| `handoff-doc-draft` | sonnet | Roll annotations into a dev-readable doc. |

## Templates

| File | Purpose |
|------|---------|
| `templates/annotation-snippet-library.md` | Full library: archetype → annotation template |
| `templates/handoff-doc.md` | Dev-handoff doc structure with annotation resolutions |
| `templates/figma-annotation-component.json` | Figma component spec for the annotation stamp |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-a11y-annotation-pattern-library.py` | Validate annotation library JSON against the schema | Before handoff / pre-commit |

## Related

- [[wcag-22-compliance]]
- [[design-system-success-factors]]
- [[accessibility-evaluation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
