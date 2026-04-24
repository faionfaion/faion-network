# AIOps LLM Prompts

## Anomaly Detection Prompts

### Prompt 1: Metric Anomaly Explanation

```
You are an AIOps analyst. Analyze the following metric anomaly and provide a clear explanation.

## Metric Data
- **Metric**: {{ metric_name }}
- **Service**: {{ service_name }}
- **Current Value**: {{ current_value }}
- **Baseline (same time last week)**: {{ baseline_value }}
- **Deviation**: {{ deviation_percent }}%
- **Duration**: {{ duration_minutes }} minutes

## Recent Context
{{ recent_events }}

## Task
1. Explain why this is anomalous in plain language
2. Assess the likely business impact (High/Medium/Low)
3. List top 3 probable causes in order of likelihood
4. Recommend immediate investigation steps

Format your response as:
### Anomaly Summary
[1-2 sentence explanation for non-technical stakeholders]

### Impact Assessment
[Business impact assessment]

### Probable Causes
1. [Most likely cause - confidence %]
2. [Second likely cause - confidence %]
3. [Third likely cause - confidence %]

### Investigation Steps
1. [First step]
2. [Second step]
3. [Third step]
```

### Prompt 2: Multi-Signal Correlation

```
You are an AIOps correlation engine. Multiple anomalies have been detected across different signals. Determine if they are related.

## Detected Anomalies

### Anomaly 1
- **Signal**: {{ signal_1_type }} ({{ signal_1_metric }})
- **Service**: {{ signal_1_service }}
- **Detected At**: {{ signal_1_time }}
- **Value**: {{ signal_1_value }}

### Anomaly 2
- **Signal**: {{ signal_2_type }} ({{ signal_2_metric }})
- **Service**: {{ signal_2_service }}
- **Detected At**: {{ signal_2_time }}
- **Value**: {{ signal_2_value }}

### Anomaly 3
- **Signal**: {{ signal_3_type }} ({{ signal_3_metric }})
- **Service**: {{ signal_3_service }}
- **Detected At**: {{ signal_3_time }}
- **Value**: {{ signal_3_value }}

## Service Topology
{{ service_dependency_graph }}

## Task
1. Determine correlation likelihood (Correlated/Possibly Correlated/Unrelated)
2. If correlated, identify the most likely root cause service
3. Explain the causal chain

Format your response as JSON:
{
  "correlation_status": "Correlated|Possibly Correlated|Unrelated",
  "confidence": 0.0-1.0,
  "root_cause_service": "service_name or null",
  "causal_chain": ["Event A", "caused Event B", "which caused Event C"],
  "explanation": "Natural language explanation"
}
```

---

## Root Cause Analysis Prompts

### Prompt 3: Incident RCA

```
You are a Site Reliability Engineer performing root cause analysis. An incident has occurred and you have the following data.

## Incident Summary
- **Incident ID**: {{ incident_id }}
- **Start Time**: {{ start_time }}
- **Duration**: {{ duration }}
- **Affected Service**: {{ affected_service }}
- **Symptoms**: {{ symptoms }}
- **User Impact**: {{ user_impact }}

## Timeline of Events
{{ event_timeline }}

## Recent Changes (last 24 hours)
{{ recent_changes }}

## Service Dependencies
{{ service_dependencies }}

## Metrics at Incident Time
{{ metrics_snapshot }}

## Log Excerpts
{{ relevant_logs }}

## Task
Perform root cause analysis and provide:
1. Root cause identification with confidence level
2. Contributing factors
3. Timeline reconstruction
4. Recommendations to prevent recurrence

Format as:
### Root Cause
**Cause**: [Primary root cause]
**Confidence**: [High/Medium/Low]
**Evidence**: [Supporting evidence]

### Contributing Factors
- [Factor 1]
- [Factor 2]

### Timeline Reconstruction
1. [Time]: [Event]
2. [Time]: [Event]
...

### Prevention Recommendations
1. [Short-term fix]
2. [Long-term improvement]
3. [Monitoring improvement]
```

### Prompt 4: Change Impact Analysis

```
A deployment is about to occur. Analyze the potential impact and risks.

## Deployment Details
- **Service**: {{ service_name }}
- **Environment**: {{ environment }}
- **Change Type**: {{ change_type }}
- **Changes**: {{ change_summary }}
- **Deployment Time**: {{ deployment_time }}

## Current System State
- **Error Rate**: {{ current_error_rate }}%
- **Latency P99**: {{ current_latency }}ms
- **Traffic Level**: {{ traffic_level }} (compared to normal)
- **Recent Incidents**: {{ recent_incidents }}

## Service Dependencies
- **Upstream**: {{ upstream_services }}
- **Downstream**: {{ downstream_services }}

## Historical Data
- **Previous similar deployments**: {{ similar_deployments }}
- **Previous rollbacks**: {{ previous_rollbacks }}

## Task
Assess deployment risk and provide recommendations:
1. Risk level (High/Medium/Low)
2. Potential failure modes
3. Recommended monitoring during deployment
4. Rollback criteria

Format as:
### Risk Assessment
**Risk Level**: [High/Medium/Low]
**Reasoning**: [Explanation]

### Potential Failure Modes
1. [Failure mode 1] - Likelihood: [High/Medium/Low]
2. [Failure mode 2] - Likelihood: [High/Medium/Low]

### Monitoring Recommendations
Watch these metrics during deployment:
- [Metric 1]: Alert if [condition]
- [Metric 2]: Alert if [condition]

### Rollback Criteria
Trigger rollback if:
- [Condition 1]
- [Condition 2]
```

---

## Incident Management Prompts

### Prompt 5: Incident Summary Generation

```
Generate an incident summary for stakeholders based on the following data.

## Incident Data
- **ID**: {{ incident_id }}
- **Service**: {{ service_name }}
- **Start**: {{ start_time }}
- **End**: {{ end_time }}
- **Duration**: {{ duration }}
- **Severity**: {{ severity }}

## Impact
- **Users Affected**: {{ users_affected }}
- **Requests Failed**: {{ requests_failed }}
- **Revenue Impact**: {{ revenue_impact }}

## Timeline
{{ event_timeline }}

## Resolution
{{ resolution_steps }}

## Task
Create a concise incident summary suitable for:
1. Executive summary (2-3 sentences, non-technical)
2. Technical summary (detailed, for engineering)
3. Customer communication (if needed)

Format as:
### Executive Summary
[Non-technical summary for leadership]

### Technical Summary
**What happened**: [Technical explanation]
**Why it happened**: [Root cause]
**How it was fixed**: [Resolution]
**Prevention**: [Future prevention measures]

### Customer Communication
[Draft message for affected customers, if applicable]
```

### Prompt 6: Runbook Generation

```
Generate a runbook for the following alert based on historical incident data.

## Alert Definition
- **Alert Name**: {{ alert_name }}
- **Condition**: {{ alert_condition }}
- **Severity**: {{ severity }}
- **Service**: {{ service_name }}

## Historical Incidents
{{ historical_incidents }}

## Service Architecture
{{ service_architecture }}

## Available Remediation Actions
{{ available_actions }}

## Task
Generate a step-by-step runbook including:
1. Initial triage steps
2. Diagnosis commands
3. Remediation options
4. Verification steps
5. Escalation criteria

Format as Markdown runbook:
# Runbook: {{ alert_name }}

## Quick Reference
- **Severity**: {{ severity }}
- **On-Call**: {{ team }}
- **Escalation**: {{ escalation_path }}

## Triage (First 5 minutes)
1. [Step 1]
2. [Step 2]

## Diagnosis
### Check 1: [Name]
\`\`\`bash
[command]
\`\`\`
Expected: [what to look for]

### Check 2: [Name]
...

## Remediation Options

### Option A: [Name] (Recommended for [condition])
\`\`\`bash
[commands]
\`\`\`

### Option B: [Name] (If Option A fails)
...

## Verification
1. [Verify step 1]
2. [Verify step 2]

## Escalation
Escalate if:
- [Condition 1]
- [Condition 2]
```

---

## Auto-Remediation Prompts

### Prompt 7: Remediation Recommendation

```
An incident is in progress. Based on the data, recommend remediation actions.

## Current Incident
- **Service**: {{ service_name }}
- **Symptom**: {{ primary_symptom }}
- **Duration**: {{ incident_duration }}
- **Severity**: {{ severity }}

## Diagnostic Data
- **CPU**: {{ cpu_usage }}%
- **Memory**: {{ memory_usage }}%
- **Error Rate**: {{ error_rate }}%
- **Latency P99**: {{ latency_p99 }}ms
- **Pod Restarts**: {{ pod_restarts }}
- **Recent Deployment**: {{ recent_deployment }}

## Available Actions
{{ available_remediation_actions }}

## Constraints
- Max blast radius: {{ max_blast_radius }}
- Approval required for: {{ approval_required_actions }}
- Currently disabled: {{ disabled_actions }}

## Task
Recommend remediation actions in order of preference:
1. Most likely to resolve with least risk
2. Explain expected outcome
3. Specify approval requirements
4. Provide rollback plan

Format as JSON:
{
  "recommended_actions": [
    {
      "action": "action_name",
      "confidence": 0.0-1.0,
      "expected_outcome": "description",
      "risk_level": "low|medium|high",
      "requires_approval": true|false,
      "rollback_plan": "how to undo if needed",
      "estimated_recovery_time": "X minutes"
    }
  ],
  "reasoning": "explanation of recommendation logic"
}
```

### Prompt 8: Post-Remediation Analysis

```
Analyze the effectiveness of an auto-remediation action.

## Remediation Details
- **Action Taken**: {{ action_name }}
- **Triggered At**: {{ trigger_time }}
- **Completed At**: {{ completion_time }}
- **Target**: {{ target_resource }}

## Before Remediation
{{ metrics_before }}

## After Remediation
{{ metrics_after }}

## Expected Outcome
{{ expected_outcome }}

## Task
Analyze the remediation effectiveness:
1. Was the remediation successful?
2. Did it fully resolve the issue?
3. Were there any side effects?
4. Should the remediation policy be adjusted?

Format as:
### Remediation Assessment
**Status**: [Successful/Partially Successful/Failed]
**Issue Resolved**: [Yes/Partially/No]

### Metrics Comparison
| Metric | Before | After | Expected | Status |
|--------|--------|-------|----------|--------|
| [metric] | [value] | [value] | [value] | [check] |

### Side Effects
[Any observed side effects or none]

### Policy Recommendations
[Suggestions to improve remediation policy]
```

---

## Postmortem Prompts

### Prompt 9: Postmortem Draft

```
Generate a postmortem document based on incident data.

## Incident Summary
- **ID**: {{ incident_id }}
- **Date**: {{ incident_date }}
- **Duration**: {{ duration }}
- **Severity**: {{ severity }}
- **Services Affected**: {{ affected_services }}

## Timeline
{{ full_timeline }}

## Impact
{{ impact_details }}

## Root Cause
{{ root_cause }}

## Resolution
{{ resolution_steps }}

## Detection
- **How detected**: {{ detection_method }}
- **Time to detect**: {{ time_to_detect }}

## Response
- **Responders**: {{ responders }}
- **Time to mitigate**: {{ time_to_mitigate }}

## Task
Generate a blameless postmortem document with:
1. Executive summary
2. Detailed timeline
3. Root cause analysis (5 Whys)
4. Impact assessment
5. Action items (categorized by priority)
6. Lessons learned

Use blameless language focusing on systems and processes, not individuals.

Format as Markdown postmortem document.
```

### Prompt 10: Action Item Generation

```
Based on this postmortem, generate specific action items.

## Postmortem Summary
{{ postmortem_summary }}

## Root Cause
{{ root_cause }}

## Contributing Factors
{{ contributing_factors }}

## Current Gaps
{{ identified_gaps }}

## Task
Generate action items that:
1. Address the root cause
2. Improve detection capability
3. Enhance response procedures
4. Prevent recurrence

For each action item, specify:
- Clear description
- Owner (team, not individual)
- Priority (P0/P1/P2/P3)
- Due date suggestion (relative)
- Success criteria

Format as:
### P0 - Critical (Complete within 1 week)
- [ ] [Action item] - Owner: [Team] - Success: [Criteria]

### P1 - High (Complete within 2 weeks)
- [ ] [Action item] - Owner: [Team] - Success: [Criteria]

### P2 - Medium (Complete within 1 month)
- [ ] [Action item] - Owner: [Team] - Success: [Criteria]

### P3 - Low (Complete within quarter)
- [ ] [Action item] - Owner: [Team] - Success: [Criteria]
```

---

## Integration Prompts

### Prompt 11: Alert Enrichment

```
Enrich this alert with additional context from available data sources.

## Raw Alert
{{ raw_alert }}

## Available Context
- **Service metadata**: {{ service_metadata }}
- **Recent deployments**: {{ recent_deployments }}
- **Related alerts**: {{ related_alerts }}
- **Service topology**: {{ service_topology }}
- **On-call schedule**: {{ oncall_schedule }}

## Task
Enrich the alert with:
1. Plain language summary
2. Business context
3. Likely root cause
4. Suggested first responder actions
5. Relevant runbook link

Format as enriched alert JSON:
{
  "original_alert": {{ raw_alert }},
  "enrichment": {
    "summary": "Human-readable summary",
    "business_context": "Impact on business operations",
    "probable_cause": "Most likely cause",
    "confidence": 0.0-1.0,
    "suggested_actions": ["action1", "action2"],
    "runbook_url": "link if available",
    "related_incidents": ["INC-xxx"],
    "oncall": {
      "primary": "name",
      "secondary": "name"
    }
  }
}
```

### Prompt 12: Capacity Planning

```
Analyze resource usage trends and provide capacity planning recommendations.

## Current Resource Usage (30-day average)
{{ resource_usage }}

## Traffic Patterns
{{ traffic_patterns }}

## Growth Rate
{{ growth_rate }}

## Upcoming Events
{{ upcoming_events }}

## Current Infrastructure
{{ current_infrastructure }}

## Task
Provide capacity planning recommendations:
1. Project resource needs for next 3/6/12 months
2. Identify potential bottlenecks
3. Recommend scaling actions
4. Estimate cost implications

Format as:
### Resource Projections

| Resource | Current | 3 Months | 6 Months | 12 Months |
|----------|---------|----------|----------|-----------|
| [resource] | [value] | [value] | [value] | [value] |

### Bottleneck Analysis
1. [Potential bottleneck] - Risk: [High/Medium/Low] - Timeline: [When]

### Scaling Recommendations

#### Short-term (0-3 months)
- [Recommendation]

#### Medium-term (3-6 months)
- [Recommendation]

#### Long-term (6-12 months)
- [Recommendation]

### Cost Estimate
[Estimated additional cost for recommended changes]
```
