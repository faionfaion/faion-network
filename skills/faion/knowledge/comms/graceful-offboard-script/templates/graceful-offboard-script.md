<!-- purpose: offboard script and handover-plan skeleton — same sections and field names as content/02-output-contract.xml -->
<!-- consumes: QBR data for the account, the signed contract's termination clause, the agency's asset list for the client, partner network (AGENTS.md Prerequisites) -->
<!-- produces: an offboard artefact validating against scripts/validate-graceful-offboard-script.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~700 tokens once filled -->

# Offboard — <client_name>

## Bad-fit evidence (`qbr_source`: path to the QBR file)

| Signal (margin below target / out-of-scope requests above cap / days-to-pay above terms / hours over budget / satisfaction below threshold) | Value | Target | Period | Consecutive quarters (margin: 2+) |
|-----------|-------|--------|--------|-------------------------------|

## Contract

- `termination_clause_id`: — `notice_days`: — `minimum_term_end`:
- `decision_date`: — `last_service_date`: <end_date> — `days_notice_given`:
- Prepaid or committed period: exists? — disposition: delivered_in_full | refunded

## Script (framing = fit_and_alignment)

Fit statement: "Your needs have moved toward X; we are built for Y."

- States the last service date: yes
- Banned phrases found: none — any sentence criticising the client: none

## Handover plan

| Asset | Kind | Owned by | Transfer method | Transfer date | Conditioned on payment (clause id if yes) |
|-------|------|----------|-----------------|---------------|-------------------------------------------|

- Transition support: (days), included | at named rate:

## Recommended alternative (confirmed before being named)

- Provider: — matched need: — confirmed on: — via: call | email | meeting | message — warm introduction offered: yes

## Delivery

- Live conversation: date, channel (call | video_call | in_person_meeting), delivered by <owner_full_name>
- Written follow-up: date (within one business day), contains only what was said, handover plan attached
- Email only: no

## Feedback request (T+30)

- `scheduled_date` = last service date + 30
- Promoter (9-10): ask for testimonial / referral — otherwise: thank, ask one question, never argue

## Internal record

- Root cause: pricing_and_margin | scope_and_expectations | capability_fit | communication_and_working_style | payment_behaviour
- Intake or qualification change: — flagged for review (if none), reviewer:

## Validation

Run `python scripts/validate-graceful-offboard-script.py --file <path-to-filled-json>`. Exit 0 = valid, exit 1 = violations listed on stderr.
