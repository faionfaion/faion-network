<!--
- purpose: smoke-test fixture for prompt-engineering-fundamentals
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# prompt-engineering-fundamentals — smoke test

slug: prompt-engineering-fundamentals
version: 1.0.0
date: 2026-05-22
produces: playbook-step
signature: 374c45ac16101e21

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-prompt-engineering-fundamentals.py templates/_smoke-test.json --self-test`
