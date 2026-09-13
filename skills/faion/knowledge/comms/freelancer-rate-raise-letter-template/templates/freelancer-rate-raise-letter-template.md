<!-- purpose: rate-raise letter and artefact skeleton — same sections and field names as content/02-output-contract.xml -->
<!-- consumes: retainer contract (rate-change notice clause), engagement log since the current rate, trailing-12-month revenue by client, in-flight SOWs (AGENTS.md Prerequisites) -->
<!-- produces: a rate-raise artefact validating against scripts/validate-freelancer-rate-raise-letter-template.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~600 tokens once filled -->

# Rate Raise — <client_name>

## Inputs used

- Retainer contract, rate-change notice clause (`contract_notice_days`):
- Engagement log since the current rate was set:
- Trailing-12-month revenue by client:
- In-flight SOWs, accepted quotes, prepaid periods:

## Rate and schedule

- `current` → `new` (<current_rate> → <new_rate>), one number with currency and unit, `change_pct`:
- `letter_date`: <artefact_date> — `effective_date`: <effective_date> (longest of 30 days, one full billing cycle, contract notice period)
- `raises_in_last_12_months`: 0 — otherwise `scope_change_documented_at`:

## Justification (value deltas, each citing an `inputs_used` name)

| Kind | Statement (deliverable / metric before-after / scope added / capability depended on) | Input |
|------|-------------------------------------------------------------------------------------|-------|

- CPI or costs mentioned? Never as the sole justification.

## In-flight work (completes at the current rate)

| Reference | Kind (signed_sow / accepted_quote / prepaid_retainer_period) |
|-----------|--------------------------------------------------------------|

## Churn risk (before sending)

- `class`: stay | negotiate | churn — `revenue_share_pct_t12m`:
- Alternatives / recent feedback / payment behaviour / renewal date:
- Replacement revenue plan (required when churn and share > 30%): pipeline name, expected close date, monthly value

## Letter (under 250 words, business-notice shape)

Subject: Retainer rate from <effective_date>

(Opens with the value delivered.) (States the change: one number, old and new, percentage.) (States what is protected.) (Closes with the effective date and the follow-up date.)

— <owner_full_name>

- Banned phrases found: none — personal-cost narrative: no — concession in letter: no

## Prepared concession (follow-up only)

- One pre-decided concession:

## Follow-up (T+7)

- `date`: letter date + 7
- If confirmed: — If no reply: — If push-back:

## Acknowledgement

- Received in writing on: — response state: — new rate applied only after written confirmation.

## Validation

Run `python scripts/validate-freelancer-rate-raise-letter-template.py --file <path-to-filled-json>`. Exit 0 = valid, exit 1 = violations listed on stderr.
