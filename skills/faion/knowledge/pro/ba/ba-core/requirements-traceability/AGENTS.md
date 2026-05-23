---
slug: requirements-traceability
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a Requirements Traceability Matrix (RTM) linking each requirement forward to design / code / test / release artefacts and backward to source elicitation.
content_id: "bf1a519357282dbb"
complexity: medium
produces: spec
est_tokens: 4300
tags: [ba, traceability, rtm, compliance, audit]
---
# Requirements Traceability

## Summary

**One-sentence:** Produces a Requirements Traceability Matrix (RTM) linking each requirement forward to design / code / test / release artefacts and backward to source elicitation.

**One-paragraph:** Produces a Requirements Traceability Matrix (RTM) linking each requirement forward to design / code / test / release artefacts and backward to source elicitation. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Audit-driven engagement (ISO/SOC2/FDA), де bidirectional traceability — обов'язково.
- Cross-team initiative, де requirement розходиться у design/code/test/release.
- Defect investigation: треба знайти який requirement був mis-implemented.
- Change-impact analysis перед великим CR — щоб порахувати ripple.

## Applies If (ALL must hold)

- Engagement under audit (ISO, SOC2, FDA, gov) requires bidirectional traceability.
- Large multi-team initiative where requirements ripple into many artefacts.
- Defect investigation needs to identify which requirement was misimplemented.
- Change-impact analysis where downstream artefacts must be located fast.

## Skip If (ANY kills it)

- Small initiative (<10 requirements) where traceability overhead > value.
- Throwaway prototype with no audit need.
- Tooling already provides traceability natively (Polarion, Jama) and an extra matrix is redundant.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements register | Output of requirements-documentation | BA |
| Design artefact list | Wiki / Confluence | architects |
| Code repository | Git | engineering |
| Test plan | Output of acceptance-criteria + test management tool | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[requirements-documentation]] | source of requirement IDs |
| [[acceptance-criteria]] | AC IDs feed the test column |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-artefact-refs` | haiku | Mechanical scan of design / code / test for requirement-ID references. |
| `build-matrix` | sonnet | Assemble RTM with per-direction completeness. |
| `flag-gaps` | sonnet | Identify orphan requirements + orphan code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rtm-template.md` | RTM matrix template with columns: req_id, design_ref, code_ref, test_ref, release_ref. |
| `templates/rtm_min.py` | Stdlib RTM generator that scans repo for req-ID mentions. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-traceability.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[requirements-documentation]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
