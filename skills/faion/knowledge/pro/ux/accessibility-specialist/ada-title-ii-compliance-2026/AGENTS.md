---
slug: ada-title-ii-compliance-2026
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Operational checklist + audit-report shape for US ADA Title II Web/App Rule (DOJ 2024, effective 2026/2027) — WCAG 2.1 AA conformance for state/local gov digital services.
content_id: "565e43b8fde81718"
complexity: medium
produces: report
est_tokens: 4100
tags: [ada, title-ii, compliance, wcag-2-1, regulation]
---
# ADA Title II Compliance 2026

## Summary

**One-sentence:** Operational checklist + audit-report shape for US ADA Title II Web/App Rule (DOJ 2024, effective 2026/2027) — WCAG 2.1 AA conformance for state/local gov digital services.

**One-paragraph:** DOJ's 2024 rule under ADA Title II requires state and local governments (and their contractors) to conform their web content and mobile apps to WCAG 2.1 AA by April 2026 (large entities) and April 2027 (small entities). This methodology pins the operational scope (covered entities + content), the audit-report shape (per-service-area conformance + remediation plan), and the documented exception list (archived content, third-party content with conditions, individualised documents). Output is an ADA Title II conformance report validated against the schema.

**Ефективно для:**

- Mapping DOJ rule clauses to internal service-area inventory.
- Documenting exception list (archived / third-party / individualised) with rationale.
- Audit-grade conformance report ready for OCR / DOJ inquiry.
- Tracking 2026 vs 2027 deadlines per service area.

## Applies If (ALL must hold)

- Covered entity (state/local gov or contractor) preparing 2026/2027 deadlines.
- Existing WCAG 2.1 AA audit baseline available or scheduled.
- Counsel has confirmed ADA Title II applicability.

## Skip If (ANY kills it)

- Federal entity — Section 508 / Rehab Act applies, not Title II.
- Private commercial entity outside contractor scope — Title III may apply, this rule does not.
- Pre-compliance phase with no audit baseline — run `a11y-testing` first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Covered entity status | string (state/local gov or contractor) | legal |
| Service area inventory | list of digital services | product |
| WCAG 2.1 AA audit baseline | report | audit |
| Effective-date track | April 2026 vs April 2027 | size threshold |

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
| `templates/title-ii-conformance-report.md` | Markdown skeleton for the ADA Title II conformance report. |
| `templates/vpat-cell-generator.sh` | Helper to populate VPAT cells from conformance verdicts. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ada-title-ii-compliance-2026.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[regulatory-compliance-2026]]
- [[wcag-22-compliance]]
- [[a11y-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
