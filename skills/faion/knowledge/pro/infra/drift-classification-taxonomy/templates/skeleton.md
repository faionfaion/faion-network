<!-- purpose: Drift Classification Taxonomy skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=rubric -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# Drift Classification Taxonomy — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-drift-classification-taxonomy.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **drift_id** (string): _value here_
- **environment** (string): _value here_
- **resource_address** (string (TF address)): _value here_
- **detected_at** (string (ISO-8601)): _value here_
- **class** (enum (hand_edit | external_automation | vendor_change | legitimate_emergency | unknown)): _value here_
- **evidence** (object (source + reference)): _value here_
- **fix_action** (enum (revert | backport | provider_bump | boundary_review | triage)): _value here_
- **fix_pr_url** (string (null if not yet open)): _value here_
- **triage_owner** (string): _value here_
- **triage_at** (string (ISO-8601)): _value here_
