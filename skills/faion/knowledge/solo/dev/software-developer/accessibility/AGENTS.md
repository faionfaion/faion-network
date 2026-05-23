---
slug: accessibility
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Generates a WCAG 2.2 AA accessibility report for one web screen — semantic-HTML score, ARIA pattern audit, keyboard-path trace, contrast table, and axe-core violation list.
content_id: "2000145e98e78395"
complexity: deep
produces: report
est_tokens: 4500
tags: [accessibility, wcag, a11y, axe-core, aria, keyboard, contrast]
---
# Accessibility (Web)

## Summary

**One-sentence:** Generates a WCAG 2.2 AA accessibility report for one web screen — semantic-HTML score, ARIA pattern audit, keyboard-path trace, contrast table, and axe-core violation list.

**One-paragraph:** WCAG 2.1/2.2 AA is the floor for any public-facing UI. This methodology runs five checks per screen: (1) semantic-HTML score (count of landmarks + headings vs div soup); (2) ARIA-first-rule audit (was ARIA added where semantic HTML would do?); (3) keyboard-only path trace (every interactive element reachable + visible focus ring); (4) contrast table (all foreground/background pairs ≥ 4.5:1 for text, ≥ 3:1 for UI); (5) axe-core violations. Output: an a11y-report with verdict per check + the must-fix list.

**Ефективно для:**

- Solo dev shipping a public-facing screen who needs a WCAG floor sign-off.
- Component-library author fixing once, benefiting everywhere.
- Pre-launch sweep before opening signup / paywall / checkout pages.
- Revenue-bearing flows where a keyboard-only user must complete the same path.

## Applies If (ALL must hold)

- Target is a rendered web screen (HTML reachable for static or DOM-instrumented analysis).
- Screen contains ≥1 interactive element (button, link, form control).
- Output will block release until verdict=pass.
- Tester has access to axe-core (or pa11y / Lighthouse a11y) in CI.

## Skip If (ANY kills it)

- Internal one-off script used by 1-2 people without assistive tech — defer.
- Throwaway prototype with no public launch path — defer.
- Pure-PDF artefact — use PDF/UA methodology instead.
- Screen has no interactive elements (pure static doc) — run reading-order checks only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Screen URL or rendered HTML snapshot | URL / .html | running app or storybook |
| Design tokens (colours) | JSON / CSS vars | design system |
| axe-core / pa11y CLI | binary | npm devDependency |
| Keyboard-path expected | ordered list of interactive elements | designer / PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[a11y-audit-per-screen-checklist]] | Per-screen checklist this report fills in. |
| [[design-tokens-basics]] | Source of contrast-correct colour pairs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules (semantic-first, ARIA-as-last-resort, keyboard-completeness, contrast-floor, axe-zero-critical) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for a11y-report + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: div-button, ARIA-on-everything, keyboard-trap, low-contrast-on-disabled | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (snapshot → semantic → ARIA → keyboard → contrast + axe) | 700 |
| `content/05-examples.xml` | essential | Worked example: pricing-page a11y-report with 2 failures repaired | 600 |
| `content/06-decision-tree.xml` | essential | Routes by axe-critical + contrast + keyboard verdicts | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `accessibility_semantic_audit` | sonnet | HTML structure judgement. |
| `accessibility_keyboard_trace` | sonnet | Path validation with focus-visible check. |
| `accessibility_axe_parse` | haiku | Mechanical parse of axe-core JSON output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the a11y-report artefact |
| `templates/a11y-report.md` | Markdown skeleton with the 5 sections + verdict header |
| `templates/contrast-pairs.json` | Example contrast-pair table for one screen |
| `templates/_smoke-test.json` | Minimum viable filled-in a11y-report for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-accessibility.py` | Validate a11y-report against schema + WCAG floors | Pre-commit; CI on each screen change |

## Related

- [[a11y-audit-per-screen-checklist]]
- [[design-tokens-basics]]
- [[browser-automation]]
- [[api-documentation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) axe-core critical count > 0 → fail, (b) keyboard-path incomplete → fail, (c) contrast violations on text → fail. Verdict pass requires all three clean. Every leaf references a rule in `01-core-rules.xml`.
