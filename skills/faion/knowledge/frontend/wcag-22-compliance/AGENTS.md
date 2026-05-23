# WCAG 2.2 Compliance

## Summary

**One-sentence:** Generates a WCAG 2.2 AA conformance report for the 9 new success criteria (focus appearance, target size, drag, auth, redundant entry, consistent help) + automated CI gate.

**One-paragraph:** WCAG 2.2 was released October 2023 and is the baseline compliance standard by 2025-2026. It adds 9 new success criteria on top of 2.1: 2.4.11 Focus Not Obscured (Minimum), 2.4.12 Focus Not Obscured (Enhanced), 2.4.13 Focus Appearance, 2.5.7 Dragging Movements, 2.5.8 Target Size (Minimum), 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication (Minimum), 3.3.9 Accessible Authentication (Enhanced). This methodology emits a per-SC conformance report and a CI gate that flags regressions.

**Ефективно для:**

- Adding WCAG 2.2 AA as a CI quality gate.
- Auditing a product against the 9 new SC for a 2026 launch.
- Preparing VPAT 2.5 ACR conformance documentation.
- Coaching engineers on the focus + target size traps.

## Applies If (ALL must hold)

- Web product with public users, on production roadmap.
- Engineering has CI infrastructure that can run a11y checks.
- Author has access to component library + page templates.
- Product is meant to claim WCAG 2.2 AA conformance.

## Skip If (ANY kills it)

- Native-mobile-only app — defer to platform a11y APIs (UIAccessibility, Android a11y).
- Internal tooling with documented narrow user pool (rare; document the exception).
- Pre-production prototype with no users — defer.
- Trying to claim WCAG 3.0 conformance — 3.0 is still draft; keep 2.2 baseline.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component library | list of components with current a11y status | design system owner |
| Page inventory | list of pages to audit | PM |
| CI runner | axe-core / Pa11y / Lighthouse runner | DevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[w3c-design-tokens-standard]] | design tokens enforce contrast inputs |
| [[vpat-acr-template]] | downstream — feeds VPAT rows per SC |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `automated-checks` | haiku | Mechanical: run axe-core, parse output. |
| `manual-sc-review` | sonnet | Judgment on cognitive-burden SC. |
| `compute-overall` | haiku | Pure aggregation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wcag-22-report.md` | Markdown skeleton for the 9-SC report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wcag-22-compliance.py` | Validate wcag-22-compliance artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[w3c-design-tokens-standard]]
- [[vpat-acr-template]]

## Decision tree

See `content/06-decision-tree.xml`. Routes by scope, SC coverage completeness, and presence of failing SC. Conformance claim allowed only when all 9 are pass or not-applicable.
