<!-- purpose: Markdown skeleton for the structured-logging spec. -->
<!-- consumes: see content/02-output-contract.xml inputs for structured-logging-as-code -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# Structured Logging Spec

- owner: REPLACE
- last_reviewed: REPLACE

## Required fields
- ts (ISO-8601 UTC)
- level (DEBUG|INFO|WARN|ERROR)
- msg
- service
- env
- request_id
- trace_id

## Redaction
| Field / Regex | Policy |
|---------------|--------|
| user.email    | hash   |
| card_number   | drop   |
| (?i)password\|secret\|token | drop |

## Per-env levels
- dev: DEBUG
- staging: INFO + sampled DEBUG
- prod: INFO + 1% sampled DEBUG

## CI parser fixture
- path: tests/test_log_parser.py
- asserts: schema + redaction + trace_id
