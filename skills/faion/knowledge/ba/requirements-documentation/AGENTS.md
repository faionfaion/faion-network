# Requirements Documentation

## Summary

**One-sentence:** Hierarchical requirements documentation pipeline (BR → SH → SR with FR/NFR split) producing typed BR/SH/SR records with acceptance criteria, source citations, and version-controlled artifacts.

**One-paragraph:** A structured methodology for documenting requirements across the hierarchy: business requirements (why), stakeholder requirements (user needs), and solution requirements (functional and non-functional). Each requirement carries an ID (BR/SH/SR/NFR), source citation (≥2 elicitation sessions), acceptance criteria, status, owner. Output is a version-controlled requirements pack ready for prioritization and traceability.

**Ефективно для:**

- Kickoff нової ініціативи з BR → SH → SR hierarchy.
- Регульований domain — auditor-grade specifications.
- Outsourced delivery: контрактні specs.
- Migration: документувати кожну поведінку до rewrite.

## Applies If (ALL must hold)

- New initiative kickoff requiring documented BR → SH → SR hierarchy.
- Regulated domain requiring auditor-grade requirement specifications.
- Outsourced delivery requiring contractual specifications.
- Migration / replatform where every behaviour must be documented before rewrite.
- Compliance evidence requiring trace from regulation → BR → SR.

## Skip If (ANY kills it)

- Pure agile shop with user-story-as-contract — use story format instead.
- Internal tooling where specifications are overhead.
- Hot fixes / single tickets.
- Pre-existing requirements pack already authoritative.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Elicitation session artifacts | JSON / Markdown | elicitation-techniques |
| Glossary registry | JSON | glossary-management-living-doc |
| Acceptance-criteria template | Markdown | acceptance-criteria methodology |
| Version-control venue | Git | engineering |
| Traceability seed | RTM JSON | requirements-traceability |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/elicitation-techniques` | Source citations come from typed session artifacts. |
| `pro/ba/business-analyst/glossary-management-living-doc` | Every term in requirements links to glossary. |
| `pro/ba/business-analyst/requirements-traceability` | Documentation feeds the RTM. |

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
| `br-drafting` | sonnet | Compose BR from elicitation evidence. |
| `sr-decomposition` | sonnet | Decompose BR into SR (FR + NFR). |
| `ac-extraction` | sonnet | Extract acceptance criteria per SR. |
| `spec-lint` | haiku | Lint frontmatter + glossary links + acceptance criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/br-record.md` | Business requirement record. |
| `templates/sh-record.md` | Stakeholder requirement record. |
| `templates/sr-record.md` | Solution requirement record (FR/NFR). |
| `templates/spec-frontmatter.yaml` | Frontmatter schema for all requirement records. |
| `templates/_smoke-test.md` | Minimum filled-in BR/SH/SR triple. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-documentation.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[elicitation-techniques]]
- [[requirements-traceability]]
- [[requirements-validation]]
- [[requirements-prioritization]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
