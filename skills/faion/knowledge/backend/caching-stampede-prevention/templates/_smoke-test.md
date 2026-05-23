<!--
purpose: Filled-in minimum viable example of a Cache Stampede Prevention (Distributed Lock, Probabilistic Refresh, Coalescing) artefact.
consumes: nothing — fixture.
produces: a worked Markdown example for tests / docs.
depends-on: content/02-output-contract.xml + templates/caching-stampede-prevention.md.
token-budget-impact: ~150 tokens.
-->

# Cache Stampede Prevention (Distributed Lock, Probabilistic Refresh, Coalescing) — csp-smoke-001

- **artefact_id**: csp-smoke-001
- **owner**: alice@acme.com
- **status**: active
- **version**: 1.0.0
- **last_reviewed**: 2026-05-23

## Decision

SETNX lock with 5s TTL + UUID token + Lua conditional release; XFetch β=1.5 for ramp; in-process singleflight for coalescing; TTL = 60s ±10% jitter.

## Rationale

Decision cites the scope doc (input A) and the workload sample (input B). The scenario is the canonical instance for this gap; the rationale exceeds the 60-character floor and names every input it relies on.

## Inputs used

- scope_doc — repo:engagements/acme/scope.md
- workload_sample — repo:engagements/acme/workload.csv

## Notes

Ready for owner review; supersedes none.
