<!--
- purpose: smoke-test fixture for multi-agent-design-patterns
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# multi-agent-design-patterns — smoke test

slug: multi-agent-design-patterns
version: 1.0.0
date: 2026-05-22
produces: decision-record
signature: b677c7cc1c524cc0

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-multi-agent-design-patterns.py templates/_smoke-test.json --self-test`
