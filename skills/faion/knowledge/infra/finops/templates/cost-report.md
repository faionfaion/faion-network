# Monthly Cloud Cost Report — [MONTH YEAR]

## Summary

| Metric | Value |
|--------|-------|
| Total spend | $X,XXX |
| vs last month | +X% / -X% |
| vs budget | X% of $X,XXX |
| Largest cost driver | [service/team] |

## Cost by Team

| Team | Service | Cost | vs Last Month | % of Total |
|------|---------|------|---------------|------------|
| [Team A] | EC2 | $X,XXX | +X% | X% |
| [Team B] | RDS | $X,XXX | -X% | X% |
| [Team C] | S3 | $X,XXX | +X% | X% |

## Waste Identified

| Resource | Type | Avg CPU/Mem | Monthly Cost | Action |
|----------|------|-------------|--------------|--------|
| i-xxxxx | EC2 | 2% CPU | $XXX | Schedule stop or terminate |
| db-xxxxx | RDS | 5% CPU | $XXX | Downsize to t3.small |

## Optimization Opportunities

| Action | Estimated Savings | Effort |
|--------|-------------------|--------|
| Convert baseline EC2 to 1-year Compute SP | $X,XXX/mo | Low |
| S3 lifecycle: move logs to Glacier at 90d | $XXX/mo | Low |
| Rightsize 5 idle EC2 instances | $XXX/mo | Medium |

## Next Steps

- [ ] Owner: assign idle resources above to team leads by [DATE]
- [ ] Finance: review Savings Plan purchase for $[AMOUNT] commitment
- [ ] Engineering: implement S3 lifecycle policy for [bucket names]
