<!-- purpose: Edge and CDN Strategy skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=spec -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# Edge and CDN Strategy — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-edge-and-cdn-strategy.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **platform** (enum (cloudflare | lambda_edge | fastly_compute | akamai)): _value here_
- **routes** (array (each {pattern, cache_ttl, cache_key, auth_at_edge, origin_shield})): _value here_
- **fallback_dns_record** (string): _value here_
- **per_request_cost_budget_usd** (number): _value here_
- **cache_hit_ratio_target** (number): _value here_
- **auth_handoff_method** (enum (jwt_signed | mtls | shared_secret)): _value here_
