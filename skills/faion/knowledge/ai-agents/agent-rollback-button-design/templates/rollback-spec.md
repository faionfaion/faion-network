<!--
purpose: Markdown skeleton for a rollback-button spec
consumes: bundle inventory, mutable/immutable partition, eval gate definition
produces: human-readable companion to the JSON spec
depends-on: content/01-core-rules.xml
token-budget-impact: ~400 tokens when rendered
-->
# Rollback Button Spec — {{spec_id}}

| Field | Value |
|---|---|
| Environment | {{environment}} |
| Owner | {{owner}} |
| Version | {{version}} |
| Last reviewed | {{last_reviewed}} |
| Audit log | `{{audit_log_path}}` |

## Bundle (reverts atomically)

- {{bundle_fields}}

## Immutable (preserved across rollback)

- {{immutable_fields}}

## Eval gate

- Golden set: `{{eval_gate.golden_set_version}}`
- Minimum pass-rate: `{{eval_gate.min_pass_rate}}`
- CI width: `{{eval_gate.ci_width}}`

## Operator UX

A single button labelled **"{{button_label}}"** is visible to ops users in the {{environment}} environment.
On click:
1. Verify rollback target passes eval gate; refuse if not (override requires named human + reason).
2. Acquire exclusive environment lock.
3. Apply bundle revert; do not touch immutable fields.
4. Write audit-log entry.
5. Release lock.

## Override

Override is gated by a named ops owner. Override invocation writes `{override: true, by: <handle>, reason: <text>}` to the audit log.
