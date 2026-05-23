# VUI Accessibility and Inclusivity

## Summary

**One-sentence:** Accessibility + inclusivity spec for voice user interfaces: accent + dialect coverage, text alternates, confirmation cues, command discoverability.

**One-paragraph:** VUIs without accessibility produce exclusion at scale: under-trained accents, no text alternates, ambiguous confirmations, undiscoverable commands. This methodology pins five operational rules — accent + dialect training coverage, text-mode alternate for every voice flow, audible + visible confirmation cues, command discoverability via 'what can I say' help, and explicit consent + opt-out — and emits a VUI accessibility record validated against the schema.

**Ефективно для:**

- Accent coverage list pins fairness metric and recall floor.
- Text alternate keeps the flow accessible for deaf / non-speaking users.
- Audible + visible confirmation closes the trust loop.
- 'What can I say' help removes command-discoverability gap.

## Applies If (ALL must hold)

- Voice-only or voice-primary interface in production.
- User base spans multiple accents / dialects.
- Critical actions are voice-initiated.

## Skip If (ANY kills it)

- Optional voice supplement to a flat UI — primary remains the flat path.
- Single-language single-accent rig with no production users.
- Pure text dictation with no command grammar.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VUI inventory | list of voice flows | product |
| Speech-recog provider | Azure / Google / OpenAI / on-device | platform |
| Accent coverage list | language + dialect set | research |
| Confirmation policy | audible + visible spec | design |

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
| `templates/vui-record.json` | JSON skeleton for VUI accessibility record. |
| `templates/vui-grammar-help.md` | 'What can I say' help-text template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-accessibility-inclusivity.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[cognitive-inclusion-design]]
- [[a11y-basics]]
- [[screen-reader-test-script-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
