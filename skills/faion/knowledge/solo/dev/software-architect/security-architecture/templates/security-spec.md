<!-- __faion_header_v1__ -->
<!-- purpose: Spec skeleton tying threat-model + controls + ASVS coverage. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#r1-zero-trust-default -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Spec skeleton tying threat-model + controls + ASVS coverage.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-zero-trust-default","token_budget_impact":"~150 tokens when loaded"}} -->
# Security Spec

## Identity & Access
- IAM provider: <fill>
- AuthN: <OIDC/OAuth/passwordless>
- MFA scope: <fill>

## Authorisation
- Model: RBAC / ABAC / hybrid
- Matrix: see authz-matrix.json

## Secrets
- Provider: <Vault / SSM / KMS>
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
