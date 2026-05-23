# Regulatory Compliance 2026

## Summary

**One-sentence:** Cross-regime accessibility compliance map (ADA Title II, EU EAA, EN 301 549, Section 508, AODA) producing a per-region conformance plan + VPAT-ACR.

**One-paragraph:** 2026 brings overlapping accessibility regimes: ADA Title II (April 2026), EU EAA (June 2025 already-in-force), updated EN 301 549, Section 508 refresh signals, AODA enforcement uplifts. This methodology pins a per-region conformance plan + VPAT-ACR mapping, the documentation deliverables expected per regime, and the per-region exception clauses. Output is a regulatory compliance plan record validated against the schema.

**Ефективно для:**

- Avoids parallel-audit cost across overlapping regimes.
- Produces VPAT-ACR + EAA accessibility statement + AODA filing in one pass.
- Pins per-region exception clauses with rationale.
- Tracks per-region deadlines in one dashboard.

## Applies If (ALL must hold)

- Product ships to ≥1 region with active 2026 a11y rule.
- Procurement requires a VPAT-ACR or equivalent.
- Counsel has confirmed which regimes apply.

## Skip If (ANY kills it)

- Internal-only tool with no external users.
- Pre-product phase — return when audit baseline exists.
- Single-region narrow scope — use `ada-title-ii-compliance-2026` directly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Market regions in scope | list | legal |
| Product type | web / mobile / kiosk / hardware | product |
| Existing audit baselines | report list | audit |
| Procurement / contracting status | string | sales |

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
| `templates/vpat-acr-skeleton.md` | VPAT-ACR template (WCAG 2.2 AA). |
| `templates/accessibility-statement.txt` | EU EAA accessibility statement skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-regulatory-compliance-2026.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[ada-title-ii-compliance-2026]]
- [[wcag-22-compliance]]
- [[a11y-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
