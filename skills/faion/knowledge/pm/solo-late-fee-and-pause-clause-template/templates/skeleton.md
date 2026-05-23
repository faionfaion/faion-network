<!-- purpose: LateFeeClauseSpec skeleton with tiered fee + pause right + re-engagement fee -->
<!-- consumes: jurisdiction lawyer review + base SOW template -->
<!-- produces: scaffold consumed by fill-clause step -->
<!-- depends-on: content/01-core-rules.xml#r5-jurisdiction-review -->
<!-- token-budget-impact: ~160 tokens -->

# Late-Fee & Pause Clause — [jurisdiction]

**Owner:** [freelancer role] / [person]
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Schedule (tiered)

| after_days | rate_pct_per_month |
|------------|--------------------|
| 14 | 1.5 |
| 30 | 3.0 |
| 60 | 5.0 |

## Pause right

- pause_days: 14 (hard minimum)
- notice_period_business_days: 5

## Re-engagement fee

- re_engagement_fee_usd: 500 (covers context-switch + admin)

## Jurisdiction review

- reviewed_by: counsel-handle
- reviewed_at: YYYY-MM-DD (annual refresh)
- memo_link: drive://legal/...

## Clause text (paste into SOW)

> Late payment fees: invoices unpaid beyond 14 days accrue a 1.5%/month fee.
> After 30 days, 3.0%/month. After 60 days, 5.0%/month.
> Pause right: Vendor may suspend work after 14 days unpaid with 5-business-day notice.
> Re-engagement: $500 paid in advance to resume work after pause.
> Applies to invoices issued on or after [effective date].
