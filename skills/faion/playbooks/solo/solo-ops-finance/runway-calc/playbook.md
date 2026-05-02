---
name: runway-calc
description: Build a runway.md worksheet to compute months of cash left and set a hard revenue trigger.
tier: solo
group: solo-ops-finance
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a `runway.md` worksheet that tracks your monthly burn, emergency buffer, and current savings — and know exactly at which runway length to flip into consulting mode or raise revenue.

## Prerequisites

- A text editor or Obsidian vault for your `runway.md` file.
- Your last 3 months of bank/card statements (to calculate real average spend).
- A spreadsheet or calculator app for the arithmetic.
- Optional: a currency exchange rate if your costs and savings are in different currencies.

## Steps

1. Create the file `runway.md` in your project root or personal wiki.

2. List every **fixed monthly cost** in a table. Include everything that recurs regardless of whether you work:

   ```markdown
   | Category          | Monthly cost (€) |
   |-------------------|-----------------|
   | Rent / mortgage   | 900             |
   | Groceries + food  | 350             |
   | Health insurance  | 180             |
   | Transport + fuel  | 120             |
   | Software subs     | 95              |
   | Utilities         | 75              |
   | Phone + internet  | 40              |
   | Misc / personal   | 100             |
   | **Total burn**    | **1860**        |
   ```

3. Add a **variable buffer** (20% of fixed costs) for irregular expenses — car repair, vet bills, dentist. Round up:

   ```
   variable_buffer = 1860 × 0.20 = 372 → round to 400
   monthly_burn = 1860 + 400 = 2260
   ```

   > Real example used in this playbook: monthly_burn = **€2400** (slightly higher after rounding + subscriptions added during a product sprint).

4. Record your **one-time emergency buffer** — 1 month of burn kept untouched in a separate savings account. This is not runway; it is the floor:

   ```
   emergency_buffer = 2400
   ```

5. Record **spendable savings** — your current liquid savings minus the emergency buffer:

   ```
   total_savings  = 20400
   emergency_buf  = 2400
   spendable      = 20400 - 2400 = 18000
   ```

6. Compute **runway in months**:

   ```
   runway_months = spendable / monthly_burn
                 = 18000 / 2400
                 = 7.5 months
   ```

7. Set a **trigger threshold** in `runway.md`. The rule of thumb: at 4 months remaining, act before cash is gone:

   ```markdown
   ## Trigger

   When runway_months drops to **4.0**, immediately take one of:
   - Switch to 3-day-per-week consulting at ≥€400/day to cover burn.
   - Launch a paid waitlist or charge existing beta users.
   - Raise a pre-seed or friends-and-family round.
   ```

8. Update `runway.md` on the **1st of each month**: re-check your bank balance, adjust `spendable`, and recompute `runway_months`. Takes 5 minutes.

9. Add a **revenue projection** block once you have any paying users:

   ```markdown
   ## Revenue offset

   | Month     | MRR (€) | Net burn (€)  | Adjusted runway |
   |-----------|---------|---------------|-----------------|
   | 2026-05   | 0       | 2400          | 7.5 mo          |
   | 2026-06   | 480     | 1920          | recalculate     |
   | 2026-07   | 960     | 1440          | recalculate     |
   ```

   Net burn = monthly_burn − MRR. Recalculate runway_months using net burn.

## Verify

Open `runway.md` and confirm it contains all three values. Then validate the arithmetic:

```bash
python3 -c "
spendable = 18000
monthly_burn = 2400
runway = spendable / monthly_burn
print(f'runway_months = {runway}')
assert runway == 7.5, 'check your numbers'
print('OK')
"
```

Expected output: `runway_months = 7.5` followed by `OK`. If the assertion fails, your spendable/burn numbers do not match the worksheet.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Runway looks much longer than expected | Emergency buffer not subtracted from savings | Re-read Step 5: spendable = total_savings − emergency_buffer, never total_savings |
| Monthly burn keeps growing each month | Software subscriptions accumulate silently | Audit every recurring charge in your bank statement each month; cancel any sub unused for 30+ days |
| Trigger at 4 months arrives faster than expected | Variable costs ran higher than 20% buffer | Increase the variable buffer to 25–30% if you have irregular expenses like travel or equipment |
| Revenue offset makes runway feel safe too early | MRR is not yet recurring (one-time payments) | Only count confirmed, contractually recurring revenue in MRR; invoice-based income goes in a separate "one-time" line |

## Next

- `roadmap-for-one-person` — once runway is visible, use outcome-based roadmaps to sequence features against the trigger date.
- `pricing-experiments` — raise MRR by testing price points before you hit the 4-month trigger.
- `customer-onboarding-email` — convert free users to paid before the trigger forces a consulting pivot.

## References

- [knowledge/solo/product/product-operations/product-lifecycle](../../../knowledge/solo/product/product-operations/product-lifecycle) — defines the lifecycle stages from build to growth; the trigger threshold in Step 7 maps directly onto the transition from the build stage to the monetisation stage.
