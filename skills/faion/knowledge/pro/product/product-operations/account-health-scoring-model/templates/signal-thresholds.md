<!-- purpose: Fixed cutoffs for each 0/1/2 score per signal -->
<!-- consumes: operating data -->
<!-- produces: thresholds reference for compute-account-health.py -->
<!-- depends-on: none -->
<!-- token-budget-impact: low -->

# Signal Thresholds (locked — no per-account overrides)

| Signal          | 0 (red)                  | 1 (yellow)               | 2 (green)                |
|-----------------|--------------------------|--------------------------|--------------------------|
| Utilization     | <50% or >150% retainer   | 50-69% or 131-150%       | 70-130%                  |
| DM engagement   | 0 contacts / 4 weeks     | 1 contact / 4 weeks      | 2+ contacts / 4 weeks    |
| Scope-creep     | >25% over SOW            | 10-25% over              | <=10% over               |
| Payment         | >30d late                | 7-30d late               | <=7d late                |
| Advocacy        | none                     | 1 referral / 6mo         | 2+ referrals / 6mo       |
| Sponsor         | resigned / lost          | reorged                  | stable                   |

## Tier cutoffs (fixed)

- green: 10-12
- yellow: 5-9
- red: 0-4
