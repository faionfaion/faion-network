# Sample Size Quick Reference

Sample size per variant at 95% confidence, 80% power.

| Baseline | 5% Relative MDE | 10% Relative MDE | 20% Relative MDE |
|----------|-----------------|------------------|------------------|
| 1%       | 314,000         | 78,500           | 19,600           |
| 2%       | 156,000         | 39,000           | 9,800            |
| 5%       | 61,500          | 15,400           | 3,850            |
| 10%      | 28,800          | 7,200            | 1,800            |
| 20%      | 12,800          | 3,200            | 800              |
| 50%      | 3,200           | 800              | 200              |

MDE = Minimum Detectable Effect (relative to baseline).
Example: baseline=5%, 10% relative MDE = detecting a lift from 5.0% to 5.5%.

## Simplified formula

```
n per variant = 16 * p * (1 - p) / MDE_absolute^2
```

Where MDE_absolute = baseline * MDE_relative.
