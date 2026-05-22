<!--
purpose: human-readable wrapper of the hardening-plan JSON
consumes: validated decision-record
produces: PR-reviewable summary
depends-on: 02-output-contract.xml schema
token-budget-impact: ~350 tokens
-->

# Hardening plan: `<chain-name>`

## Drivers
- target_uptime: `<n>`
- latency_budget_ms: `<n>`
- providers: `<list>`
- dep_policy: `<locked|floating>`

## Decisions
| Layer | Choice |
|---|---|
| Fallbacks | `<comma list>` |
| Retry | `max_attempts=<n>, backoff=<exp|lin|none>` |
| Configurable fields | `<list>` |
| Pinning | `<exact-hash|exact|minor-upper-bound|floating>` |

## Patch

```python
# templates/chain-hardening-patch.py with substitutions
```

## Audit
Rules: `<r-list>`
