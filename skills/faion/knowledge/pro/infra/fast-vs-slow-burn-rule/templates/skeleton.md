<!-- purpose: Fast vs Slow Burn Rule skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=config -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# Fast vs Slow Burn Rule — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-fast-vs-slow-burn-rule.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **slo_id** (string): _value here_
- **slo_target** (number): _value here_
- **windows** (array (exactly 4 entries: 1h, 6h, 3d, 30d with burn_rate_threshold + routing)): _value here_
- **sli_recording_rule_prefix** (string): _value here_
- **alertmanager_routes** (object {window: receiver}): _value here_
- **runbook_urls** (object {window: url}): _value here_
