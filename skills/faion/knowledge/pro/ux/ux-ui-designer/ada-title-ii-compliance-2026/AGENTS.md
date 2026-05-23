---
slug: ada-title-ii-compliance-2026
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Conformance report for US state/local government digital services on the WCAG 2.1 AA target under DOJ's April-2024 final rule (Apr 2026 / Apr 2027 deadlines by population).
content_id: "565e43b8fde81718"
complexity: deep
produces: report
est_tokens: 4500
tags: [compliance, ada, government, wcag, legal]
---
# ADA Title II Compliance 2026

## Summary

**One-sentence:** Conformance report for US state/local government digital services on the WCAG 2.1 AA target under DOJ's April-2024 final rule (Apr 2026 / Apr 2027 deadlines by population).

**One-paragraph:** DOJ's April 2024 final rule under ADA Title II requires state and local government digital services to conform to WCAG 2.1 AA. Compliance dates: April 24, 2026 (jurisdictions >=50k population), April 26, 2027 (under 50k). Produces a conformance report tying every public-facing surface to WCAG SCs, identifying the population-bucket deadline, and exposing remediation gaps. Compliance is verifiable evidence, not a self-attestation.

**Ефективно для:**

- State/local government digital service з public-facing UI — обов'язково за DOJ rule.
- Procurement / VPAT для гос. контрактів — потрібен conformance report.
- Legal/risk team вимагає evidence перед deadline (Apr 2026 чи 2027).
- Federal grant funding conditioned on Title II compliance.

## Applies If (ALL must hold)

- Organisation is a US state/local government, district, or public entity bound by ADA Title II.
- Digital service is public-facing (citizen-served).
- WCAG 2.1 AA is the explicit target (DOJ rule).

## Skip If (ANY kills it)

- Private entity — Title II does not apply (Title III may; use a different methodology).
- Federal agency — Section 508 applies, not Title II.
- Internal-only employee tools — Title II scope is public-facing services.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service inventory | URL list | agency CIO |
| Population bucket | >=50k or <50k | US Census |
| WCAG 2.1 AA audit | audit-report.json | accessibility-evaluation |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[accessibility-evaluation]] | Source of per-SC findings the conformance report cites |
| [[wcag-22-compliance]] | Reference for SC text (note Title II targets 2.1 AA, not 2.2) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: doj-rule-target-2.1-AA, population-bucket-deadline, surface-scope-public-only, evidence-not-attestation, third-party-content-included | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for conformance report | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: target-2.2-instead-of-2.1, third-party-excluded, self-attestation-without-audit | 700 |
| `content/04-procedure.xml` | essential | 5 steps: scope → bucket → audit → gap → report | 800 |
| `content/05-examples.xml` | essential | Worked example: a 75k-pop city portal | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree: entity type + population → deadline + scope | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scope-public-surfaces` | sonnet | Judgement: which URLs are public-facing. |
| `gap-analysis` | sonnet | Match audit findings to SCs + remediation cost. |
| `conformance-report` | sonnet | Legal-context drafting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conformance-report.md` | DOJ Title II conformance report skeleton with WCAG 2.1 AA scoresheet |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ada-title-ii-compliance-2026.py` | Validate conformance-report JSON against schema | Pre-submission / pre-procurement |

## Related

- [[accessibility-evaluation]]
- [[wcag-22-compliance]]
- [[accessibility-first-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
