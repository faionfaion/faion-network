<!-- purpose: viral-loop spec — inherent share event, K as invites per user x accept rate, measured cycle time and projection, anchored K target, invitee path and friction experiments, five joinable events, incentive on activation, consent and disclosure -->
<!-- consumes: joined loop events, K components, cycle-time distribution, invitee path conversions, category benchmark, templates/loop-projection.py -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/06-decision-tree.xml -->
<!-- token-budget-impact: ~700 tokens when loaded -->
# Viral Loop Spec — <loop_name> (<product_name>)

## Primary loop (inherent)
- share_event: <product event where sharing creates value for the inviter>
- kind: inherent
- value_to_inviter: <why the inviter shares as part of getting their own value>
- secondary_loop: <null, or invite_modal / referral_page with its own k>

## K-factor (templates/loop-anatomy.md.j2; at least two full cycles)
- invites_per_active_user: value <i>, window_days <n>, sample_size <n>
- accept_rate_per_invite: value <c>, window_days <n>, sample_size <n>
- k: <i x c, three decimals>
- cycles_measured: <2 or more>

## Cycle time and projection (templates/loop-projection.py)
- cycle_time: days <median inviter send to invitee first send>, method send_to_first_send_timestamps, sample_size <n>
- projection: starting_users <n>, days <n>, projected_users <project(starting_users, k, cycle_days, days)>, ignores_churn true

## K target (anchored to baseline and benchmark)
- current_k: <metric_baseline>
- target_k: <metric_target> (above 1.0 only when current_k is at least 0.4)
- kind: <self_sustaining when target_k is 1.0 or more; otherwise increment>
- benchmark: range_low <n>, range_high <n>, source <named source>

## Invitee path (at most three steps, measured)

| step | conversion |
|---|---|
| <open link> | <0.xx> |
| <create account> | <0.xx> |
| <first value action> | <0.xx> |

## Friction experiments (each names its step and the conversion it moves)

| name | target_step | current_conversion | expected_conversion |
|---|---|---|---|
| <experiment> | <a path step> | <that step's conversion> | <higher> |

## Events (five, each keyed on invite_id and inviter_user_id)
- invite_shown, invite_sent, invite_opened, invite_accepted, invitee_activated: keys <invite_id, inviter_user_id, ...>

## Retention
- invitee_d30: <0.xx>
- organic_d30: <0.xx>

## Incentive (templates/referral-program.md.j2; null when nothing is paid)
- referrer_reward / invitee_reward: <what each side gets>
- trigger_milestone: <activation event, never signup>, window_days <n>
- max_rewards_per_referrer_per_12_months: <n>
- self_referral_block: device_fingerprint, ip, payment_instrument
- excludes_existing_and_past_users: true

## Consent and disclosure
- recipient_source: <entered_by_inviter | consented_contact_import>
- casl_express_consent: true
- gdpr_lawful_basis: <consent | contract | legitimate_interest>
- compensation_disclosure: <message | landing_page | both; not_applicable only without an incentive>
