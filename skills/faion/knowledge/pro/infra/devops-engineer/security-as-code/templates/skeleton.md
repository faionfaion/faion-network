<!-- purpose: Security as Code (Policy as Code) skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=config -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# Security as Code (Policy as Code) — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-security-as-code.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **pipeline_stage** (enum (build | test | sca | sast | sign | deploy | admission | runtime)): _value here_
- **scanner_or_policy** (string (tool name + version)): _value here_
- **block_severity_threshold** (enum (critical | high | medium | low)): _value here_
- **policy_repo_path** (string (relative to monorepo)): _value here_
- **enforce_mode** (enum (enforce | audit)): _value here_
- **waiver_required_for_exception** (boolean (true)): _value here_
- **audit_destination** (string (SIEM / log store URL)): _value here_
- **signing_attestation** (object (cosign + key reference)): _value here_
