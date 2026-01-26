# AIOps Templates

Reusable templates for AIOps implementation.

## Prometheus Alerting Templates

### Anomaly Detection Alert Template

```yaml
# prometheus-anomaly-template.yaml
groups:
  - name: aiops-{SERVICE_NAME}-anomalies
    interval: 30s
    rules:
      # Z-Score based anomaly detection
      - alert: {SERVICE_NAME}_{METRIC_NAME}Anomaly
        expr: |
          abs(
            {METRIC_QUERY}
            - avg_over_time({METRIC_QUERY}[{BASELINE_PERIOD}])
          ) / stddev_over_time({METRIC_QUERY}[{BASELINE_PERIOD}]) > {THRESHOLD}
        for: {DURATION}
        labels:
          severity: {SEVERITY}
          category: aiops
          service: {SERVICE_NAME}
          detection_type: zscore
        annotations:
          summary: "Anomaly detected in {{ $labels.instance }}"
          description: "{{ $labels.{LABEL} }} is deviating from baseline by {{ $value | humanize }} standard deviations"
          runbook_url: "{RUNBOOK_URL}"

      # Change-aware detection (higher weight after deploys)
      - alert: {SERVICE_NAME}PostDeployAnomaly
        expr: |
          {METRIC_QUERY}
          and on() (time() - {DEPLOY_TIMESTAMP_METRIC}) < 3600
          and abs(
            {METRIC_QUERY}
            - avg_over_time({METRIC_QUERY}[1d] offset 1h)
          ) > {POST_DEPLOY_THRESHOLD}
        for: 5m
        labels:
          severity: warning
          category: aiops
          detection_type: change_aware
```

### Multi-Signal Convergence Template

```yaml
# prometheus-convergence-template.yaml
groups:
  - name: aiops-convergent-incidents
    rules:
      # Require multiple signals before incident
      - alert: ConvergentIncident_{SERVICE_NAME}
        expr: |
          (
            # Signal 1: Error rate
            (rate({ERROR_METRIC}[5m]) > {ERROR_THRESHOLD}) +
            # Signal 2: Latency
            (histogram_quantile(0.99, rate({LATENCY_METRIC}[5m])) > {LATENCY_THRESHOLD}) +
            # Signal 3: Resource pressure
            ({RESOURCE_METRIC} > {RESOURCE_THRESHOLD})
          ) >= {MIN_SIGNALS}
        for: 5m
        labels:
          severity: critical
          category: aiops
          detection_type: convergent
        annotations:
          summary: "Multiple anomaly signals detected for {SERVICE_NAME}"
          signals_detected: "{{ $value }} of {MIN_SIGNALS} minimum"
```

## Kubernetes Remediation Templates

### Auto-Restart ConfigMap Template

```yaml
# aiops-restart-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aiops-restart-config
  namespace: {NAMESPACE}
data:
  restart-policy.yaml: |
    rules:
      - name: memory-pressure-restart
        selector:
          labelSelector:
            app: {APP_NAME}
        trigger:
          metric: container_memory_usage_bytes
          operator: ">"
          threshold: "{MEMORY_THRESHOLD}"
          duration: 5m
        action:
          type: restart
          gracePeriod: 30
        cooldown: 10m
        maxRestarts: 3

      - name: liveness-failure-restart
        selector:
          labelSelector:
            app: {APP_NAME}
        trigger:
          event: PodUnhealthy
          count: 3
          window: 5m
        action:
          type: restart
          gracePeriod: 0
        cooldown: 5m
```

### HPA with Predictive Scaling Template

```yaml
# aiops-predictive-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {DEPLOYMENT_NAME}-aiops-hpa
  namespace: {NAMESPACE}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {DEPLOYMENT_NAME}
  minReplicas: {MIN_REPLICAS}
  maxReplicas: {MAX_REPLICAS}
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: {SCALE_UP_PODS}
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 120
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {CPU_TARGET}
    - type: External
      external:
        metric:
          name: aiops_predicted_load
          selector:
            matchLabels:
              service: {SERVICE_NAME}
        target:
          type: Value
          value: "{PREDICTED_LOAD_THRESHOLD}"
```

### Rollback Controller Template

```yaml
# aiops-rollback-controller.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aiops-rollback-config
  namespace: {NAMESPACE}
data:
  rollback-rules.yaml: |
    deployments:
      - name: {DEPLOYMENT_NAME}
        namespace: {NAMESPACE}
        triggers:
          - type: error_rate
            metric: "sum(rate(http_requests_total{status=~'5..'}[5m])) / sum(rate(http_requests_total[5m]))"
            threshold: {ERROR_RATE_THRESHOLD}
            duration: 3m

          - type: availability
            metric: "up{job='{JOB_NAME}'}"
            threshold: 0
            duration: 2m

          - type: latency
            metric: "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))"
            threshold: {LATENCY_THRESHOLD}
            duration: 5m

        action:
          type: rollback
          revisions: 1
          waitTime: 60s

        approval:
          required: {APPROVAL_REQUIRED}
          channel: "{SLACK_CHANNEL}"
          timeout: 300s
          escalate_to: "{ESCALATION_CONTACT}"
```

## Slack Notification Templates

### Incident Alert Template

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "{SEVERITY_EMOJI} {INCIDENT_TITLE}"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Service:*\n{SERVICE_NAME}"
        },
        {
          "type": "mrkdwn",
          "text": "*Severity:*\n{SEVERITY}"
        },
        {
          "type": "mrkdwn",
          "text": "*Detection Type:*\n{DETECTION_TYPE}"
        },
        {
          "type": "mrkdwn",
          "text": "*Signals:*\n{SIGNAL_COUNT} convergent"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Summary:*\n{INCIDENT_SUMMARY}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Recommended Action:*\n{RECOMMENDED_ACTION}"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Approve Remediation"
          },
          "style": "primary",
          "action_id": "approve_remediation",
          "value": "{ACTION_ID}"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Reject"
          },
          "style": "danger",
          "action_id": "reject_remediation",
          "value": "{ACTION_ID}"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View Dashboard"
          },
          "url": "{DASHBOARD_URL}"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Auto-approval in {TIMEOUT_SECONDS}s if no action taken | <{RUNBOOK_URL}|View Runbook>"
        }
      ]
    }
  ]
}
```

### Postmortem Summary Template

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Incident Postmortem: {INCIDENT_ID}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Duration:* {DURATION}\n*Impact:* {IMPACT_DESCRIPTION}\n*Services Affected:* {AFFECTED_SERVICES}"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Timeline:*\n{TIMELINE_EVENTS}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Root Cause:*\n{ROOT_CAUSE}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Remediation Actions Taken:*\n{ACTIONS_TAKEN}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Action Items:*\n{ACTION_ITEMS}"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Generated by AIOps | <{FULL_REPORT_URL}|View Full Report>"
        }
      ]
    }
  ]
}
```

## Python Class Templates

### AIOps Service Template

```python
# aiops_service_template.py
"""
AIOps Service Template for {SERVICE_NAME}

Replace placeholders:
- {SERVICE_NAME}: Your service name
- {PROMETHEUS_URL}: Prometheus server URL
- {SLACK_WEBHOOK}: Slack webhook URL
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
import asyncio
import logging

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TrustLevel(Enum):
    AUTO = "auto"
    RECOMMEND = "recommend"
    HUMAN_APPROVE = "human_approve"
    MANUAL_ONLY = "manual_only"

@dataclass
class Anomaly:
    metric: str
    value: float
    baseline: float
    deviation: float
    timestamp: float
    severity: Severity

@dataclass
class Incident:
    id: str
    anomalies: List[Anomaly]
    severity: Severity
    recommended_action: Optional[str]
    trust_level: TrustLevel

@dataclass
class RemediationResult:
    success: bool
    action: str
    details: Dict[str, Any]
    duration_ms: int

class AIOpsService:
    def __init__(
        self,
        prometheus_url: str = "{PROMETHEUS_URL}",
        slack_webhook: str = "{SLACK_WEBHOOK}",
        min_convergent_signals: int = 2
    ):
        self.prometheus_url = prometheus_url
        self.slack_webhook = slack_webhook
        self.min_signals = min_convergent_signals
        self.logger = logging.getLogger(__name__)

    async def detect_anomalies(self, metrics: Dict[str, float]) -> List[Anomaly]:
        """Detect anomalies in provided metrics."""
        # Implementation here
        raise NotImplementedError

    async def evaluate_incident(self, anomalies: List[Anomaly]) -> Optional[Incident]:
        """Evaluate if anomalies constitute an incident."""
        if len(anomalies) < self.min_signals:
            return None
        # Implementation here
        raise NotImplementedError

    async def execute_remediation(self, incident: Incident) -> RemediationResult:
        """Execute remediation based on trust level."""
        # Implementation here
        raise NotImplementedError

    async def notify(self, incident: Incident) -> bool:
        """Send notification via configured channels."""
        # Implementation here
        raise NotImplementedError

    async def run(self):
        """Main event loop."""
        while True:
            try:
                metrics = await self._fetch_metrics()
                anomalies = await self.detect_anomalies(metrics)

                if incident := await self.evaluate_incident(anomalies):
                    await self.notify(incident)

                    if incident.trust_level == TrustLevel.AUTO:
                        await self.execute_remediation(incident)

            except Exception as e:
                self.logger.error(f"Error in AIOps loop: {e}")

            await asyncio.sleep(30)
```

## Grafana Dashboard Template

```json
{
  "dashboard": {
    "title": "AIOps - {SERVICE_NAME}",
    "tags": ["aiops", "{SERVICE_NAME}"],
    "panels": [
      {
        "title": "Anomaly Detection Status",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "sum(aiops_anomalies_detected_total{service=\"{SERVICE_NAME}\"})",
            "legendFormat": "Anomalies (24h)"
          }
        ]
      },
      {
        "title": "Auto-Remediation Rate",
        "type": "gauge",
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 0},
        "targets": [
          {
            "expr": "sum(aiops_remediations_auto_total) / sum(aiops_remediations_total) * 100",
            "legendFormat": "Auto %"
          }
        ],
        "options": {
          "thresholds": [
            {"value": 0, "color": "red"},
            {"value": 15, "color": "yellow"},
            {"value": 40, "color": "green"}
          ]
        }
      },
      {
        "title": "Anomaly Score Timeline",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4},
        "targets": [
          {
            "expr": "aiops_anomaly_score{service=\"{SERVICE_NAME}\"}",
            "legendFormat": "{{metric}}"
          }
        ]
      },
      {
        "title": "Remediation Actions",
        "type": "table",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4},
        "targets": [
          {
            "expr": "aiops_remediation_actions{service=\"{SERVICE_NAME}\"}",
            "format": "table"
          }
        ]
      }
    ]
  }
}
```

---

*AIOps Templates | faion-cicd-engineer*
