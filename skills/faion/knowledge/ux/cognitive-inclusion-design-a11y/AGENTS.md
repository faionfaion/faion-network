# Cognitive Inclusion Design

## Summary

**One-sentence:** Design spec for cognitive accessibility: plain language, predictable navigation, error tolerance, recoverable actions, time-extension defaults.

**One-paragraph:** Cognitive disabilities cover the widest population (≈25% in some studies) and the smallest design coverage. This methodology pins five operational rules — plain language (Flesch / target reading level), predictable navigation patterns, error tolerance with auto-suggest, recoverable / undoable critical actions, and time-extension defaults — and emits a cognitive-inclusion design record per component validated against the schema.

**Ефективно для:**

- Plain-language rule cuts ambiguity defects ≥40%.
- Predictable navigation removes 'where am I' bounces.
- Recoverable actions enable confident exploration for users with executive-function differences.
- Time extension defaults remove pressure-induced fail-states.

## Applies If (ALL must hold)

- Public-facing form, content, or critical-action flow.
- Audience includes non-experts or includes neurodivergent users.
- Localisation targets multiple reading levels / languages.

## Skip If (ANY kills it)

- Internal expert tooling where jargon is required.
- Pure UI chrome with no language content.
- Performance / Operable issues — use `a11y-basics` instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component brief | Markdown | product |
| Target reading level | default Flesch ≥60 / Grade ≤8 | team policy |
| Critical actions list | list | product |
| Localisation matrix | languages in scope | i18n |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with sourced rationale + skip-this-methodology + run-the-checklist | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
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
| `templates/cognitive-spec.md` | Markdown skeleton for cognitive-inclusion design spec. |
| `templates/readability-gate.py` | Stdlib readability scorer. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cognitive-inclusion-design.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[accessibility-first-design]]
- [[wcag-22-compliance]]
- [[vui-accessibility-inclusivity]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
