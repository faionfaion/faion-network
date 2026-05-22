<!--
purpose: human-readable wrapper around the mocking-spec JSON for code review
consumes: validated spec.json from the output contract
produces: rendered markdown for owner sign-off
depends-on: 02-output-contract.xml schema
token-budget-impact: ~300 tokens
-->

# Mocking Spec — `<project>`

## Drivers

- `is_own_code`: `<value>`
- `is_io_or_time_or_random`: `<value>`
- `verify_calls_needed`: `<value>`
- `stateful_reuse_count`: `<value>`

## Decision

- `language`: `<python | typescript | go>`
- `runner`: `<pytest | vitest | jest | go-test>`
- `adapter_layer_path`: `<path>`

## Doubles

| Dependency | Type | Boundary | Tool |
|---|---|---|---|
| `<dep>` | `<stub|mock|fake|...>` | `<io-network|time|...>` | `<pytest-mock|freezegun|...>` |

## Audit

Rules consulted: `<r-list>` — see content/01-core-rules.xml.
