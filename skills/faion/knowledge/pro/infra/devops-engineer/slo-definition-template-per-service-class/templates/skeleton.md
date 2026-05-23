<!-- purpose: SLO Definition Template Per Service Class skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=spec -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# SLO Definition Template Per Service Class — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-slo-definition-template-per-service-class.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **slo_name** (string): _value here_
- **service_id** (string (matches catalog)): _value here_
- **service_class** (enum (http_api | async_worker | batch | static_asset | scheduled_job)): _value here_
- **sli_query** (string (PromQL recording-rule reference)): _value here_
- **target** (object (good_ratio_min | latency_p99_max | etc.)): _value here_
- **window_days** (integer (1 | 7 | 28 | 90)): _value here_
- **rationale** (string (≤300 chars)): _value here_
- **owner** (string): _value here_
