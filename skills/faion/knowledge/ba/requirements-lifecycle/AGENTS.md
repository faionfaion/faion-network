# Requirements Lifecycle Management

## Summary

**One-sentence:** Per-requirement state machine (Draft → Approved → Implemented → Verified) with change-control gates, multi-role sign-off, and immutable version log producing audit-grade traceability of every status transition.

**One-paragraph:** A governance framework for managing requirements from initial capture through implementation and verification. Per-requirement state machine: Draft, Reviewed, Approved, Implemented, Verified, Deferred, Rejected. Forward-only transitions; backward-state corruption blocked. Change control: multi-role sign-off (BA + Product + Architecture + QA), impact analysis required for every change, version history immutable. Output: per-requirement lifecycle log + change records.

**Ефективно для:**

- Регульований domain з auditor-grade lifecycle evidence.
- Long-running програма з частими change requests.
- Outsourced delivery: формальний change control.
- Compliance: per-requirement status history як evidence.

## Applies If (ALL must hold)

- Regulated domain (SOX 404, ISO 9001, GxP) requiring auditor-grade lifecycle evidence.
- Long-running programme with frequent change requests.
- Outsourced delivery requiring formal change control.
- Compliance evidence requiring per-requirement status history.
- Multi-team programme where ad-hoc edits create version confusion.

## Skip If (ANY kills it)

- Small agile team with single-source story tracker (Linear / Jira) as authoritative.
- Internal hot-fix tooling.
- Pre-MVP discovery phase where requirements are still volatile.
- Single-person project with no audit obligation.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Requirements pack | Markdown / YAML | requirements-documentation |
| State-machine policy | Markdown | this methodology |
| Multi-role sign-off list | JSON | governance |
| Change-control template | Markdown | templates/ |
| Version-control venue | Git | engineering |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/requirements-documentation` | Source records to manage. |
| `pro/ba/business-analyst/requirements-traceability` | RTM tracks impact across status changes. |
| `pro/ba/business-analyst/requirements-validation` | Validation gate before Verified status. |

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
| `transition-validator` | haiku | Validate state-machine transitions; reject backward-corruption. |
| `change-impact-analysis` | sonnet | Analyse impact of a proposed change on linked artifacts. |
| `sign-off-orchestration` | sonnet | Route change to BA + Product + Architecture + QA. |
| `version-history-compose` | haiku | Compose immutable diff entries. |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-request.md` | Change request template with impact analysis. |
| `templates/requirements-status-log.md` | Per-requirement status log. |
| `templates/version-history.md` | Immutable version history block. |
| `templates/_smoke-test.md` | Minimum filled-in lifecycle record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-lifecycle.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[requirements-documentation]]
- [[requirements-validation]]
- [[requirements-traceability]]
- [[requirements-prioritization]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
