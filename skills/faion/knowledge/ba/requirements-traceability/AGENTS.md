# Requirements Traceability Matrix (RTM) Generation and Maintenance

## Summary

**One-sentence:** Bidirectional RTM pipeline (forward coverage need→test, backward justification test→need) producing per-requirement trace records over consistent role vocabulary suitable for automated coverage analysis.

**One-paragraph:** Requirements traceability links every artifact (business requirement, stakeholder requirement, solution requirement, design, code, test) to its origin and downstream dependents, enabling forward coverage analysis (need → test) and backward justification (test → need). RTM uses a consistent role vocabulary so automated tools can query coverage reliably. Output: per-requirement trace record + project-level RTM with coverage + orphan reports.

**Ефективно для:**

- Регульований domain з auditor evidence.
- Long програма, де impact analysis обов'язковий.
- Multi-team програма з cross-team trace.
- Migration: legacy behaviour → new requirement → test.

## Applies If (ALL must hold)

- Regulated domain requiring auditor-grade trace evidence.
- Long programme where impact analysis on change is mandatory.
- Multi-team programme needing cross-team trace.
- Migration: every legacy behaviour must trace to a new requirement.
- Compliance: regulation → BR → SR → test trace.

## Skip If (ANY kills it)

- Small agile team where story → PR → test is enough.
- Hot fixes.
- Spike phase without committed requirements.
- Pre-existing RTM authoritative and freshly maintained.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Requirements pack | Markdown / YAML | requirements-documentation |
| Test plan / test cases | Markdown / Cucumber | QA |
| Design artifacts | Markdown / diagrams | architecture |
| Code repository | Git | engineering |
| Role vocabulary policy | YAML | this methodology |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/requirements-documentation` | Source records. |
| `pro/ba/business-analyst/requirements-validation` | Verifies forward coverage. |
| `pro/ba/business-analyst/requirements-lifecycle` | Status changes propagate via RTM. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `forward-coverage` | sonnet | From need to test; identify gaps. |
| `backward-justification` | sonnet | From test to need; identify orphans. |
| `impact-analysis` | sonnet | On change, surface affected nodes. |
| `rtm-render` | haiku | Render matrix + coverage report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rtm.md` | RTM skeleton with role vocabulary. |
| `templates/per-req-trace.md` | Per-requirement trace block. |
| `templates/rtm.py` | Render RTM + coverage report from YAML store. |
| `templates/_smoke-test.md` | Minimum filled-in RTM. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-traceability.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[requirements-documentation]]
- [[requirements-validation]]
- [[requirements-lifecycle]]
- [[data-driven-requirements]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
