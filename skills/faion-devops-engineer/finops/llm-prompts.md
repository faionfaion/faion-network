# FinOps LLM Prompts

AI-assisted prompts for cloud cost analysis and optimization.

## Cost Analysis Prompts

### Prompt 1: Cost Breakdown Analysis

```
Analyze the following cloud cost data and provide insights:

[PASTE COST DATA OR CSV]

Please analyze:
1. Top 5 cost drivers by service
2. Month-over-month trends
3. Unusual patterns or anomalies
4. Cost distribution by environment/team
5. Potential optimization opportunities

Format the response as a structured report with tables where appropriate.
```

### Prompt 2: Rightsizing Recommendations

```
Based on the following resource utilization metrics:

[PASTE UTILIZATION DATA]

Provide rightsizing recommendations:
1. Identify underutilized resources (CPU <20%, Memory <30%)
2. Suggest appropriate instance sizes
3. Calculate potential monthly savings
4. Rank recommendations by savings potential
5. Note any risks or considerations

Include a summary table with: Resource ID, Current Size, Recommended Size, Utilization, Monthly Savings.
```

### Prompt 3: Savings Plan Calculator

```
Calculate optimal Savings Plan commitment based on:

Current spend:
- On-Demand EC2: $[AMOUNT]/month
- Fargate: $[AMOUNT]/month
- Lambda: $[AMOUNT]/month

Usage patterns:
- Baseline (steady): [PERCENTAGE]%
- Variable: [PERCENTAGE]%
- Peak periods: [DESCRIPTION]

Constraints:
- Maximum commitment term: [1yr/3yr]
- Risk tolerance: [Low/Medium/High]

Provide recommendations for:
1. Compute Savings Plan vs EC2 Instance Savings Plan
2. Optimal commitment amount (hourly)
3. Expected utilization rate
4. Projected annual savings
5. Break-even analysis
```

## Tagging & Allocation Prompts

### Prompt 4: Tag Schema Design

```
Design a tagging strategy for a company with:

Organization structure:
- [DEPARTMENTS/TEAMS]

Cloud environment:
- Providers: [AWS/GCP/Azure/Multi-cloud]
- Workloads: [Production/Dev/Test/etc.]
- Compliance: [HIPAA/PCI/SOC2/etc.]

Requirements:
- Cost allocation by [CRITERIA]
- Chargeback to [TEAMS/PROJECTS]
- Compliance tracking needed: [YES/NO]

Provide:
1. Mandatory tags schema with descriptions
2. Optional tags for enhanced tracking
3. Tag naming conventions
4. Enforcement strategy
5. Sample values for each tag
```

### Prompt 5: Unallocated Cost Investigation

```
Help investigate unallocated cloud costs:

Current state:
- Total monthly spend: $[AMOUNT]
- Unallocated/untagged: $[AMOUNT] ([PERCENTAGE]%)

Known untaggable resources:
- [LIST IF KNOWN]

Questions:
1. What AWS/GCP/Azure resources commonly resist tagging?
2. How can we allocate costs for untaggable resources?
3. What allocation rules should we apply for shared services?
4. How do we handle data transfer costs?

Provide a strategy to reduce unallocated costs to <10%.
```

## Optimization Strategy Prompts

### Prompt 6: AI/ML Cost Optimization

```
Optimize AI/ML workload costs:

Current setup:
- Training jobs: [INSTANCE TYPES, FREQUENCY]
- Inference: [INSTANCE TYPES, LOAD]
- Data pipeline: [STORAGE, TRANSFER]
- Monthly spend: $[AMOUNT]

Constraints:
- SLA requirements: [LATENCY/AVAILABILITY]
- Training job duration: [HOURS/DAYS]

Provide optimization recommendations for:
1. Training cost reduction (spot instances, checkpointing)
2. Inference optimization (batching, caching, quantization)
3. Data storage optimization
4. GPU utilization improvements
5. Expected savings with implementation effort level
```

### Prompt 7: Kubernetes Cost Optimization

```
Analyze Kubernetes cluster costs:

Cluster details:
- Provider: [EKS/GKE/AKS]
- Node pools: [INSTANCE TYPES, COUNT]
- Namespaces: [LIST]
- Monthly cost: $[AMOUNT]

Utilization data:
[PASTE PROMETHEUS/OPENCOST METRICS]

Analyze:
1. Node utilization efficiency
2. Pod resource requests vs actual usage
3. Namespace cost allocation
4. Idle/over-provisioned workloads
5. Autoscaling opportunities

Recommend:
1. Node pool rightsizing
2. Pod resource limit adjustments
3. Cluster autoscaler configuration
4. Spot node pool opportunities
```

## Reporting & Communication Prompts

### Prompt 8: Executive Cost Summary

```
Create an executive summary from cost data:

Data:
[PASTE MONTHLY COST BREAKDOWN]

Audience: [C-Level/VP/Director]
Focus: [Cost reduction/Budget compliance/Forecast accuracy]

Generate:
1. One-paragraph executive summary
2. Key metrics dashboard (3-5 metrics)
3. Traffic light status for cost health
4. Top 3 actions needed
5. Risk/opportunity callouts

Keep technical jargon minimal. Focus on business impact.
```

### Prompt 9: Team Cost Communication

```
Draft a cost awareness message for engineering team:

Context:
- Team: [TEAM NAME]
- Current spend: $[AMOUNT]
- Budget: $[AMOUNT]
- Status: [Over/Under/On track]

Key issues:
- [ISSUE 1]
- [ISSUE 2]

Tone: [Collaborative/Urgent/Educational]

Create:
1. Email/Slack message explaining cost situation
2. Specific actions team can take
3. Resources for self-service cost checks
4. Deadline for action items
```

### Prompt 10: Anomaly Alert Response

```
Help investigate cost anomaly:

Alert details:
- Service: [SERVICE]
- Account: [ACCOUNT]
- Expected: $[AMOUNT]
- Actual: $[AMOUNT]
- Increase: [PERCENTAGE]%
- Time period: [START] to [END]

CloudTrail events:
[PASTE RELEVANT EVENTS]

Questions:
1. What likely caused this spike?
2. Is this expected or problematic?
3. What additional data should I gather?
4. How should I communicate this to stakeholders?
5. What preventive measures should we implement?
```

## Forecasting Prompts

### Prompt 11: Cost Forecast

```
Generate cost forecast based on:

Historical data (12 months):
[PASTE MONTHLY COST DATA]

Known changes:
- Planned launches: [DESCRIPTION, DATE]
- Team growth: [PERCENTAGE]
- New workloads: [DESCRIPTION]
- Decommissions: [DESCRIPTION]

Provide:
1. 3-month forecast with confidence intervals
2. 6-month forecast with assumptions
3. Key factors affecting forecast
4. Scenario analysis (best/expected/worst)
5. Budget recommendation for next quarter
```

### Prompt 12: What-If Analysis

```
Analyze cost impact of proposed changes:

Current baseline:
- Monthly spend: $[AMOUNT]
- Architecture: [DESCRIPTION]

Proposed changes:
[DESCRIBE CHANGES]

Questions:
1. What is the expected cost impact?
2. What are the cost risks?
3. Are there more cost-effective alternatives?
4. What's the break-even point?
5. What monitoring should we add?
```

## Tool Integration Prompts

### Prompt 13: FinOps Tool Selection

```
Help select FinOps tools for our organization:

Requirements:
- Cloud providers: [AWS/GCP/Azure/Multi-cloud]
- Monthly cloud spend: $[AMOUNT]
- Team size: [NUMBER]
- Key use cases: [LIST]
- Budget for tools: $[AMOUNT/year]

Current tools:
- [LIST EXISTING TOOLS]

Evaluate options:
1. Native cloud tools (pros/cons)
2. Third-party platforms (compare 3-5)
3. Open source alternatives
4. Implementation complexity
5. ROI expectations

Provide recommendation with justification.
```

### Prompt 14: Dashboard Design

```
Design a FinOps dashboard for:

Audience: [Engineering/Finance/Executive]
Cloud: [AWS/GCP/Azure]
Tool: [Grafana/Looker/DataStudio/PowerBI]

Key questions to answer:
- [QUESTION 1]
- [QUESTION 2]
- [QUESTION 3]

Include:
1. Dashboard layout with sections
2. Key metrics with formulas
3. Visualization types for each metric
4. Drill-down capabilities
5. Alert thresholds
6. Sample query/SQL for top metrics
```

## Best Practices Prompts

### Prompt 15: FinOps Maturity Assessment

```
Assess FinOps maturity based on:

Current practices:
- Visibility: [DESCRIPTION]
- Optimization: [DESCRIPTION]
- Operations: [DESCRIPTION]
- Culture: [DESCRIPTION]

Team structure:
- [WHO OWNS WHAT]

Tools:
- [CURRENT TOOLS]

Provide:
1. Current maturity level (Crawl/Walk/Run)
2. Gap analysis per FinOps capability
3. Priority improvements (quick wins vs strategic)
4. Recommended roadmap
5. Success metrics to track
```

### Prompt 16: FinOps Runbook Creation

```
Create a runbook for:

Process: [PROCESS NAME]
Example: Monthly cost review / Anomaly investigation / Rightsizing

Include:
1. Purpose and scope
2. Prerequisites and access needed
3. Step-by-step procedure
4. Decision trees for common scenarios
5. Escalation criteria
6. Metrics to track
7. Common issues and solutions

Format as a clear, actionable document for [ROLE].
```

## Usage Tips

### Effective Prompting

1. **Include context**: Provide actual numbers, not placeholders when possible
2. **Specify output format**: Tables, bullet points, narrative
3. **Set constraints**: Budget limits, timeline, compliance requirements
4. **Request reasoning**: Ask "why" along with "what"
5. **Iterate**: Follow up with clarifying questions

### Data Preparation

Before using prompts:
- Export relevant cost data (CSV/JSON)
- Gather utilization metrics
- Note any constraints or requirements
- Identify stakeholder concerns

### Privacy Considerations

When using external LLMs:
- Remove account IDs and identifiers
- Anonymize team/project names if sensitive
- Do not include credentials or secrets
- Consider using aggregated data

## Sources

- [FinOps Foundation](https://www.finops.org/)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)
- [Google Cloud Cost Management](https://cloud.google.com/cost-management)
- [Azure Cost Management](https://azure.microsoft.com/en-us/products/cost-management/)
