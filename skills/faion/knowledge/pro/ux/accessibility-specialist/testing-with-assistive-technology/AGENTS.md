---
slug: testing-with-assistive-technology
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Operational guide for AT testing rigs (screen readers, switch devices, voice-control, magnifiers) — environment setup, test matrix, finding capture.
content_id: "8b0dbdd7739af81f"
complexity: medium
produces: report
est_tokens: 4100
tags: [assistive-technology, screen-reader, voice-control, switch, magnifier, a11y]
---
# Testing with Assistive Technology

## Summary

**One-sentence:** Operational guide for AT testing rigs (screen readers, switch devices, voice-control, magnifiers) — environment setup, test matrix, finding capture.

**One-paragraph:** AT testing produces noisy results without a controlled rig. This methodology pins the AT environment (devices + AT versions), the per-flow test matrix (which AT exercises which flow), the finding capture format (env + AT + gesture + observation + WCAG SC), and the multi-AT cross-check. Output is an AT-finding record per test run validated against the schema.

**Ефективно для:**

- Multi-AT cross-check uncovers AT-specific defects.
- Recording each session produces audit-grade evidence.
- AT version pinning prevents drift between runs.
- Matrix tracks coverage per AT × flow.

## Applies If (ALL must hold)

- Audit requires AT-grade evidence across categories (SR + switch + voice + magnifier).
- AT rig fleet is available or budgeted.
- Recording is enabled per test run.

## Skip If (ANY kills it)

- Single-AT test — use `screen-reader-test-script-templates` if SR-only.
- Quick scanner pass — use `a11y-basics`.
- Unbudgeted AT environment — defer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AT rig inventory | device + AT + version list | QA |
| Test matrix | AT x flow | QA |
| Recording setup | OBS / Guidepup / WindowsAT | QA |
| WCAG SC mapping list | applicable SCs | audit |

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
| `templates/at-finding-record.json` | JSON skeleton for AT finding record. |
| `templates/at-test-case.txt` | Plaintext per-test case template. |
| `templates/guidepup-nvda-form-error.js` | Guidepup script template for NVDA form-error flow. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-with-assistive-technology.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[screen-reader-test-script-templates]]
- [[a11y-testing]]
- [[wcag-22-compliance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
