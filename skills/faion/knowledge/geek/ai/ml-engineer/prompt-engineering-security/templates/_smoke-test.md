<!--
- purpose: smoke-test fixture for prompt-engineering-security
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# prompt-engineering-security — smoke test

slug: prompt-engineering-security
version: 1.0.0
date: 2026-05-22
produces: spec
signature: 768bc1948179ed8b

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-prompt-engineering-security.py templates/_smoke-test.json --self-test`
