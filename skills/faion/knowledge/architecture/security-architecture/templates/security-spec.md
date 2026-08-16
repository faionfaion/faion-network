<!-- __faion_header_v1__ -->
<!-- purpose: Spec skeleton tying threat-model + controls + ASVS coverage. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~300 tokens once filled -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Spec skeleton tying threat-model + controls + ASVS coverage.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/02-output-contract.xml","token_budget_impact":"~300 tokens once filled"}} -->
# Security Spec

## Identity & Access
- IAM provider: <fill>
- AuthN: <oidc_oauth_passwordless>
- MFA scope: <fill>

## Authorisation
- Model: RBAC / ABAC / hybrid
- Matrix: see authz-matrix.json

## Secrets
- Provider: <vault_ssm_kms>
- Rotation: <cadence>
- Scope: per-service

## Data
- At rest: AES-256
- In transit: TLS 1.2+
- Backups: encrypted + key-separated

## Threat model
- See threat-model-stride.md

## OWASP ASVS L2 controls
- Inventory of covered + uncovered controls.

## Incident response
- Detection signals, runbooks, retro cadence.
