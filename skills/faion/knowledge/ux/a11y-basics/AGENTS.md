# Accessibility Basics

## Summary

**One-sentence:** Entry-level accessibility layer for web products: WCAG POUR principles, conformance levels, four evaluation types, and a 5-minute pre-PR quick-check protocol.

**One-paragraph:** Products without an accessibility baseline exclude users with disabilities, create legal exposure (ADA, Section 508, AODA, EAA), and accumulate expensive late-stage fixes. This methodology pins the POUR framing (Perceivable / Operable / Understandable / Robust), the WCAG A / AA / AAA bands, the four evaluation types (automated ≈30%, manual ≈50%, AT, user testing), and a 5-minute pre-PR quick-check covering tab navigation, 200% zoom, alt-text on one image, label on one input, and an axe DevTools run. Output is a quick-check report validated against the schema.

**Ефективно для:**

- Pre-PR quick-check that takes ≤5 minutes per page.
- Onboarding the team to a shared a11y vocabulary (POUR + A/AA/AAA).
- Wiring axe-core into CI for the automated 30% baseline.
- Tagging the 70% gap so QA / AT testing can be scoped.

## Applies If (ALL must hold)

- Onboarding a new team or codebase to accessibility for the first time.
- Pre-launch sanity sweep on a small feature where a full WCAG 2.2 audit is overkill.
- Wiring CI to catch the obvious ~30% issues automated tools find.
- Educating a new agent or developer before they touch UI code.

## Skip If (ANY kills it)

- Final compliance sign-off — use `wcag-22-compliance` and `regulatory-compliance-2026`.
- Real AT testing flows (NVDA / VoiceOver / TalkBack) — use `testing-with-assistive-technology`.
- Procurement / VPAT-ACR generation — use `regulatory-compliance-2026`.
- XR / spatial experiences — use `vr-design-patterns`, `ar-design-patterns`, `spatial-accessibility`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff / page URL | URL or unified diff | git / browser |
| WCAG version | string (target = 2.2 AA) | team policy |
| Axe DevTools or axe-core | browser ext / npm pkg | deque.com |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pour-as-frame, pin-wcag-version-and-level, automated-only-catches-30pct, five-minute-quick-check, placeholder-is-not-a-label | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the quick-check report + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: scanner-only-audit, placeholder-as-label, aria-label-on-native, mixed-wcag-levels | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
| `content/05-examples.xml` | essential | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (preconditions, severity, modality) to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-inputs` | haiku | Mechanical scrape from inputs. |
| `apply-rules` | sonnet | Per-rule judgement on inputs. |
| `synthesise-artefact` | sonnet | Aggregates rule outcomes into the final artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/quick-check-report.md` | Markdown skeleton for a11y quick-check report. |
| `templates/a11y-ci.js` | axe-core CI wiring snippet. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-a11y-basics.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[wcag-22-compliance]]
- [[a11y-testing]]
- [[testing-with-assistive-technology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
