<!--
- purpose: smoke-test fixture for rag-evaluation
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# rag-evaluation — smoke test

slug: rag-evaluation
version: 1.0.0
date: 2026-05-22
produces: report
signature: e0dd7566a01ba1dd

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-rag-evaluation.py templates/_smoke-test.json --self-test`
