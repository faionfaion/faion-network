<!-- purpose: Async11Note skeleton with 3 named prompts + response section -->
<!-- consumes: pair_id + cycle_iso + response_window -->
<!-- produces: scaffold populated by compose-prompts -->
<!-- depends-on: content/01-core-rules.xml#r-three-named-prompts-fixed -->
<!-- token-budget-impact: ~140 tokens -->

# Async 1:1 — <pair_id>

**Cycle:** YYYY-Www
**Owner:** <pm_role> / <owner_full_name>
**Version / last reviewed:** 1.0.0 / YYYY-MM-DD (review within 90 days)
**Response window:** N business hours (24-168, default 48), counted in the IC's timezone
**Channel:** private_doc | dm | email; visible to pm and ic only; morale never shared outside the pair

## Why async this cycle

- reason: no_overlapping_hours | temporary_leave | sickness | travel
- consecutive_async_cycles: N (max 3 without a synchronous call); last_sync_call_cycle: YYYY-Www

## Prompts (PM posts; the three fixed prompts)

- **Blockers:** What is blocking your current sprint goals? Cite the WBS id or ticket and what is upstream of it.
- **Decisions needed:** What decision are you waiting on, from whom, and by which date?
- **Morale:** Workload 1-10, autonomy 1-10, clarity 1-10, and anything else you want me to know.

## Posting

- ic_timezone: Area/City; posted_at: YYYY-MM-DDTHH:MM+hh:mm; window_closes_at: YYYY-MM-DDTHH:MM+hh:mm (IC's working days, holidays excluded); reminders_sent: 0

## IC response (IC writes it here; "none" is an answer, a missing field is not)

- status: answered | unresponsive | paused (leave_type: vacation | parental | sick)
- received_at: YYYY-MM-DDTHH:MM+hh:mm; authored_by: ic
- blockers: ...
- decisions_needed: ...
- morale: workload N, autonomy N, clarity N; ...

## PM acknowledgement (within 24 business hours of received_at)

- acked_at: YYYY-MM-DDTHH:MM+hh:mm; ack_business_hours_after_response: N
- next_actions: [{action, owner_role, deadline_sprint: S14}] (one per reported blocker or decision)

## Escalation

- count_before_cycle: N; unresponsive_count: 0 (answered) | before + 1 (unresponsive) | unchanged (paused)
- action: none (count 0) | synchronous_reschedule (count 1; sync_slot_offered_for_cycle) | escalate_to_manager (count 2+; manager_packet: manager, count, last acked next_actions, includes_morale: false)

## Quarterly review (every 90 days at most)

- computed_at; cycles_in_quarter; in_window_responses; response_rate = ratio; below_80_over_4_cycles
- structural_decision: none | change_response_window | restructure_pair | mandate_synchronous (required when below 80%); version_after
