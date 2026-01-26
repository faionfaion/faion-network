# FinOps LLM Prompts

Prompts for cloud cost analysis, optimization recommendations, and FinOps workflows.

---

## 1. Cost Analysis Prompts

### Analyze Monthly Cloud Bill

```
Analyze this cloud bill data and identify optimization opportunities:

Provider: {AWS/Azure/GCP}
Monthly Spend: ${amount}
Period: {month/year}

Top services by cost:
{service_breakdown}

Usage patterns:
{usage_data}

Please provide:
1. Cost breakdown analysis
2. Anomalies or unusual spending
3. Top 5 optimization opportunities with estimated savings
4. Recommended actions prioritized by impact vs effort
5. Questions to investigate further
```

### Compare Month-over-Month Costs

```
Compare these two months of cloud spending and explain the changes:

Previous Month ({month}):
- Total: ${amount}
- By service: {breakdown}

Current Month ({month}):
- Total: ${amount}
- By service: {breakdown}

Please provide:
1. Overall change analysis (% increase/decrease)
2. Services with significant changes (>10%)
3. Likely causes for each major change
4. Whether changes are expected vs concerning
5. Recommended actions if costs increased unexpectedly
```

### Analyze Cost Allocation

```
Review this cost allocation report and identify issues:

Allocation summary:
- Allocated costs: ${amount} ({percentage}%)
- Unallocated costs: ${amount} ({percentage}%)

By cost center:
{cost_center_breakdown}

Tag compliance:
{tag_compliance_data}

Please identify:
1. Allocation coverage gaps
2. Cost centers with unusual spending
3. Tagging compliance issues
4. Recommendations for improving allocation accuracy
5. Suggested new tags or allocation dimensions
```

---

## 2. Rightsizing Prompts

### Analyze Instance Utilization

```
Analyze these EC2/VM instances and provide rightsizing recommendations:

Instance data:
| Instance ID | Type | vCPUs | Memory | Avg CPU % | Avg Mem % | Peak CPU % | Peak Mem % | Monthly Cost |
{instance_table}

Consider:
- Minimum 20% headroom for peaks
- Instance family alternatives (compute, memory, general)
- ARM-based options where applicable

Provide:
1. Instances that should be downsized
2. Instances that should use different families
3. Estimated savings for each recommendation
4. Migration risks and considerations
5. Priority order for implementation
```

### Analyze Database Rightsizing

```
Review these database instances for rightsizing opportunities:

Database instances:
| Instance | Engine | Type | Storage | Avg CPU % | Avg Connections | IOPS Avg | Monthly Cost |
{database_table}

Consider:
- Read replicas vs larger instances
- Reserved capacity options
- Storage type optimization (SSD vs magnetic, provisioned vs autoscaling)

Provide:
1. Oversized instances with recommendations
2. Storage optimization opportunities
3. Architecture improvements (read replicas, caching)
4. Estimated savings
5. Migration approach and risks
```

---

## 3. Commitment Optimization Prompts

### Savings Plans Recommendation

```
Analyze this usage data and recommend Savings Plans commitments:

Current state:
- Monthly On-Demand compute spend: ${amount}
- Existing Savings Plans: {current_commitments}
- Current coverage: {percentage}%

Usage pattern (last 6 months):
| Month | Total Compute | Min Daily | Max Daily | Avg Daily |
{usage_table}

Service breakdown:
{service_breakdown}

Recommend:
1. Optimal hourly commitment amount
2. Compute SP vs EC2 Instance SP split
3. 1-year vs 3-year term recommendation
4. Expected savings and break-even analysis
5. Ramp-up strategy (if starting fresh)
6. Risk assessment
```

### Reserved Instance Analysis

```
Analyze RI utilization and provide recommendations:

Current RIs:
| Instance Family | Count | Term Remaining | Utilization % | Monthly Value |
{ri_table}

Usage data:
| Instance Family | On-Demand Hours | Avg Instances | Min Instances | Max Instances |
{usage_table}

Provide:
1. Underutilized RIs (action: exchange, sell, modify)
2. Candidates for new RI purchases
3. Standard vs Convertible recommendation
4. 1-year vs 3-year analysis
5. Expected savings impact
6. Expiring RIs strategy
```

### Spot Instance Strategy

```
Develop a Spot instance strategy for these workloads:

Workloads:
| Workload | Current Type | Instances | Interruption Tolerance | State | Monthly Cost |
{workload_table}

Requirements:
- Maximum acceptable interruption rate: {percentage}%
- Availability requirements: {description}

Provide:
1. Workloads suitable for Spot
2. Recommended Spot configuration (pools, diversification)
3. Fallback strategy (On-Demand, multiple instance types)
4. Interruption handling approach
5. Expected savings
6. Implementation priority
```

---

## 4. Tagging Strategy Prompts

### Design Tagging Policy

```
Design a tagging policy for this organization:

Organization details:
- Industry: {industry}
- Cloud providers: {providers}
- Teams: {team_structure}
- Cost allocation needs: {requirements}
- Compliance requirements: {compliance}

Current state:
- Existing tags: {current_tags}
- Tag compliance: {percentage}%
- Pain points: {issues}

Provide:
1. Mandatory tag schema with validation rules
2. Optional/recommended tags
3. Tag naming conventions
4. Enforcement strategy per provider
5. Migration plan for existing resources
6. Governance and maintenance process
```

### Improve Tag Compliance

```
Create a plan to improve tag compliance:

Current state:
- Overall compliance: {percentage}%
- By provider:
  - AWS: {percentage}%
  - Azure: {percentage}%
  - GCP: {percentage}%

Compliance by tag:
| Tag | Required | Compliance % | Top Violators |
{tag_compliance_table}

Top untagged resources:
{untagged_resources}

Provide:
1. Root cause analysis for low compliance
2. Quick wins (bulk tagging, automation)
3. Enforcement mechanisms to implement
4. Communication plan for teams
5. Metrics and targets with timeline
6. Escalation process for non-compliance
```

---

## 5. Anomaly Investigation Prompts

### Investigate Cost Spike

```
Investigate this cost anomaly:

Anomaly details:
- Date: {date}
- Service: {service}
- Account: {account}
- Expected cost: ${expected}
- Actual cost: ${actual}
- Variance: {percentage}%

Recent changes:
{cloudtrail_or_activity_log}

Resource inventory changes:
{resource_changes}

Please:
1. Identify likely root cause
2. Determine if legitimate or concerning
3. Calculate total impact
4. Recommend immediate actions
5. Suggest preventive measures
6. Provide investigation checklist if more info needed
```

### Analyze Data Transfer Costs

```
Analyze these data transfer costs and identify optimization opportunities:

Data transfer breakdown:
| Type | Source | Destination | GB/Month | Cost |
{transfer_table}

Architecture:
{architecture_description}

Provide:
1. Largest cost drivers
2. Potentially unnecessary transfers
3. Architecture changes to reduce costs
4. CDN/caching opportunities
5. VPC/networking optimizations
6. Estimated savings for each recommendation
```

---

## 6. Report Generation Prompts

### Generate Executive Summary

```
Generate an executive summary from this FinOps data:

Period: {month/quarter}

Spending:
- Total: ${amount}
- vs Budget: {percentage}%
- vs Previous period: {percentage}%

Key metrics:
- Tag compliance: {percentage}%
- Commitment coverage: {percentage}%
- Waste identified: ${amount}

Top initiatives:
{initiatives_and_status}

Format as:
1. One-paragraph executive summary
2. Key metrics dashboard (table)
3. Wins this period (bullets)
4. Risks and concerns (bullets)
5. Recommended actions for leadership
6. Forecast for next period
```

### Create Team Cost Report

```
Create a team-specific cost report:

Team: {team_name}
Period: {month}

Spending by service:
{service_breakdown}

Spending by environment:
{environment_breakdown}

Compared to:
- Budget: {percentage}%
- Previous month: {percentage}%
- Team average: {percentage}%

Top resources:
{top_resources}

Format as:
1. Summary (2-3 sentences)
2. Cost breakdown table
3. Month-over-month trends
4. Optimization opportunities specific to this team
5. Action items with owners
6. Upcoming changes that may affect costs
```

---

## 7. Automation Prompts

### Generate Cost Optimization Script

```
Generate a script to identify and remediate this cost issue:

Issue: {description}
Provider: {AWS/Azure/GCP}
Resources affected: {resource_types}

Requirements:
- Language: {Python/Bash/Terraform}
- Dry-run mode required
- Logging to {destination}
- Notification via {Slack/email/PagerDuty}

Current approach (if any):
{current_process}

Generate:
1. Script with full comments
2. Required IAM permissions
3. Scheduling recommendation (cron/Lambda/Cloud Functions)
4. Testing approach
5. Rollback procedure
```

### Design Budget Alert Workflow

```
Design an automated budget alert and response workflow:

Requirements:
- Alert thresholds: 50%, 75%, 90%, 100%
- Notification channels: {channels}
- Escalation path: {path}
- Auto-remediation for: {scenarios}

Current infrastructure:
- Cloud providers: {providers}
- IaC tool: {Terraform/Pulumi/CloudFormation}
- Monitoring: {tools}

Provide:
1. Alert configuration (IaC code)
2. Notification workflow
3. Auto-remediation scripts for safe actions
4. Escalation logic
5. Dashboard/visibility requirements
6. Testing and validation approach
```

---

## 8. Strategic Planning Prompts

### FinOps Maturity Assessment

```
Assess FinOps maturity based on these inputs:

Current capabilities:
- Cost visibility: {description}
- Cost allocation: {description}
- Optimization: {description}
- Forecasting: {description}
- Governance: {description}

Team structure:
{team_description}

Tools in use:
{tools_list}

Pain points:
{pain_points}

Assess against FinOps Foundation maturity model:
1. Current maturity level (Crawl/Walk/Run) by capability
2. Gaps and improvement areas
3. Recommended next steps (prioritized)
4. Resource requirements
5. Expected timeline to next maturity level
6. Quick wins vs long-term investments
```

### Cloud Cost Forecasting

```
Create a cloud cost forecast:

Historical data:
| Month | Spend | Key Drivers |
{historical_table}

Known upcoming changes:
{planned_changes}

Business context:
- Growth rate: {percentage}%
- New products/features: {description}
- Migrations: {description}

Provide:
1. 3-month forecast with confidence intervals
2. 12-month forecast with assumptions
3. Key variables affecting forecast
4. Scenarios (optimistic, baseline, pessimistic)
5. Recommended budget with buffer
6. Cost optimization targets to hit budget
```

---

## Usage Tips

### Prompt Engineering Best Practices

1. **Provide context**: Include cloud provider, scale, industry
2. **Include data**: Tables with actual numbers improve accuracy
3. **Specify format**: Request tables, bullets, or specific structures
4. **Set constraints**: Mention compliance, security, or business requirements
5. **Ask for reasoning**: Request explanations, not just recommendations

### Enhancing Prompts

Add these modifiers for better results:

```
Additional context:
- Risk tolerance: {Low/Medium/High}
- Team expertise: {Junior/Mid/Senior}
- Change velocity: {Slow/Medium/Fast}
- Compliance: {SOC2/HIPAA/PCI/None}
```

### Iterative Analysis

Use follow-up prompts:

```
Based on the previous analysis:
1. Drill deeper into {specific_area}
2. Consider this constraint: {new_constraint}
3. Compare with industry benchmarks
4. Provide implementation details for recommendation #{number}
```

---

## Sources

- [FinOps Foundation](https://www.finops.org/)
- [AWS Cost Optimization](https://aws.amazon.com/aws-cost-management/)
- [Azure Cost Management](https://azure.microsoft.com/en-us/products/cost-management)
- [GCP Cost Management](https://cloud.google.com/cost-management)
- [CloudZero](https://www.cloudzero.com/)
- [Vantage](https://www.vantage.sh/)
