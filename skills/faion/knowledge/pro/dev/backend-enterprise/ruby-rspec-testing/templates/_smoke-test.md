<!--
purpose: Filled-in minimum viable example of a RSpec Testing for Rails Applications artefact.
consumes: nothing — fixture.
produces: a worked Markdown example for tests / docs.
depends-on: content/02-output-contract.xml + templates/ruby-rspec-testing.md.
token-budget-impact: ~150 tokens.
-->

# RSpec Testing for Rails Applications — rspec-smoke-001

- **artefact_id**: rspec-smoke-001
- **owner**: alice@acme.com
- **status**: active
- **version**: 1.0.0
- **last_reviewed**: 2026-05-23

## Decision

Model + service + request specs (no system spec yet); SimpleCov branch ≥80; suite under 30s on dev box.

## Rationale

Decision cites the scope doc (input A) and the workload sample (input B). The scenario is the canonical instance for this gap; the rationale exceeds the 60-character floor and names every input it relies on.

## Inputs used

- scope_doc — repo:engagements/acme/scope.md
- workload_sample — repo:engagements/acme/workload.csv

## Notes

Ready for owner review; supersedes none.
