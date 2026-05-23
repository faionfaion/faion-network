<!-- purpose: RTM matrix template with columns: req_id, design_ref, code_ref, test_ref, release_ref. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Requirements Traceability Matrix

| req_id | source_ref | design_ref | code_ref | test_ref | release_ref |
|---|---|---|---|---|---|
| REQ-001 | elicit/2026-04-12.md | design.md#auth | src/auth/oauth.ts | tests/auth.spec.ts | v1.2.0 |
