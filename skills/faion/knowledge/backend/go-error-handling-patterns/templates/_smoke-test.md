<!--
purpose: Filled-in minimum viable example of a Go Error Handling Patterns (Wrap, Translate, Sentinel, Log-Once) artefact.
consumes: nothing — fixture.
produces: a worked Markdown example for tests / docs.
depends-on: content/02-output-contract.xml + templates/go-error-handling-patterns.md.
token-budget-impact: ~150 tokens.
-->

# Go Error Handling Patterns (Wrap, Translate, Sentinel, Log-Once) — goep-smoke-001

- **artefact_id**: goep-smoke-001
- **owner**: alice@acme.com
- **status**: active
- **version**: 1.0.0
- **last_reviewed**: 2026-05-23

## Decision

`internal/apperror` with `ErrNotFound`, `ErrConflict`, `ErrPermission`; repository translates `sql.ErrNoRows` + `pgerrcode.UniqueViolation`; handler logs once + returns AppError.

## Rationale

Decision cites the scope doc (input A) and the workload sample (input B). The scenario is the canonical instance for this gap; the rationale exceeds the 60-character floor and names every input it relies on.

## Inputs used

- scope_doc — repo:engagements/acme/scope.md
- workload_sample — repo:engagements/acme/workload.csv

## Notes

Ready for owner review; supersedes none.
