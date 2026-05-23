<!-- purpose: Print-friendly 6-check Markdown for daily triage -->
<!-- consumes: ad-platform dashboard or API for spend/CPA/frequency/CTR/conversions/account-health -->
<!-- produces: 15-minute triage log following content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300 tokens when loaded -->

# Daily Ads Anomaly Checklist — `<DATE>`

Account: `<ACCOUNT_ID>` · Owner: `@<HANDLE>` · Started: `<HH:MM>`

## 1. Spend spike

- Threshold: spend > **1.5× 7-day rolling avg** per ad set
- Action if tripped (first day): `reduce-budget`, auto-resume next morning
- Action if persistent (2nd day): `escalate`

## 2. CPA spike

- Threshold: CPA > **1.5× 7-day rolling avg** per ad set
- Action: `pause` with auto_resume_at next morning

## 3. Frequency spike

- Threshold: frequency > **4.0** per ad set
- Action: `reduce-budget` + tag for creative refresh

## 4. CTR drop

- Threshold: CTR **-30%** vs 7-day avg
- Action: `reduce-budget` + tag for creative refresh

## 5. Conversion drop

- Threshold: conversions **-40%** vs 7-day avg
- Action: `escalate` (tracking suspected broken)

## 6. Account health

- Threshold: zero platform warnings
- Action if tripped: `escalate` immediately

---

## Log entry

Save as JSON per `templates/daily-run-log.json`. Run `scripts/validate-daily-ads-anomaly-checklist.py --file <log>.json` before publish.
