<!-- purpose: Error Budget Policy and Freeze Rules skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=decision-record -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# Error Budget Policy and Freeze Rules — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-error-budget-policy-and-freeze-rules.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **policy_version** (string (semver)): _value here_
- **doctrine_url** (string): _value here_
- **authorised_declarers** (array): _value here_
- **freeze_allow_list** (array (e.g. security_patch, rollback, tier0_bugfix)): _value here_
- **freeze_deny_list** (array): _value here_
- **revert_criteria** (object (e.g. budget_remaining_min, burn_rate_max, duration_h)): _value here_
- **comms_channels** (array (slack channel, email list)): _value here_
- **review_date** (string): _value here_
- **signoff** (object (engineering_leader, product_vp, date)): _value here_
