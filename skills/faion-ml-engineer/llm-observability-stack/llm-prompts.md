---
id: llm-observability-stack-prompts
name: "LLM Observability Stack Prompts"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Stack Prompts

Prompts for stack evaluation, debugging, and optimization.

## Stack Evaluation Prompts

### Platform Selection Analysis

```
You are an LLM observability expert helping choose the right monitoring stack.

## Current Situation
**Application Type:** {app_type}
**LLM Providers:** {providers}
**Frameworks:** {frameworks}
**Monthly LLM Spend:** {monthly_spend}
**Team Size:** {team_size}
**Existing Observability:** {existing_tools}

## Requirements
- Self-hosting requirement: {self_host}
- Compliance needs: {compliance}
- Primary concern: {primary_concern}

## Platforms to Consider
1. Langfuse (MIT, self-hosted, tracing + evals)
2. LangSmith (LangChain native, debugging)
3. Helicone (proxy, cost optimization)
4. Portkey (multi-provider gateway)
5. Arize Phoenix (evaluation, embeddings)
6. OpenLLMetry (OTEL-native, existing APM)
7. Datadog LLM Observability (enterprise APM)

## Output Format
{
  "recommended_primary": "<platform>",
  "recommended_secondary": "<platform or null>",
  "reasoning": "<explanation>",
  "integration_complexity": "low|medium|high",
  "estimated_monthly_cost": "<range>",
  "key_tradeoffs": ["<tradeoff1>", "<tradeoff2>"],
  "migration_path": "<if switching from existing>"
}
```

### Stack Health Assessment

```
You are analyzing an LLM observability stack configuration for issues.

## Current Stack Configuration
**Tracing Platform:** {tracing_platform}
**Cost Tracking:** {cost_tracking}
**Evaluation System:** {eval_system}
**Alerting:** {alerting}
**Dashboards:** {dashboards}

## Current Metrics
- Trace coverage: {trace_coverage}%
- Alert false positive rate: {false_positive_rate}%
- Mean time to debug: {mttr_minutes} minutes
- Cost visibility delay: {cost_delay} hours
- Quality score tracking: {quality_tracking}

## Recent Issues
{recent_issues}

## Task
Identify gaps and recommend improvements to the observability stack.

## Output Format
{
  "health_score": <1-10>,
  "critical_gaps": ["<gap1>", "<gap2>"],
  "recommended_improvements": [
    {
      "area": "<area>",
      "current_state": "<description>",
      "recommended_state": "<description>",
      "priority": "high|medium|low",
      "effort": "low|medium|high"
    }
  ],
  "quick_wins": ["<improvement1>", "<improvement2>"],
  "long_term_recommendations": ["<recommendation1>"]
}
```

---

## Debugging Prompts

### Trace Analysis

```
You are debugging an LLM trace to identify issues.

## Trace Data
**Trace ID:** {trace_id}
**Duration:** {duration_ms}ms
**Token Usage:** Input: {input_tokens}, Output: {output_tokens}
**Status:** {status}
**Model:** {model}

## Spans
{spans_json}

## Prompt
{prompt}

## Response
{response}

## Expected Behavior
{expected_behavior}

## Task
Analyze the trace and identify potential issues.

## Output Format
{
  "issue_identified": true|false,
  "issue_type": "latency|quality|cost|error|none",
  "root_cause": "<explanation>",
  "problematic_span": "<span_name or null>",
  "recommendations": [
    {
      "action": "<what to do>",
      "expected_impact": "<improvement>",
      "implementation": "<how to do it>"
    }
  ],
  "similar_issues_to_check": ["<pattern1>", "<pattern2>"]
}
```

### Cost Anomaly Investigation

```
You are investigating a cost anomaly in LLM usage.

## Anomaly Details
**Time Window:** {start_time} to {end_time}
**Expected Cost:** ${expected_cost}
**Actual Cost:** ${actual_cost}
**Anomaly Factor:** {anomaly_factor}x

## Usage Breakdown
| Model | Requests | Input Tokens | Output Tokens | Cost |
{usage_table}

## Comparison with Previous Period
| Metric | Previous | Current | Change |
{comparison_table}

## Top Users/Teams
{top_users}

## Task
Identify the cause of the cost anomaly and recommend actions.

## Output Format
{
  "root_cause": "<explanation>",
  "contributing_factors": [
    {
      "factor": "<description>",
      "impact_percentage": <0-100>,
      "evidence": "<what data shows this>"
    }
  ],
  "is_legitimate": true|false,
  "immediate_actions": ["<action1>", "<action2>"],
  "preventive_measures": ["<measure1>", "<measure2>"],
  "estimated_savings": "<if actions taken>"
}
```

### Quality Degradation Analysis

```
You are analyzing a quality degradation in LLM responses.

## Quality Metrics
**Current Average Score:** {current_score}/5
**Previous Average Score:** {previous_score}/5
**Degradation Period:** {degradation_period}
**Affected Queries:** {affected_percentage}%

## Score Breakdown
| Metric | Previous | Current | Delta |
| Relevance | {prev_relevance} | {curr_relevance} | {delta_relevance} |
| Accuracy | {prev_accuracy} | {curr_accuracy} | {delta_accuracy} |
| Completeness | {prev_completeness} | {curr_completeness} | {delta_completeness} |

## Sample Low-Quality Responses
{low_quality_samples}

## Recent Changes
- Prompt changes: {prompt_changes}
- Model changes: {model_changes}
- Context/RAG changes: {rag_changes}

## Task
Identify the cause of quality degradation and recommend fixes.

## Output Format
{
  "degradation_type": "relevance|accuracy|completeness|coherence|mixed",
  "likely_cause": "<explanation>",
  "confidence": <0-1>,
  "affected_query_types": ["<type1>", "<type2>"],
  "immediate_fixes": [
    {
      "fix": "<description>",
      "expected_improvement": "<metric improvement>",
      "risk": "low|medium|high"
    }
  ],
  "testing_recommendations": ["<test1>", "<test2>"],
  "monitoring_improvements": ["<improvement1>"]
}
```

---

## Optimization Prompts

### Cost Optimization Recommendations

```
You are optimizing LLM costs based on usage patterns.

## Current Usage (Last 30 Days)
**Total Spend:** ${total_spend}
**Total Requests:** {total_requests}
**Total Tokens:** {total_tokens}

## Model Usage
| Model | Requests | Tokens | Cost | Avg Tokens/Req |
{model_usage_table}

## Cache Performance
- Cache hit rate: {cache_hit_rate}%
- Estimated savings: ${cache_savings}

## Quality Metrics
- Average quality score: {avg_quality}/5
- Quality threshold: {quality_threshold}/5

## Task
Provide specific cost optimization recommendations.

## Output Format
{
  "current_cost_efficiency": "<rating>",
  "optimization_opportunities": [
    {
      "strategy": "<name>",
      "description": "<what to do>",
      "estimated_savings_percent": <0-100>,
      "estimated_savings_usd": <amount>,
      "implementation_effort": "low|medium|high",
      "quality_impact": "none|minimal|moderate",
      "specific_actions": ["<action1>", "<action2>"]
    }
  ],
  "priority_order": ["<strategy1>", "<strategy2>"],
  "projected_monthly_savings": "<range>",
  "quality_monitoring_needed": ["<metric1>", "<metric2>"]
}
```

### Alert Tuning Recommendations

```
You are optimizing alert configurations to reduce noise.

## Current Alert Configuration
{alert_config_yaml}

## Alert Statistics (Last 30 Days)
| Alert | Fires | True Positives | False Positives | MTTR |
{alert_stats_table}

## False Positive Examples
{false_positive_examples}

## Missed Issues (Not Alerted)
{missed_issues}

## Task
Recommend alert threshold adjustments and new alerts.

## Output Format
{
  "alert_health_score": <1-10>,
  "threshold_adjustments": [
    {
      "alert": "<alert_name>",
      "current_threshold": "<value>",
      "recommended_threshold": "<value>",
      "reasoning": "<explanation>",
      "expected_fp_reduction": "<percentage>"
    }
  ],
  "alerts_to_add": [
    {
      "name": "<alert_name>",
      "condition": "<promql or description>",
      "threshold": "<value>",
      "severity": "critical|warning|info",
      "reasoning": "<why needed>"
    }
  ],
  "alerts_to_remove": [
    {
      "name": "<alert_name>",
      "reasoning": "<why remove>"
    }
  ],
  "grouping_recommendations": ["<recommendation1>"]
}
```

---

## Dashboard Generation Prompts

### Executive Dashboard Requirements

```
You are designing an executive LLM observability dashboard.

## Audience
- C-level executives
- Finance team
- Non-technical stakeholders

## Available Metrics
{available_metrics_list}

## Business Goals
- Cost control: ${monthly_budget} budget
- Quality threshold: {quality_threshold}/5
- Reliability target: {uptime_target}%

## Task
Design a concise executive dashboard with key panels.

## Output Format
{
  "dashboard_title": "<title>",
  "refresh_rate": "<interval>",
  "panels": [
    {
      "title": "<panel_title>",
      "type": "stat|gauge|timeseries|piechart|table",
      "position": {"row": <n>, "col": <n>, "width": <n>, "height": <n>},
      "metric_query": "<promql or description>",
      "thresholds": {"warning": <value>, "critical": <value>},
      "business_context": "<why this matters>"
    }
  ],
  "drill_down_links": ["<dashboard1>", "<dashboard2>"],
  "export_schedule": "<recommendation>"
}
```

### Engineering Dashboard Requirements

```
You are designing a technical LLM observability dashboard for engineers.

## Audience
- ML Engineers
- Backend Developers
- SRE/DevOps

## Available Metrics
{available_metrics_list}

## Debugging Needs
{common_debugging_scenarios}

## Task
Design a comprehensive engineering dashboard for debugging and optimization.

## Output Format
{
  "dashboard_title": "<title>",
  "sections": [
    {
      "name": "<section_name>",
      "panels": [
        {
          "title": "<panel_title>",
          "type": "stat|gauge|timeseries|heatmap|table|logs",
          "metric_query": "<promql>",
          "purpose": "<what question it answers>"
        }
      ]
    }
  ],
  "filters": ["model", "endpoint", "user_id", "environment"],
  "drill_down_capabilities": ["<capability1>"],
  "alerting_integration": "<how alerts link to dashboard>"
}
```

---

## Runbook Generation Prompts

### Alert Runbook Generation

```
You are creating a runbook for an LLM observability alert.

## Alert Details
**Name:** {alert_name}
**Condition:** {alert_condition}
**Severity:** {severity}
**Current Threshold:** {threshold}

## Historical Context
- Average fires per week: {fires_per_week}
- Average resolution time: {avg_resolution_time}
- Common root causes: {common_causes}

## Available Diagnostic Tools
- Langfuse traces: {langfuse_url}
- Grafana dashboards: {grafana_url}
- Log aggregation: {logs_url}

## Task
Create a step-by-step runbook for responding to this alert.

## Output Format
{
  "alert_name": "<name>",
  "severity": "<severity>",
  "description": "<what this alert means>",
  "business_impact": "<potential impact>",
  "steps": [
    {
      "step": <number>,
      "action": "<what to do>",
      "tool": "<tool to use>",
      "query_or_command": "<specific query or command>",
      "expected_output": "<what to look for>",
      "decision_point": "<if X then Y, else Z>"
    }
  ],
  "escalation_criteria": ["<criterion1>", "<criterion2>"],
  "escalation_contacts": ["<team or person>"],
  "resolution_verification": "<how to confirm fixed>",
  "post_incident_actions": ["<action1>", "<action2>"]
}
```

---

## Implementation Notes

### Using These Prompts

1. **Replace placeholders** with actual data from your observability stack
2. **Use structured output** (JSON mode) for consistent parsing
3. **Store results** in your observability platform for tracking
4. **Automate** common analyses with scheduled evaluations
5. **Version prompts** and track effectiveness over time

### Integration with Observability Stack

```python
from langfuse import Langfuse
from openai import OpenAI

langfuse = Langfuse()
client = OpenAI()

async def analyze_cost_anomaly(anomaly_data: dict) -> dict:
    """Run cost anomaly analysis using LLM."""
    prompt = COST_ANOMALY_PROMPT.format(**anomaly_data)

    # Create trace for the analysis itself
    trace = langfuse.trace(name="cost_anomaly_analysis")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)

    # Log analysis result
    trace.update(
        metadata={
            "anomaly_factor": anomaly_data["anomaly_factor"],
            "root_cause": result["root_cause"]
        }
    )

    return result
```

### Best Practices

1. **Cache analysis results** to avoid re-running expensive analyses
2. **Set up automated triggers** for common debugging scenarios
3. **Track prompt effectiveness** using A/B testing
4. **Create feedback loops** to improve prompts over time
5. **Document decisions** made based on LLM analyses
