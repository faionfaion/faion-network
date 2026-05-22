<!--
- purpose: smoke-test fixture for model-evaluation
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# model-evaluation — smoke test

slug: model-evaluation
version: 1.0.0
date: 2026-05-22
produces: report
signature: c795c4f604b973f7

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-model-evaluation.py templates/_smoke-test.json --self-test`
