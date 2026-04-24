# DORA Metrics LLM Prompts

Effective prompts for analyzing, implementing, and improving DORA metrics.

---

## Analysis Prompts

### DORA Metrics Assessment

```
Analyze these DORA metrics for [TEAM/SERVICE] and provide recommendations:

Current metrics (last 30 days):
- Deployment Frequency: [N] deployments/week
- Lead Time for Changes: [N] hours (median)
- Change Failure Rate: [N]%
- Time to Restore Service: [N] minutes
- Reliability: [N]% availability

Industry benchmarks (Elite tier):
- Deployment Frequency: Multiple/day
- Lead Time: <1 hour
- Change Failure Rate: 0-15%
- MTTR: <1 hour
- Reliability: >99.9%

Provide:
1. Current performance tier for each metric
2. Gap analysis vs Elite tier
3. Root cause hypotheses for underperforming metrics
4. Prioritized improvement recommendations
5. Quick wins vs strategic initiatives
```

### Bottleneck Identification

```
Identify bottlenecks in our software delivery process based on these DORA metrics:

Metrics:
- Deployment Frequency: [N]/week (target: daily)
- Lead Time breakdown:
  - Commit to PR: [N] hours
  - PR review: [N] hours
  - Merge to deploy: [N] hours
- Change Failure Rate: [N]%
- MTTR: [N] hours

Team context:
- Team size: [N] engineers
- Services owned: [list]
- Tech stack: [stack]
- Current practices: [list practices]

Identify:
1. Which metric is the biggest constraint?
2. Where in the pipeline is the bottleneck?
3. Is this a people, process, or tooling issue?
4. Theory of constraints analysis
5. Recommended first improvement
```

### Trend Analysis

```
Analyze DORA metrics trends for [SERVICE] over the past [N] months:

Monthly data:
| Month | Deploy Freq | Lead Time | CFR | MTTR |
|-------|-------------|-----------|-----|------|
| Jan   | [N]         | [N]h      | [N]%| [N]m |
| Feb   | [N]         | [N]h      | [N]%| [N]m |
| Mar   | [N]         | [N]h      | [N]%| [N]m |

Events during this period:
- [Month]: [Event, e.g., "hired 2 engineers"]
- [Month]: [Event, e.g., "migrated to K8s"]

Analyze:
1. Overall trend direction for each metric
2. Correlation between metrics
3. Impact of events on metrics
4. Seasonal patterns
5. Forecast for next quarter
6. Risk areas to monitor
```

---

## Implementation Prompts

### DORA Metrics Setup

```
Help me implement DORA metrics tracking for our engineering team.

Current setup:
- Version control: [GitHub/GitLab/Bitbucket]
- CI/CD: [GitHub Actions/GitLab CI/Jenkins/etc.]
- Deployment target: [Kubernetes/AWS ECS/etc.]
- Incident management: [PagerDuty/Opsgenie/etc.]
- Monitoring: [Prometheus/Datadog/etc.]

Requirements:
1. Automated data collection (no manual entry)
2. Real-time dashboard
3. Weekly reports
4. Team/service breakdown

Provide:
1. Data collection strategy for each metric
2. Integration points and webhooks needed
3. Database schema for storing metrics
4. Dashboard design recommendations
5. Implementation phases
```

### Deployment Tracking Implementation

```
Design a deployment tracking system for DORA metrics.

Current state:
- Deployments happen via [method]
- [N] services deployed to production
- [N] deployments per day average
- Currently no automated tracking

Requirements:
- Track every production deployment
- Capture commit SHA, timestamp, deployer
- Associate with PRs and tickets
- Calculate lead time automatically
- Track deployment success/failure

Provide:
1. Event schema for deployment records
2. Collection mechanism (webhook, CI integration, etc.)
3. Code examples for common CI/CD platforms
4. Storage recommendations
5. Query patterns for metrics calculation
```

### Incident Correlation

```
Help me correlate incidents with deployments for Change Failure Rate calculation.

Current data:
- Deployments: Stored in [system] with fields [list]
- Incidents: Stored in [system] with fields [list]
- No direct linking between them

Challenges:
- Incidents don't always reference causing deployment
- Multiple services affected by single incident
- Some incidents not caused by deployments

Design:
1. Algorithm to associate incidents with deployments
2. Time window for correlation (recommend value)
3. Handling multi-service incidents
4. Excluding non-deployment incidents
5. Manual override mechanism
6. Confidence scoring for correlations
```

---

## Improvement Prompts

### Deployment Frequency Improvement

```
Help me improve deployment frequency from [current] to [target] per week.

Current state:
- Deployments per week: [N]
- Deployment process: [describe]
- Blockers identified: [list]
- Team size: [N]
- Services: [N]

Constraints:
- [Constraint 1, e.g., "manual QA required"]
- [Constraint 2, e.g., "change approval board"]

Provide:
1. Analysis of why frequency is low
2. Process changes to increase frequency
3. Tooling improvements needed
4. Risk mitigation for more frequent deploys
5. Phased implementation plan
6. Expected timeline to reach target
```

### Lead Time Reduction

```
Help me reduce lead time for changes from [current] hours to [target] hours.

Current pipeline breakdown:
- Code commit to PR creation: [N] hours
- PR waiting for review: [N] hours
- Review to approval: [N] hours
- Approval to merge: [N] hours
- Merge to build complete: [N] hours
- Build to production: [N] hours
- TOTAL: [N] hours

Bottleneck analysis:
- Longest stage: [stage]
- Most variable stage: [stage]

Team practices:
- PR size: [average lines]
- Review process: [describe]
- Test suite duration: [N] minutes
- Deployment process: [describe]

Provide:
1. Top 3 opportunities to reduce lead time
2. Specific actions for each opportunity
3. Expected impact of each action
4. Dependencies between actions
5. Metrics to track improvement
```

### Change Failure Rate Reduction

```
Help me reduce Change Failure Rate from [current]% to [target]%.

Current failure analysis:
- Total deployments: [N]
- Failed deployments: [N]
- Failure categories:
  - Build/deployment failures: [N]
  - Runtime errors post-deploy: [N]
  - Performance degradation: [N]
  - Rollbacks: [N]

Current practices:
- Test coverage: [N]%
- Staging environment: [yes/no]
- Canary deployments: [yes/no]
- Feature flags: [yes/no]
- Pre-deploy checks: [list]

Provide:
1. Root cause analysis of failures
2. Prevention strategies for each category
3. Detection improvements (faster identification)
4. Safe deployment patterns to implement
5. Rollback improvements
6. Prioritized action plan
```

### MTTR Improvement

```
Help me reduce Mean Time to Restore from [current] minutes to [target] minutes.

Current incident response:
- Time to detect (alert fires): [N] minutes
- Time to acknowledge: [N] minutes
- Time to diagnose: [N] minutes
- Time to mitigate: [N] minutes
- Time to resolve: [N] minutes

Current capabilities:
- Monitoring coverage: [describe]
- Alerting: [describe]
- On-call rotation: [yes/no]
- Runbooks: [N] documented
- Rollback capability: [describe]

Recent incidents:
| Incident | Severity | Detection | Resolution | Root Cause |
|----------|----------|-----------|------------|------------|
| [ID]     | [P1-P4]  | [N] min   | [N] min    | [cause]    |

Provide:
1. Breakdown of where time is spent
2. Detection improvements
3. Diagnosis improvements (observability)
4. Mitigation speedups (rollback, feature flags)
5. Prevention of recurring incidents
6. On-call and process improvements
```

### Reliability Improvement

```
Help me improve service reliability from [current]% to [target]% availability.

Current state:
- Availability (30-day): [N]%
- Error rate: [N]%
- P99 latency: [N]ms
- MTBF: [N] hours
- Main failure modes: [list]

Architecture:
- [Describe service architecture]
- Dependencies: [list]
- Single points of failure: [list]

SLOs defined:
- Availability: [target]%
- Latency P99: [target]ms
- Error rate: [target]%

Provide:
1. Gap analysis vs targets
2. Reliability risks identified
3. Architecture improvements needed
4. Operational improvements
5. Chaos engineering recommendations
6. SLO-based alerting strategy
```

---

## Reporting Prompts

### Executive Summary Generation

```
Generate an executive summary of DORA metrics for [PERIOD].

Raw data:
[Paste metrics data]

Requirements:
1. One-paragraph summary for executives
2. Key highlights (wins)
3. Key concerns (risks)
4. Trend direction
5. Comparison to industry benchmarks
6. Recommended focus areas

Format:
- Use business-friendly language (avoid jargon)
- Focus on outcomes, not technical details
- Highlight business impact
- Keep under 500 words
```

### Team Comparison Report

```
Compare DORA metrics across teams fairly and constructively.

Team metrics:
| Team | Deploy Freq | Lead Time | CFR | MTTR | Services |
|------|-------------|-----------|-----|------|----------|
| A    | [N]         | [N]h      | [N]%| [N]m | [N]      |
| B    | [N]         | [N]h      | [N]%| [N]m | [N]      |
| C    | [N]         | [N]h      | [N]%| [N]m | [N]      |

Context:
- Team A: [context, e.g., "legacy system"]
- Team B: [context, e.g., "greenfield project"]
- Team C: [context, e.g., "high-traffic service"]

Generate:
1. Fair comparison accounting for context
2. Strengths of each team
3. Learning opportunities between teams
4. Avoid punitive comparisons
5. Collaborative improvement suggestions
```

### Improvement Retrospective

```
Analyze the impact of our DORA improvement initiative.

Before initiative (baseline):
- Deployment Frequency: [N]/week
- Lead Time: [N] hours
- Change Failure Rate: [N]%
- MTTR: [N] minutes

After initiative ([N] months later):
- Deployment Frequency: [N]/week
- Lead Time: [N] hours
- Change Failure Rate: [N]%
- MTTR: [N] minutes

Changes implemented:
1. [Change 1]
2. [Change 2]
3. [Change 3]

Investment:
- [Resources/effort invested]

Generate:
1. Impact analysis for each metric
2. ROI calculation (if possible)
3. Which changes had the most impact
4. Unexpected outcomes
5. Lessons learned
6. Recommendations for next phase
```

---

## Tooling Prompts

### Tool Selection

```
Help me select DORA metrics tooling for our organization.

Requirements:
- Team size: [N] engineers
- Services: [N]
- Tech stack: [list]
- Budget: [range]
- Key requirements: [list]

Current tools:
- VCS: [tool]
- CI/CD: [tool]
- Monitoring: [tool]
- Incident management: [tool]

Evaluate these options:
1. Build custom (using existing tools)
2. Sleuth
3. LinearB
4. Jellyfish
5. Faros AI
6. Native GitHub/GitLab

For each option provide:
- Pros and cons
- Integration effort
- Total cost of ownership
- Time to value
- Recommendation
```

### Dashboard Design

```
Design a DORA metrics dashboard for [AUDIENCE].

Audience: [Executives / Engineering Managers / Team Leads / Engineers]

Requirements:
1. All five DORA metrics visible
2. Trend visualization
3. Team/service filtering
4. Comparison to benchmarks
5. Drill-down capability

Data available:
- Deployment events with [fields]
- Incident events with [fields]
- Commit/PR data with [fields]

Provide:
1. Dashboard layout (panels and placement)
2. Visualization types for each metric
3. Filtering and interactivity
4. Color coding (good/warning/bad thresholds)
5. Refresh frequency
6. Mobile considerations
```

---

## Quick Reference

| Task | Key Prompt Elements |
|------|---------------------|
| Assess metrics | Current values, targets, context |
| Find bottlenecks | Metric breakdown, pipeline stages |
| Improve metric | Current state, constraints, target |
| Generate report | Raw data, audience, format |
| Compare teams | Metrics, context for each team |
| Select tools | Requirements, budget, current stack |
| Design dashboard | Audience, data available, requirements |

---

## Prompt Engineering Tips

### Context Setting

```
You are a DevOps metrics expert helping with DORA metrics for a [COMPANY_SIZE] company.
Industry: [INDUSTRY]
Maturity: [low/medium/high DevOps maturity]
Constraints: [list any constraints]
```

### Data Presentation

```
Present data in tables when possible:
| Metric | Current | Target | Gap |
|--------|---------|--------|-----|

Include time periods:
- Last 30 days, Last 90 days, YoY comparison

Provide benchmarks:
- Elite: [value], High: [value], Medium: [value], Low: [value]
```

### Output Formatting

```
Format recommendations as:
1. Priority: [High/Medium/Low]
2. Action: [Specific action]
3. Expected impact: [Metric improvement]
4. Effort: [Low/Medium/High]
5. Dependencies: [List]
```

---

## Sources

- [DORA Metrics Four Keys](https://dora.dev/guides/dora-metrics-four-keys/)
- [Accelerate Book](https://itrevolution.com/product/accelerate/)
- [State of DevOps Reports](https://dora.dev/research/)
- [DORA Metrics Complete Guide | DX](https://getdx.com/blog/dora-metrics/)
