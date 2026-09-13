<!-- purpose: single-page channel-bet rubric — ICP sample, 3 to 6 tactic-level candidates scored on founder fit, ICP density and early traction, the 12-of-15 gate, one 90-day bet with weekly unit, checkpoints and kill criterion, parking lot -->
<!-- consumes: revenue by source, paying customers and qualified conversations with where they found the product, inbound leads per channel, Traction's 19 channels -->
<!-- produces: filled artefact for validate-single-channel-bet-selector.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~600 tokens when fully filled -->

# Channel Bet — <product_name>

- selected_on: <artefact_date>
- founder: <owner_full_name>
- rubric_location: <repository path or dated document URL>
- working_channel_exists: false
- icp_sample: paying_customers <n>, qualified_conversations <n> (at least 5 or 50)

## Candidates (3 to 6, tactic level, scored 1 to 5, no weights)

| channel | taxonomy_channel | founder_fit | icp_density | observed of sample | early_traction | unsolicited inbound | total | clears_bar |
|---|---|---|---|---|---|---|---|---|
| <the weekly tactic, not the category> | <one of Traction's 19> | <1-5> | <1-5; 1 without a sample> | <n of n> | <1-5> | <n> | <sum> | <12+ and every axis 3+> |

## Outcome
- outcome: <bet | no_bet>
- no_bet_route: <discovery | instrument_highest_scorer>, highest_scorer: <top total> (only on no_bet)

## The bet (one channel, 90 days)
- channel: <a clearing candidate>
- start_date: <YYYY-MM-DD>, end_date: <start + 90 days>
- weekly_unit: <count> x <countable unit of work>

| checkpoint week | metric | expected |
|---|---|---|
| 4 | <leading indicator> | <number> |
| 8 | <leading indicator> | <number> |

## Kill criterion (week 12, written on selected_on, never revised)
- conditions: <metric> < <value> AND <metric> < <value>
- action: rerun_rubric_with_result_as_early_traction
- revised: false

## Parking lot (no new weekly effort until the grade)

| channel | total |
|---|---|
| <every other candidate> | <its total> |

- active_work_allowed: false
