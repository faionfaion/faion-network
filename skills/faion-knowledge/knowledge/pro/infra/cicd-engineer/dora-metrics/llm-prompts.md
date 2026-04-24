# DORA Metrics LLM Prompts

## Analysis Prompts

### Analyze Current DORA Performance

```
Analyze the following DORA metrics data and provide actionable recommendations:

Service: {service_name}
Period: {start_date} to {end_date}

Metrics:
- Deployment Frequency: {df_value} per {df_unit}
- Lead Time for Changes: {lt_value} {lt_unit}
- Change Failure Rate: {cfr_value}%
- Mean Time to Restore: {mttr_value} {mttr_unit}

Current CI/CD Stack:
- Source Control: {git_platform}
- CI/CD: {cicd_tool}
- Deployment: {deployment_method}
- Monitoring: {monitoring_tools}

Tasks:
1. Rate each metric (Elite/High/Medium/Low) based on DORA benchmarks
2. Identify the weakest metric and root cause hypotheses
3. Provide 3-5 specific, actionable recommendations prioritized by impact
4. Suggest quick wins (implementable within 1 sprint)
5. Recommend metrics to track improvement

Output format: Structured markdown with clear sections.
```

### Identify Bottlenecks

```
Given the following deployment pipeline data, identify DORA metric bottlenecks:

Pipeline Stages (average duration):
{stage_data}

Recent Deployments (last 30 days):
- Total: {total_deployments}
- Successful: {successful_deployments}
- Rolled back: {rollback_count}
- Hotfixes: {hotfix_count}

Recent Incidents:
{incident_summary}

Analyze:
1. Which pipeline stage contributes most to lead time?
2. What patterns correlate with deployment failures?
3. What factors contribute to MTTR?
4. Where should optimization efforts focus first?

Provide specific technical recommendations for each bottleneck.
```

### Compare Team Performance

```
Compare DORA metrics across teams and identify improvement opportunities:

Team A ({team_a_name}):
- Deployment Frequency: {team_a_df}
- Lead Time: {team_a_lt}
- Change Failure Rate: {team_a_cfr}
- MTTR: {team_a_mttr}

Team B ({team_b_name}):
- Deployment Frequency: {team_b_df}
- Lead Time: {team_b_lt}
- Change Failure Rate: {team_b_cfr}
- MTTR: {team_b_mttr}

Context:
- Team A tech stack: {team_a_stack}
- Team B tech stack: {team_b_stack}
- Both teams use: {shared_tools}

Analysis tasks:
1. Identify metric disparities and potential causes
2. Determine which team practices could be shared
3. Account for tech stack differences in comparison
4. Recommend cross-team learning opportunities
5. Suggest normalized metrics for fair comparison
```

## Implementation Prompts

### Design DORA Tracking System

```
Design a DORA metrics tracking system for the following environment:

Current Stack:
- Git: {git_platform}
- CI/CD: {cicd_tool}
- Container Orchestration: {container_platform}
- Incident Management: {incident_tool}
- Monitoring: {monitoring_stack}

Requirements:
- Real-time metrics dashboard
- Weekly automated reports
- Alert on metric degradation
- Team-level breakdown
- Historical trend analysis

Deliverables:
1. Architecture diagram (text-based)
2. Data flow for each DORA metric
3. Integration points with existing tools
4. Database schema for metrics storage
5. Dashboard specification
6. Implementation phases with dependencies
```

### Generate CI/CD Pipeline with DORA Tracking

```
Generate a {cicd_tool} pipeline configuration that tracks DORA metrics:

Repository: {repo_url}
Language: {programming_language}
Deployment Target: {deployment_target}
Existing Metrics Endpoint: {metrics_endpoint}

Pipeline Requirements:
- Build and test stages
- Deployment to staging and production
- Automatic DORA metric emission
- Deployment failure detection
- Rollback capability with metric tracking

Include:
1. Complete pipeline configuration file
2. Metric emission script/step
3. Environment variables needed
4. Secrets configuration
5. Deployment status webhook
```

### Create Grafana Dashboard

```
Generate a Grafana dashboard JSON for DORA metrics visualization:

Data Source: {datasource_type} (Prometheus/InfluxDB/PostgreSQL)
Metrics Available:
- deployments_total (counter)
- deployment_lead_time_seconds (histogram)
- deployments_failed_total (counter)
- incident_resolution_time_seconds (gauge)

Dashboard Requirements:
- Overview panel with all 4 DORA metrics as gauges
- Deployment frequency time series (daily/weekly)
- Lead time distribution histogram
- Change failure rate trend line
- MTTR with SLO target line
- Service selector variable
- Time range selector

Include threshold colors based on DORA performance levels.
```

## Improvement Prompts

### Improve Deployment Frequency

```
Our deployment frequency is currently {current_df} ({current_rating} rating).
Target: {target_df} ({target_rating} rating)

Current Process:
{current_deployment_process}

Constraints:
- Team size: {team_size}
- Legacy system dependencies: {legacy_deps}
- Compliance requirements: {compliance_reqs}

Generate a plan to improve deployment frequency:
1. Process changes (quick wins)
2. Technical changes (automation opportunities)
3. Cultural changes (team practices)
4. Metrics to track progress
5. Potential risks and mitigations
6. Phased implementation approach
```

### Reduce Lead Time

```
Current lead time: {current_lt} (from commit to production)
Target lead time: {target_lt}

Pipeline Breakdown:
- Code review: {review_time}
- CI build: {build_time}
- Automated tests: {test_time}
- Manual QA: {qa_time}
- Deployment: {deploy_time}
- Other: {other_time}

Provide recommendations to reduce lead time:
1. Identify the biggest time consumers
2. Suggest parallelization opportunities
3. Recommend automation for manual steps
4. Propose process improvements
5. Calculate expected lead time after improvements
6. Prioritize by effort vs impact
```

### Reduce Change Failure Rate

```
Current change failure rate: {current_cfr}%
Target: <15% (Elite)

Recent Failure Analysis:
{failure_analysis}

Current Testing Strategy:
- Unit test coverage: {unit_coverage}%
- Integration tests: {integration_tests}
- E2E tests: {e2e_tests}
- Performance tests: {perf_tests}
- Security scans: {security_scans}

Deployment Strategy:
- Method: {deployment_method}
- Rollback capability: {rollback_capability}
- Feature flags: {feature_flags}
- Canary/Blue-green: {progressive_deployment}

Recommend improvements to reduce failure rate:
1. Testing strategy enhancements
2. Deployment strategy improvements
3. Pre-deployment validation gates
4. Post-deployment verification
5. Quick rollback mechanisms
6. Root cause prevention measures
```

### Improve MTTR

```
Current MTTR: {current_mttr}
Target: <1 hour (Elite)

Incident Response Process:
{incident_process}

Monitoring Coverage:
- Application metrics: {app_metrics}
- Infrastructure metrics: {infra_metrics}
- Log aggregation: {logging}
- Alerting: {alerting}
- On-call rotation: {oncall}

Recent Incidents (summary):
{recent_incidents}

Provide recommendations to reduce MTTR:
1. Detection improvements (reduce time to detect)
2. Triage improvements (reduce time to understand)
3. Resolution improvements (reduce time to fix)
4. Automation opportunities (auto-remediation)
5. Runbook improvements
6. Post-incident learning process
```

## Reporting Prompts

### Generate Weekly Report

```
Generate a DORA metrics weekly report for stakeholders:

Period: {week_start} to {week_end}
Team/Service: {team_or_service}

This Week's Metrics:
- Deployment Frequency: {df_this_week}
- Lead Time: {lt_this_week}
- Change Failure Rate: {cfr_this_week}
- MTTR: {mttr_this_week}

Last Week's Metrics:
- Deployment Frequency: {df_last_week}
- Lead Time: {lt_last_week}
- Change Failure Rate: {cfr_last_week}
- MTTR: {mttr_last_week}

Notable Events:
{notable_events}

Generate a report including:
1. Executive summary (2-3 sentences)
2. Week-over-week comparison with trend arrows
3. Highlights and lowlights
4. Actions taken this week
5. Planned actions for next week
6. Risk/concern flags if any

Format: Professional, concise, suitable for executive audience.
```

### Create Quarterly Review

```
Generate a quarterly DORA metrics review presentation outline:

Quarter: {quarter}
Teams Included: {teams}

Quarterly Metrics Summary:
{quarterly_data}

Quarterly Initiatives:
{initiatives}

Achievements:
{achievements}

Challenges:
{challenges}

Create an outline including:
1. Quarter overview (key metrics, trends)
2. Per-team performance breakdown
3. Top improvements achieved
4. Challenges faced and lessons learned
5. Comparison to industry benchmarks
6. Goals for next quarter
7. Investment recommendations

Format: Slide-by-slide outline with key talking points.
```

## Integration Prompts

### PagerDuty Integration

```
Generate code to integrate PagerDuty incidents with DORA MTTR tracking:

PagerDuty API: REST v2
Target Metrics System: {metrics_system}
Language: {programming_language}

Requirements:
1. Fetch resolved incidents from PagerDuty
2. Calculate MTTR (detected_at to resolved_at)
3. Link incidents to services
4. Export to metrics system
5. Handle pagination
6. Error handling and retry logic

Include:
- Complete integration code
- Configuration template
- Scheduled job setup (cron/scheduler)
- Sample API responses handling
```

### GitHub Actions Reusable Workflow

```
Create a reusable GitHub Actions workflow for DORA metric tracking:

Workflow Inputs:
- service_name (required)
- environment (required)
- metrics_endpoint (required)
- api_key_secret (required)

Workflow should:
1. Be callable from other workflows
2. Capture commit and deployment timestamps
3. Detect rollbacks and hotfixes
4. Send deployment event to metrics endpoint
5. Handle failures gracefully
6. Support multiple deployment methods

Include:
- Reusable workflow file (.github/workflows/dora-tracking.yml)
- Example caller workflow
- Documentation for usage
```

---

*LLM prompts for DORA metrics analysis, implementation, improvement, and reporting.*
