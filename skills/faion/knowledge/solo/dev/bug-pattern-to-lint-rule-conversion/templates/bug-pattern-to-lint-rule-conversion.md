<!--
purpose: Decision-record skeleton authors fill before wiring a lint rule.
consumes: nothing — this IS the input form.
produces: record ready for the validator + commit to decisions/.
depends-on: tracker references; lint config; sample bad + good code.
token-budget-impact: ~180 tokens when copied.
-->

# Decision-record — &lt;pattern_id&gt;

## Identity
- artefact_id: bplrc-&lt;slug&gt;
- pattern_id (kebab-case):
- owner_email (named human):

## Cluster
- ticket_refs (≥3, links): []
- recurrence window: 30 / 90 days
- cluster_size:

## Detector
- kind: ruff | eslint | regex | ast-visitor | test-name | shellcheck | custom
- definition (rule id, regex pattern, AST predicate):
- rule_id (if available):

## Fix
- one-line corrective action + link to docs:

## False-positive scan
- ran against last 90 days of code:
- total fires:
- true positives:
- false positives:
- fp_rate_pct:

## Wiring
- wired_into_pre_commit: true | false
- CHANGELOG entry:

## Verdict
- [ ] record-and-wire
- [ ] block-low-recurrence
- [ ] block-no-detector
- [ ] block-fp-too-high

## Versioning
- version: 1.0.0
- last_reviewed: YYYY-MM-DD
