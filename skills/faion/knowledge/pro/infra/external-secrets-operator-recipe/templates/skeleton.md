<!-- purpose: External Secrets Operator Recipe skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=config -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# External Secrets Operator Recipe — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-external-secrets-operator-recipe.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **cluster_secret_store** (object {name, backend, auth_method, identity_ref}): _value here_
- **external_secrets** (array (each {name, namespace, refresh_interval, target_path, key_refs})): _value here_
- **rbac_scope** (enum (namespace | cluster_with_approver)): _value here_
- **alert_on_sync_failure** (boolean (true)): _value here_
- **rotation_test_runbook_path** (string): _value here_
- **mount_type** (enum (file | env_with_approver)): _value here_
