---
name: capacity-planning
description: Build a capacity.csv to track engineer utilization, identify under/over-load, and make data-driven hire-or-sell decisions before burnout or bench time hits margin.
tier: pro
group: delivery-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a `capacity.csv` tracking each engineer's target utilization (75%), billable rate, and monthly allocation pulled from Harvest or Toggl. You will know who is over-utilized (>85% for 3+ months) and who is under-utilized (<60%), and you will have a documented decision rule to act on each signal — hire, sell more work, or invest in training.

## Prerequisites

- Harvest or Toggl account with at least 2 months of tracked billable hours per engineer.
- Engineer list with agreed billable rate ($/h) and contracted monthly hours (160 h standard).
- Spreadsheet tool: Google Sheets, Excel, or `pandas` in a Python script.
- Access to project pipeline (CRM or Notion board) to cross-check upcoming sold work.
- Familiarity with [solo/solo-ops-finance/runway-calc](../../../solo/solo-ops-finance/runway-calc) — margin floor assumptions carry over.

## Steps

1. Export last 3 months of time entries from Harvest (`Reports → Detailed → Export CSV`) or Toggl (`Reports → Detailed → Export`). Save as `raw-time.csv`.

2. Create `capacity.csv` with one row per engineer and these columns:

   ```
   name,rate_usd,monthly_hours,month,billable_h,utilization_pct,billable_revenue
   ```

   Example header row followed by one engineer for one month:

   ```
   Alice Kim,150,160,2026-03,128,80.0,19200
   ```

3. Populate `billable_h` from the exported CSV by summing hours where `billable = true` (Harvest) or `Billable = Yes` (Toggl) per person per calendar month.

4. Calculate `utilization_pct = billable_h / monthly_hours * 100`. Target is 75% (120 h/month). Leave capacity buffer for onboarding, internal meetings, and sick days.

5. Calculate `billable_revenue = billable_h * rate_usd`.

6. Add a summary section at the bottom of the spreadsheet (or a separate `summary.csv`) with a 3-month rolling average for each engineer:

   ```
   name,avg_utilization_3m,signal
   Alice Kim,80.0,ok
   Ben Osei,91.5,OVER — hire check
   Cleo Vargas,58.0,UNDER — sell/train
   ```

7. Apply the decision rule to the `signal` column:

   | Condition | Signal | Action |
   |-----------|--------|--------|
   | avg ≥ 85% for 3 consecutive months | OVER | Open job req or outsource one workstream |
   | avg < 60% for 2+ months | UNDER | Pipeline push (sell) or skill-up for higher-value work |
   | 60% ≤ avg < 85% | ok | No action; monitor next month |

8. Pull your pipeline CRM (HubSpot, Notion, or a deal sheet) and add a `sold_h_next30d` column — hours of committed work per engineer in the next 30 days. If `sold_h_next30d / monthly_hours` already predicts utilization >85%, treat it as OVER now and start the hire conversation before the work starts.

9. Review the filled `capacity.csv` in your weekly ops meeting. Update monthly — do not let data age more than 6 weeks or the signals become noise.

### Worked example: 5-person agency (May 2026)

```
name,rate_usd,monthly_hours,month,billable_h,utilization_pct,billable_revenue
Alice Kim,150,160,2026-03,128,80.0,19200
Alice Kim,150,160,2026-04,136,85.0,20400
Alice Kim,150,160,2026-05,140,87.5,21000
Ben Osei,120,160,2026-03,100,62.5,12000
Ben Osei,120,160,2026-04,95,59.4,11400
Ben Osei,120,160,2026-05,88,55.0,10560
Cleo Vargas,150,160,2026-03,124,77.5,18600
Cleo Vargas,150,160,2026-04,130,81.3,19500
Cleo Vargas,150,160,2026-05,132,82.5,19800
Dmitri Shaw,130,160,2026-03,145,90.6,18850
Dmitri Shaw,130,160,2026-04,148,92.5,19240
Dmitri Shaw,130,160,2026-05,150,93.8,19500
Eva Santos,130,160,2026-03,108,67.5,14040
Eva Santos,130,160,2026-04,115,71.9,14950
Eva Santos,130,160,2026-05,118,73.8,15340
```

Summary (3-month rolling averages):

```
Alice Kim:   avg 84.2% → approaching OVER threshold — open prospective JD now
Ben Osei:    avg 58.9% → UNDER — 1:1 to review pipeline; pitch a new service package
Cleo Vargas: avg 80.4% → ok
Dmitri Shaw: avg 92.3% → OVER — immediate hire or offload one retainer
Eva Santos:  avg 71.1% → ok
```

Revenue from these 5 for 3 months = $262,380. At 80% avg utilization, theoretical max without adding headcount ≈ $288,000 (15 months equivalent). Dmitri alone leaves ~$9,600/month on the table from over-billing risk (overtime, quality dip, churn).

## Verify

Open `capacity.csv` and run this check (Python):

```bash
python3 - <<'EOF'
import csv, sys
errors = []
with open("capacity.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        util = float(row["utilization_pct"])
        expected = round(float(row["billable_h"]) / float(row["monthly_hours"]) * 100, 1)
        if abs(util - expected) > 0.2:
            errors.append(f"{row['name']} {row['month']}: util {util} != {expected}")
if errors:
    print("ERRORS:", errors); sys.exit(1)
print("capacity.csv OK — all utilization figures consistent")
EOF
```

Exits 0 if every `utilization_pct` cell matches `billable_h / monthly_hours * 100` within 0.2%.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Harvest export missing entries for a person | Time entries logged under a different project role or client | In Harvest Reports, check "All team members" and remove any active person filter before exporting |
| utilization >100% | Overtime was logged; `billable_h` exceeds `monthly_hours` | Cap `monthly_hours` at actual contracted hours, not 160, for part-time engineers; add an `employment_pct` column |
| UNDER signal on a new hire (<2 months) | Onboarding is unbillable by design | Add `onboarding=true` flag for first 6 weeks; exclude from signal calculation |
| Two engineers with same name in Toggl export | Toggl uses display names, not IDs | Add `toggl_user_id` as a secondary key; deduplicate on that |
| avg utilization looks fine but revenue is flat | Rate is stale — engineer seniority increased, rate was never updated | Audit `rate_usd` column against current contracts every quarter |

## Next

- [pro/delivery-ops/project-margin-tracker](../project-margin-tracker/playbook.md) — pair capacity data with project-level margin to find which clients absorb the most engineer hours per dollar billed.
- [pro/team-management/first-hire-developer](../team-management/first-hire-developer/playbook.md) — once the OVER signal is confirmed for 3 months, use this playbook to structure the hire.
- Review `knowledge/pro/pm/project-manager/resource-management` leveling options (delay/split/add/cut) when two engineers hit OVER in the same month.

## References

- [knowledge/pro/pm/project-manager/resource-management](../../../knowledge/pro/pm/project-manager/resource-management) — defines 75-80% effective capacity cap and overload leveling options (delay/split/add/cut) that back the 75% target utilization and the hire-or-sell decision thresholds in Steps 4 and 7.
- [knowledge/pro/pm/project-manager/cost-estimation](../../../knowledge/pro/pm/project-manager/cost-estimation) — bottom-up cost baseline methodology; the `billable_revenue` column in capacity.csv feeds directly into project cost baseline reconciliation and margin variance tracking.
- [knowledge/pro/pm/project-manager/team-development](../../../knowledge/pro/pm/project-manager/team-development) — Tuckman-stage context for interpreting UNDER signals: a new hire in Forming/Storming will show low utilization for 4-8 weeks; this is normal and should not trigger a sell/train decision prematurely.
