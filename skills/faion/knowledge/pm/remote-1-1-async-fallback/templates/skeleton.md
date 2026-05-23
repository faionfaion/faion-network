<!-- purpose: Async11Note skeleton with 3 named prompts + response section -->
<!-- consumes: pair_id + cycle_iso + response_window -->
<!-- produces: scaffold populated by compose-prompts -->
<!-- depends-on: content/01-core-rules.xml#r2-bounded-output -->
<!-- token-budget-impact: ~140 tokens -->

# Async 1:1 — [pair_id]

**Cycle:** YYYY-Www
**Owner:** [PM role] / [person]
**Response window:** [N business hours, 24-168]
**Last reviewed:** YYYY-MM-DD

## Prompts (PM posts; named, ≥10 chars each)

- **Blockers:** What is blocking your current sprint goals? Cite the WBS id and what is upstream.
- **Decisions needed:** What decision are you waiting on, from whom, and by when?
- **Morale:** Workload 1-10, autonomy 1-10, clarity 1-10 — and anything else you want me to know.

## IC response (IC fills in within response_window)

- received_at: YYYY-MM-DDTHH:MM:SSZ
- blockers: ...
- decisions_needed: ...
- morale: ...

## PM acknowledgement

- acked_at: YYYY-MM-DDTHH:MM:SSZ
- next_actions: [{action, owner_role, deadline_sprint: S14}]

## Escalation

- unresponsive_count: 0
- action: none | synchronous_reschedule | escalate_to_manager
