# FinOps LLM Prompts

## Cost Analysis Prompts

### Analyze Cloud Billing Data

```
Analyze the following cloud billing data and provide:

1. Top 5 cost drivers by service
2. Unusual spending patterns or anomalies
3. Month-over-month trends
4. Potential optimization opportunities
5. Risk areas requiring attention

Data format: [CSV/JSON billing export]

Focus on actionable insights with estimated savings potential.
```

### Identify Waste in Infrastructure

```
Review this infrastructure configuration and identify waste:

[Paste Terraform/CloudFormation/resource list]

Look for:
1. Overprovisioned resources (CPU/memory utilization data: [paste if available])
2. Unused or orphaned resources
3. Suboptimal instance types
4. Missing commitment discounts opportunities
5. Storage that could be tiered or archived

For each finding, provide:
- Current cost estimate
- Recommended action
- Expected savings
- Risk level of change
```

### Generate Rightsizing Recommendations

```
Based on the following resource utilization metrics, generate rightsizing recommendations:

Resource: [resource-id]
Type: [current instance type]
Region: [region]

Metrics (last 30 days):
- CPU: avg [X]%, max [X]%, p95 [X]%
- Memory: avg [X]%, max [X]%, p95 [X]%
- Network: avg [X] Mbps, max [X] Mbps
- Disk IOPS: avg [X], max [X]

Requirements:
- Minimum performance headroom: 20%
- Cost optimization priority: [high/medium/low]
- Downtime tolerance: [none/maintenance-window/flexible]

Provide:
1. Recommended instance type
2. Cost comparison (current vs recommended)
3. Performance impact assessment
4. Migration steps
```

## Optimization Strategy Prompts

### Create FinOps Implementation Plan

```
Create a FinOps implementation plan for an organization with:

- Cloud provider(s): [AWS/GCP/Azure/multi-cloud]
- Current monthly spend: $[amount]
- Number of teams: [X]
- Current maturity: [crawl/walk/run]
- Main pain points: [list]

Provide a phased 6-month plan covering:

Phase 1 (Month 1-2): INFORM
- Visibility and tagging strategy
- Tool selection
- Baseline metrics

Phase 2 (Month 3-4): OPTIMIZE
- Quick wins
- Commitment strategy
- Rightsizing approach

Phase 3 (Month 5-6): OPERATE
- Governance policies
- Automation
- Cultural change

Include success metrics for each phase.
```

### Design Commitment Strategy

```
Design a commitment discount strategy based on:

Current usage (last 12 months):
- On-demand compute spend: $[X]/month
- Usage variability: [low/medium/high]
- Growth forecast: [X]% annually

Provider: [AWS/GCP/Azure]

Constraints:
- Maximum commitment term: [1/3] years
- Risk tolerance: [conservative/moderate/aggressive]
- Budget for upfront: $[X] or [none]

Provide:
1. Recommended commitment type (RI/Savings Plans/CUD)
2. Coverage target percentage
3. Commitment breakdown by service/region
4. Expected savings vs current spend
5. Flexibility considerations
6. Review cadence recommendation
```

### Develop AI/ML Cost Strategy

```
Develop a cost optimization strategy for AI/ML workloads:

Current state:
- Training workloads: [describe]
- Inference workloads: [describe]
- GPU types in use: [list]
- Monthly AI spend: $[amount]
- Provider: [AWS/GCP/Azure]

Requirements:
- Training frequency: [daily/weekly/monthly]
- Inference latency SLA: [Xms]
- Model size: [parameters]
- Batch vs real-time: [ratio]

Provide recommendations for:
1. Training cost optimization (spot, scheduling, checkpointing)
2. Inference cost optimization (caching, batching, quantization)
3. GPU selection and rightsizing
4. Cost allocation and tracking
5. Approval workflows for expensive experiments
```

## Reporting Prompts

### Generate Executive Cost Summary

```
Generate an executive summary of cloud costs for [month/quarter]:

Data:
[Paste cost data by service, team, environment]

Include:
1. One-paragraph executive summary
2. Key metrics table (total spend, vs budget, vs last period)
3. Top 3 highlights (positive or concerning)
4. Top 3 action items
5. Forecast for next period

Keep language business-focused, avoid technical jargon.
Maximum length: 1 page.
```

### Create Team Cost Report

```
Create a cost report for [team name]:

Period: [month]
Budget: $[amount]

Cost data:
[Paste team's resource costs]

Include:
1. Budget vs actual summary
2. Cost breakdown by service
3. Cost breakdown by environment
4. Week-over-week trend
5. Anomalies or concerns
6. Optimization opportunities specific to this team
7. Action items for the team

Format for engineers - include resource IDs where relevant.
```

### Document Optimization Decision

```
Document the following optimization decision in ADR format:

Decision: [e.g., "Migrate from RDS Multi-AZ to Aurora Serverless"]

Context:
- Current state: [describe]
- Problem: [describe cost issue]
- Options considered: [list]

Selected option: [choice]
Rationale: [why this option]

Expected outcome:
- Cost impact: [savings/increase]
- Performance impact: [better/same/worse]
- Risk level: [low/medium/high]

Create a concise ADR (Architecture Decision Record) for FinOps documentation.
```

## Automation Prompts

### Generate Cost Alert Rules

```
Generate cost alert rules for:

Environment: [prod/dev/all]
Provider: [AWS/GCP/Azure]
Monthly budget: $[amount]

Create alert rules for:
1. Forecast-based alerts (50%, 75%, 90% of budget)
2. Actual spend alerts (80%, 100%, 120% of budget)
3. Anomaly detection (>20% daily increase)
4. Service-specific alerts for top cost drivers

Output format: [Terraform/CloudFormation/JSON/YAML]

Include:
- Alert thresholds
- Notification channels
- Escalation logic
- Auto-remediation suggestions
```

### Create Scheduled Cleanup Script

```
Create a script to identify and clean up unused resources:

Provider: [AWS/GCP/Azure]
Resource types to check:
- [ ] Unattached volumes
- [ ] Unused elastic IPs
- [ ] Old snapshots (>X days)
- [ ] Stopped instances (>X days)
- [ ] Unused load balancers
- [ ] Empty S3 buckets

Requirements:
- Dry-run mode by default
- Generate report before deletion
- Respect tag exemptions (tag: "do-not-delete")
- Log all actions

Output: [Python/Bash/Go] script with comments.
```

### Design FinOps Dashboard

```
Design a FinOps dashboard for [Grafana/Looker/QuickSight]:

Data sources:
- Cloud billing export
- Resource utilization metrics
- Tag compliance data

Create dashboard specification with:

1. Executive Overview Panel
   - Total spend (current month)
   - Budget remaining
   - MoM trend
   - Waste percentage

2. Cost Breakdown Panel
   - By service (pie chart)
   - By team (bar chart)
   - By environment (stacked bar)

3. Optimization Metrics Panel
   - Commitment coverage
   - Rightsizing opportunities
   - Idle resources count

4. Trend Analysis Panel
   - 12-month spend history
   - Forecast vs actual
   - Unit cost trends

Provide:
- Panel specifications (queries, visualizations)
- Refresh intervals
- Alert thresholds
- Drill-down capabilities
```

## Troubleshooting Prompts

### Diagnose Cost Spike

```
Help diagnose a sudden cost increase:

Baseline: $[X]/day
Current: $[Y]/day (increase of [Z]%)
Start date of increase: [date]

Available data:
[Paste daily cost breakdown by service]

Changes around that time:
[List any known deployments, config changes]

Investigate:
1. Which service(s) caused the increase?
2. What specific resources are responsible?
3. Is this expected (scaling) or unexpected (waste/misconfiguration)?
4. Immediate actions to take
5. Prevention measures for the future
```

### Analyze Commitment Underutilization

```
Analyze Reserved Instance / Savings Plan underutilization:

Commitment details:
- Type: [RI/Savings Plan]
- Term: [1/3 years]
- Purchase date: [date]
- Monthly commitment: $[amount]
- Current utilization: [X]%

Usage data:
[Paste utilization metrics]

Provide:
1. Root cause of underutilization
2. Options to improve utilization
3. Cost of continuing current state
4. Recommendations (modify, exchange, sell, accept)
5. Prevention strategies for future purchases
```

## Best Practice Prompts

### Review Tagging Strategy

```
Review and improve this tagging strategy:

Current tags:
[Paste current tag schema]

Compliance rate: [X]%
Main issues: [list]

Requirements:
- Cost allocation accuracy: >95%
- Support for chargeback
- Environment identification
- Owner accountability

Provide:
1. Assessment of current strategy
2. Recommended tag schema
3. Enforcement approach
4. Migration plan for existing resources
5. Governance process
```

### Evaluate FinOps Tool

```
Evaluate [tool name] for our FinOps needs:

Current environment:
- Cloud providers: [list]
- Monthly spend: $[amount]
- Team size: [X]
- Current tools: [list]

Requirements:
- [ ] Multi-cloud support
- [ ] Real-time cost visibility
- [ ] Anomaly detection
- [ ] Rightsizing recommendations
- [ ] Budget management
- [ ] Chargeback/showback
- [ ] API access
- [ ] SSO integration

Provide:
1. Feature coverage assessment
2. Pricing analysis
3. Implementation complexity
4. Pros and cons
5. Comparison with alternatives
6. Recommendation with justification
```

---

*FinOps LLM Prompts | faion-cicd-engineer*
