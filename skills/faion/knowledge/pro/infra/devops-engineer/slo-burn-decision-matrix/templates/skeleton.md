<!-- purpose: SLO Burn Decision Matrix skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=decision-record -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# SLO Burn Decision Matrix — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-slo-burn-decision-matrix.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **matrix_version** (string (semver)): _value here_
- **portfolio_id** (string): _value here_
- **rows** (array (each {burn_category, service_class, action, owner, revert_criteria})): _value here_
- **audit_destination** (string (log store URL)): _value here_
- **default_cell** (string (escalate | accept)): _value here_
