<!--
- purpose: smoke-test fixture for prompt-engineering-reasoning
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# prompt-engineering-reasoning — smoke test

slug: prompt-engineering-reasoning
version: 1.0.0
date: 2026-05-22
produces: playbook-step
signature: 6600177b05dad9b9

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-prompt-engineering-reasoning.py templates/_smoke-test.json --self-test`
