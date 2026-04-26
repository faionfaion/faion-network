# FinOps Cloud Cost Optimization LLM Prompts

## Cost Analysis Prompts

### Analyze Cloud Bill

```
Analyze this cloud cost data and identify optimization opportunities:

[Paste cost breakdown data]

Please provide:
1. Top 5 cost drivers with percentage of total spend
2. Month-over-month trends and anomalies
3. Services with unusual growth patterns
4. Potential waste (idle resources, over-provisioning)
5. Quick win recommendations with estimated savings

Format as a structured report suitable for stakeholder review.
```

### Rightsizing Analysis

```
Analyze these instance utilization metrics for rightsizing opportunities:

Instance ID: [ID]
Instance Type: [current type]
vCPU: [count]
Memory: [GB]

Metrics (last 30 days):
- Avg CPU: [X]%
- Peak CPU: [X]%
- Avg Memory: [X]%
- Peak Memory: [X]%
- Network I/O: [pattern]

Please recommend:
1. Whether this instance should be rightsized (yes/no with confidence)
2. Recommended instance type if yes
3. Estimated monthly savings
4. Risk assessment (low/medium/high)
5. Any architectural changes to consider
```

### Spot Instance Feasibility

```
Evaluate this workload for Spot Instance migration:

Workload: [name]
Current instance type: [type]
Current monthly cost: $[amount]
Characteristics:
- Runtime pattern: [continuous/batch/scheduled]
- Statefulness: [stateful/stateless]
- Interruption tolerance: [high/medium/low]
- Current auto-scaling: [yes/no]
- Checkpointing capability: [yes/no/can implement]

Please provide:
1. Spot fitness score (1-10) with justification
2. Required architecture changes for Spot adoption
3. Recommended instance diversification strategy
4. Estimated savings potential
5. Implementation risks and mitigations
6. Step-by-step migration plan
```

---

## Reserved Instance Planning

### RI Purchase Recommendation

```
Based on this usage data, recommend a Reserved Instance strategy:

Current on-demand spend: $[amount]/month
Usage pattern (last 6 months):
[Paste instance usage data showing hours/month by instance type]

Constraints:
- Budget for upfront: $[amount]
- Risk tolerance: [conservative/moderate/aggressive]
- Provider: [AWS/GCP/Azure]
- Planning horizon: [1 year/3 years]

Please provide:
1. Recommended RI purchases by instance type and term
2. Standard vs Convertible RI split with rationale
3. Payment option recommendation (all upfront/partial/no upfront)
4. Expected savings calculation
5. Break-even analysis
6. Coverage percentage achieved
7. Residual on-demand for flexibility
```

### RI Utilization Optimization

```
Analyze this Reserved Instance portfolio for optimization:

Current RIs:
[List: Instance type, Quantity, Term remaining, Utilization %]

Current on-demand usage:
[List: Instance type, Average hours/month]

Please identify:
1. Underutilized RIs that should be sold or exchanged
2. Unused capacity that could be reallocated
3. On-demand usage that should be covered by new RIs
4. Expiring RIs and renewal recommendations
5. RI Marketplace selling opportunities
```

---

## Cost Allocation

### Tagging Strategy Design

```
Design a cost allocation tagging strategy for our organization:

Organization structure:
- Teams: [list teams]
- Environments: [prod, staging, dev, etc.]
- Products/services: [list]
- Cost centers: [list or describe structure]

Current state:
- Estimated untagged resources: [X]%
- Existing tags: [list any current tags]
- Compliance requirements: [PCI, HIPAA, etc.]

Please provide:
1. Recommended tag taxonomy (required and optional tags)
2. Tag naming conventions
3. Validation rules for each tag
4. Enforcement strategy (SCPs, policies)
5. Remediation workflow for untagged resources
6. Dashboard/reporting structure by tags
7. Implementation timeline
```

### Chargeback Model Design

```
Design a chargeback model for cloud costs:

Organization: [description]
Monthly cloud spend: $[amount]
Teams to charge: [list]
Shared services: [list services that are shared]

Requirements:
- [Any specific requirements]

Please provide:
1. Direct cost allocation method for team-owned resources
2. Shared cost allocation method (% split, usage-based, etc.)
3. Handling of untagged/unallocated costs
4. Suggested invoice format per team
5. Dispute resolution process
6. Governance model
```

---

## Waste Elimination

### Identify Idle Resources

```
Analyze this resource inventory for potential waste:

[Paste resource list with utilization metrics]

Categories to check:
- Unattached volumes
- Unused load balancers
- Idle instances (< 5% CPU for 7+ days)
- Orphaned snapshots
- Unused Elastic IPs
- Oversized databases

For each category, provide:
1. Count of wasteful resources
2. Monthly cost of waste
3. Confidence level (high/medium/low)
4. Recommended action (terminate/review/monitor)
5. Automation script or CLI command to clean up
```

### Non-Production Scheduling Strategy

```
Design a scheduling strategy for non-production environments:

Environments:
[List environments with current 24/7 costs]

Usage patterns:
- Development: [describe when used]
- Staging: [describe when used]
- QA: [describe when used]

Constraints:
- Timezone: [timezone]
- On-call requirements: [any]
- Exception process needed: [yes/no]

Please provide:
1. Recommended schedule per environment
2. Expected savings calculation
3. Implementation approach (Instance Scheduler, Lambda, etc.)
4. Exception handling for after-hours access
5. Monitoring and alerting setup
6. Sample schedule configuration
```

---

## AI/ML Cost Optimization

### ML Training Cost Analysis

```
Analyze this ML training workload for cost optimization:

Current setup:
- Instance type: [GPU instance]
- Training duration: [hours]
- Frequency: [daily/weekly/etc.]
- Monthly cost: $[amount]
- Checkpointing: [yes/no]
- Framework: [TensorFlow/PyTorch/etc.]

Model details:
- Model size: [parameters]
- Dataset size: [GB]
- Current GPU utilization: [%]

Please recommend:
1. Optimal GPU instance for this workload
2. Spot instance strategy with checkpointing design
3. Training optimization techniques (mixed precision, etc.)
4. Scheduling optimization (off-peak hours)
5. Expected cost reduction
6. Implementation steps
```

### Inference Cost Optimization

```
Optimize this ML inference deployment:

Current setup:
- Endpoint type: [instance type]
- Requests/day: [count]
- Avg latency: [ms]
- Monthly cost: $[amount]

Model characteristics:
- Model size: [MB/GB]
- Inference time: [ms]
- Memory requirement: [GB]

Please recommend:
1. Quantization strategy (INT8, FP16) with trade-offs
2. Caching opportunities for common queries
3. Batching strategy for throughput optimization
4. Auto-scaling configuration
5. GPU sharing options (multi-model endpoints)
6. Cost projection after optimizations
```

---

## Report Generation

### Executive Cost Summary

```
Generate an executive summary of cloud costs:

Data:
[Paste monthly cost data for last 3-6 months]

Include:
1. Key highlights (2-3 sentences)
2. Month-over-month and year-over-year trends
3. Top 3 cost optimization achievements
4. Top 3 concerns or areas needing attention
5. Forecast for next quarter
6. Strategic recommendations

Format for C-level audience (brief, business-focused, action-oriented).
```

### Team Cost Report

```
Generate a cost report for [Team Name]:

Period: [Month/Quarter]
Team's resources: [list or paste data]
Team's tags: [tag values to filter]

Include:
1. Total spend vs budget
2. Breakdown by service
3. Breakdown by environment (prod/non-prod)
4. Comparison to previous period
5. Anomalies or unusual charges
6. Optimization recommendations specific to this team
7. Action items with owners

Format as a concise report for engineering team leads.
```

---

## Automation Scripts

### Generate Cleanup Script

```
Generate a cleanup script for [AWS/GCP/Azure] to remove:

Resources to clean:
- Unattached EBS volumes older than [X] days
- Snapshots older than [X] days without tags
- Stopped instances for more than [X] days
- Unused Elastic IPs

Requirements:
- Dry-run mode first
- Logging of all actions
- Exclude resources with specific tags: [list]
- [Any other requirements]

Output:
1. Bash/Python script
2. IAM permissions required
3. Scheduling recommendation (cron/Lambda)
4. Rollback procedure
```

### Generate Cost Alert Lambda

```
Generate a Lambda function for cost anomaly detection:

Requirements:
- Check daily costs against baseline
- Alert if spend exceeds [X]% of average
- Alert if specific service exceeds $[X]
- Send alerts to [Slack/Email/PagerDuty]
- Include cost breakdown in alert

Output:
1. Lambda function code (Python)
2. IAM role policy
3. CloudWatch Event rule for scheduling
4. SNS topic configuration (if using SNS)
5. Deployment instructions
```

---

## Decision Support

### Build vs Buy for FinOps Tools

```
Evaluate build vs buy for FinOps tooling:

Current state:
- Cloud providers: [list]
- Monthly spend: $[amount]
- Team size for FinOps: [number]
- Current tools: [list]

Requirements:
- [List key requirements]

Budget for tooling: $[amount]/year

Please compare:
1. Native tools (AWS Cost Explorer, etc.)
2. Third-party tools (CloudHealth, Spot.io, nOps, etc.)
3. Open source options (Kubecost, OpenCost, etc.)
4. Custom build effort estimate

Provide recommendation with justification.
```

### Migration Cost Analysis

```
Analyze cost implications of this cloud migration:

Current state:
- Provider: [current]
- Monthly spend: $[amount]
- Services used: [list]

Proposed state:
- Provider: [target]
- Equivalent services: [mapping]

Please analyze:
1. Equivalent service mapping with pricing comparison
2. Migration costs (one-time)
3. Projected monthly costs post-migration
4. Break-even timeline
5. Hidden costs to consider (egress, training, etc.)
6. Risk factors
7. Recommendation (migrate/stay/hybrid)
```

---

## Prompt Engineering Tips

### For Better Cost Analysis

1. **Include context:** Provider, account structure, business constraints
2. **Provide data:** Actual numbers, not ranges
3. **Specify format:** Request specific output structure
4. **Set constraints:** Budget limits, risk tolerance, timeline

### For Actionable Recommendations

1. **Ask for specifics:** Instance types, not "rightsize"
2. **Request implementation steps:** Not just what, but how
3. **Include trade-offs:** Savings vs risk, effort vs impact
4. **Ask for validation:** How to verify the recommendation works

### For Automation

1. **Specify language:** Python, Bash, Terraform
2. **Include error handling:** What if API fails?
3. **Request dry-run mode:** Safe testing first
4. **Ask for logging:** Audit trail requirements

---

*Prompts should be customized with actual data for best results.*
