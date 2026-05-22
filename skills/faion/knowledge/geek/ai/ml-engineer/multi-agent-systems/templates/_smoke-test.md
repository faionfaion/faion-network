<!--
- purpose: smoke-test fixture for multi-agent-systems
- consumes: none
- produces: minimum-viable filled-in payload
- depends-on: content/02-output-contract.xml
- token-budget-impact: tiny
-->

# multi-agent-systems — smoke test

slug: multi-agent-systems
version: 1.0.0
date: 2026-05-22
produces: spec
signature: d607a24d93324af6

## Body

- Filled-in example matching the contract.

## Validator

Run: `python scripts/validate-multi-agent-systems.py templates/_smoke-test.json --self-test`
