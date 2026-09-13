<!-- purpose: retainer spec — one named shape with its terms, price at 1.3x hourly equivalent, scope lists and turnaround, term and notice, advance billing, hourly cutover, capacity ledger, 6-month outcome review -->
<!-- consumes: client request pattern and last 3 months of hourly invoices, rate card, active retainer list, available billable hours -->
<!-- produces: filled artefact for validate-retainer-pricing-methodology.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~700 tokens when fully filled -->

# Retainer Spec — <client_name>

- start_date: <start_date>
- owner: <owner_full_name>

## Shape (exactly one)
- kind: <block_of_hours | outcome_based | availability | hybrid>
- block_of_hours: prepaid_hours_per_month <n>, rollover <none | one_period | capped with rollover_cap_hours>, overage_hourly_rate <n>
- outcome_based: deliverables_per_period <list>
- availability: response_time_business_hours <n>, max_monthly_load_hours <n>
- hybrid: invoicing_shape <which shape invoices>, scope_dispute_clause <which clause governs scope>

## Pricing (at or above 1.3x the hourly equivalent)
- expected_monthly_hours: <n; maximum load for availability>
- hourly_rate: <n> <currency>
- monthly_price: <n> = expected_monthly_hours x hourly_rate x multiple
- multiple: <1.3 or more>
- concession: <null, or twelve_month_minimum_term | full_term_prepaid when below 1.3>

## Scope
- inclusions: <written list>
- exclusions: <new-feature builds, emergency weekend work, third-party costs, meetings beyond the count>
- turnaround: <n> <business_hours | business_days>
- included_meetings_per_month: <n>

## Term, notice and price review
- minimum_months: <3 or more>
- notice_days: <30 or more, either side>
- price_review_date: <no later than 12 months after start_date>

## Billing (in advance)
- timing: in_advance, invoice_days_before_period_start: <n>
- payment_due: before_period_start, payment_terms_days: <n>

## Hourly phase-out (null for a new client)
- avg_billed_hours_last_3_months: <n>, avg_monthly_spend_last_3_months: <n>
- cutover_date: <on or after start_date>, parallel_billing_periods: <0 or 1>

## Capacity ledger
- available_billable_hours_per_month: <n>
- committed_hours_other_retainers: <n> + committed_hours_this_retainer: <n> = total_after_signing: <n, within available>

## Outcome review (6 months after start_date)
- scheduled_date: <YYYY-MM-DD>
- findings: null until held; then still_active_without_renegotiation, periods (paid_hours, actual_hours), effective_hourly_rate, action <none | re_scope | rate_increase | address_usage>
