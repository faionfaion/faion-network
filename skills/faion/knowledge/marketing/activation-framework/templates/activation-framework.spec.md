<!-- purpose: activation spec skeleton — one event with a window, D30 validation, closed-cohort baseline, event-mapped funnel, drop-offs by absolute loss, ICE backlog, weekly dashboard -->
<!-- consumes: the event table, signup-week cohorts, the data cutoff date, templates/ice.py -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/06-decision-tree.xml -->
<!-- token-budget-impact: ~700 tokens when loaded -->
# Activation Framework — Spec for <product_name>

## Activation event
- name: <activation_event_name> (one tracked event name, snake_case, as it appears in the event table)
- window_days: <window_days> (counted from signup)

## D30 validation (one closed cohort)
- cohort: <signup week label>
- performed the event in the window: users <n>, D30 retention <0.xx>
- did not perform it: users <n>, D30 retention <0.xx>
- correlational_note: true (the relationship is correlational; forcing the event does not create retention)

## Baseline (closed signup-week cohorts only)
- data_cutoff: <data_cutoff>

| signup_week_start | signups | activated | activation_rate |
|---|---|---|---|
| <YYYY-MM-DD> | <n> | <n> | <activated / signups, 3 decimals> |
| <at least four consecutive closed weeks: week end + window_days before data_cutoff> | | | |

## Funnel (signup to activation event, in order)

| step | status | event | entered | completed | instrumentation_task |
|---|---|---|---|---|---|
| <name> | instrumented | <event_name> | <n> | <n> | |
| <name> | uninstrumented | | | | <ticket id: emit which event from where> |

## Drop-off priorities (sorted by users_lost descending)

| step | users_lost (entered - completed) | relative_drop (users_lost / entered) |
|---|---|---|
| <step> | <n> | <0.xxx> |

## Experiment backlog (sorted by ice descending; ice = round((impact + confidence + ease) / 3, 2) from templates/ice.py)

| name | funnel_step | hypothesis (one sentence) | primary_metric | baseline_value | ship_threshold_lift | impact | confidence | ease | ice |
|---|---|---|---|---|---|---|---|---|---|
| <name> | <step from the funnel> | <sentence> | activation_rate or step_conversion | <0.xxx> | <minimum lift to ship> | <1-10> | <1-10> | <1-10> | <x.xx> |

## Weekly dashboard
- cadence: weekly
- closed_cohorts_only: true
- window_days: <window_days> (same as the activation event)
- segment_by: acquisition_channel
- series_id: <series_id> (encodes event and window; a change starts a new series, never an edit of history)
