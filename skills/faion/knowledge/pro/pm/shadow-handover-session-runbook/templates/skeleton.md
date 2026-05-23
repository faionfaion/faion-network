<!-- purpose: HandoverSessionRecord skeleton with task list + gap log + sign-off -->
<!-- consumes: outgoing + receiver identity, pre-agreed task list -->
<!-- produces: scaffold consumed by task-list-prep step -->
<!-- depends-on: content/01-core-rules.xml#r5-no-skipped-tasks -->
<!-- token-budget-impact: ~160 tokens -->

# Shadow Handover Session — [session_id]

**Owner:** [PM role] / [person]
**Outgoing engineer:** [handle]
**Receiver:** [handle]
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Task list (pre-agreed, ≥ 5 tasks)

| task_id | description | receiver_drove | verdict |
|---------|-------------|----|---|
| T1 | [Operational task — receiver should drive] | false | (set after session) |

## Gap log

| question | answer | doc_link |
|----------|--------|----------|
| Where does the prod DB password live? | 1Password vault 'prod-db' | wiki/secrets#prod-db |
| How do I restart the worker pool? | systemctl restart worker@* | null (open: write runbook entry) |

## Sign-off

- outgoing_signed_by: [outgoing handle]
- receiver_signed_by: [receiver handle]
- signed_at: YYYY-MM-DD
- spf_undocumented: [list any single-point-of-failure facts still without doc_link]
