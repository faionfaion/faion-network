<!--
purpose: Filled-in minimum viable example of a Go Channels and Pipeline Patterns artefact.
consumes: nothing — fixture.
produces: a worked Markdown example for tests / docs.
depends-on: content/02-output-contract.xml + templates/go-channels.md.
token-budget-impact: ~150 tokens.
-->

# Go Channels and Pipeline Patterns — goch-smoke-001

- **artefact_id**: goch-smoke-001
- **owner**: alice@acme.com
- **status**: active
- **version**: 1.0.0
- **last_reviewed**: 2026-05-23

## Decision

Three stages, directional channels, fan-out 1k workers + fan-in merge, sender closes each stage, `select` with `ctx.Done()` everywhere, `goleak` in pipeline test.

## Rationale

Decision cites the scope doc (input A) and the workload sample (input B). The scenario is the canonical instance for this gap; the rationale exceeds the 60-character floor and names every input it relies on.

## Inputs used

- scope_doc — repo:engagements/acme/scope.md
- workload_sample — repo:engagements/acme/workload.csv

## Notes

Ready for owner review; supersedes none.
