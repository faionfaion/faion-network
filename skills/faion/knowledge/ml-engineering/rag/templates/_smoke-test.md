<!--
- purpose: smoke-test fixture for rag
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# rag — smoke test

slug: rag
version: 1.0.0
date: 2026-05-22
produces: spec
signature: 16c058db94cba3bd

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-rag.py templates/_smoke-test.json --self-test`
