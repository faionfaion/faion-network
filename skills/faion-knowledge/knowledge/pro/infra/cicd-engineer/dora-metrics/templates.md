# DORA Metrics Templates

## GitHub Actions Workflow Template

```yaml
# .github/workflows/deploy-with-dora.yml
name: Deploy with DORA Metrics

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  METRICS_ENDPOINT: ${{ secrets.DORA_METRICS_ENDPOINT }}
  SERVICE_NAME: ${{ github.repository }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    outputs:
      deploy_status: ${{ steps.deploy.outcome }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get commit timestamp
        id: commit_info
        run: |
          echo "commit_timestamp=$(git show -s --format=%cI HEAD)" >> $GITHUB_OUTPUT
          echo "commit_sha=${{ github.sha }}" >> $GITHUB_OUTPUT

      - name: Deploy
        id: deploy
        run: |
          # Your deployment script here
          ./deploy.sh

      - name: Record Deployment (Success)
        if: success()
        run: |
          curl -X POST "$METRICS_ENDPOINT/events/deployment" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${{ secrets.DORA_API_KEY }}" \
            -d '{
              "service": "${{ env.SERVICE_NAME }}",
              "environment": "production",
              "commit_sha": "${{ steps.commit_info.outputs.commit_sha }}",
              "commit_timestamp": "${{ steps.commit_info.outputs.commit_timestamp }}",
              "deployed_at": "'$(date -Iseconds)'",
              "is_rollback": false,
              "is_hotfix": false,
              "pipeline_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
            }'

      - name: Record Deployment (Failure)
        if: failure()
        run: |
          curl -X POST "$METRICS_ENDPOINT/events/deployment" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${{ secrets.DORA_API_KEY }}" \
            -d '{
              "service": "${{ env.SERVICE_NAME }}",
              "environment": "production",
              "commit_sha": "${{ steps.commit_info.outputs.commit_sha }}",
              "commit_timestamp": "${{ steps.commit_info.outputs.commit_timestamp }}",
              "deployed_at": "'$(date -Iseconds)'",
              "status": "failed",
              "pipeline_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
            }'
```

## GitLab CI Template

```yaml
# .gitlab-ci.yml
include:
  - template: Jobs/Deploy.gitlab-ci.yml

variables:
  DORA_METRICS_ENDPOINT: ${DORA_METRICS_ENDPOINT}
  SERVICE_NAME: ${CI_PROJECT_NAME}

stages:
  - build
  - test
  - deploy
  - metrics

deploy_production:
  stage: deploy
  environment:
    name: production
    url: https://${CI_PROJECT_NAME}.example.com
  script:
    - ./deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

record_deployment:
  stage: metrics
  needs: [deploy_production]
  script:
    - |
      COMMIT_TIMESTAMP=$(git show -s --format=%cI HEAD)
      DEPLOYED_AT=$(date -Iseconds)

      curl -X POST "${DORA_METRICS_ENDPOINT}/events/deployment" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${DORA_API_KEY}" \
        -d "{
          \"service\": \"${SERVICE_NAME}\",
          \"environment\": \"production\",
          \"commit_sha\": \"${CI_COMMIT_SHA}\",
          \"commit_timestamp\": \"${COMMIT_TIMESTAMP}\",
          \"deployed_at\": \"${DEPLOYED_AT}\",
          \"is_rollback\": false,
          \"is_hotfix\": false,
          \"pipeline_url\": \"${CI_PIPELINE_URL}\"
        }"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

## Prometheus Metrics Template

```yaml
# prometheus/dora_metrics.yml
groups:
  - name: dora_metrics
    interval: 5m
    rules:
      # Deployment Frequency (deployments per day over last 7 days)
      - record: dora:deployment_frequency:7d
        expr: |
          sum(increase(deployments_total{environment="production"}[7d])) by (service) / 7
        labels:
          metric_type: dora

      # Lead Time for Changes (average in hours)
      - record: dora:lead_time_hours:avg
        expr: |
          avg(deployment_lead_time_seconds) by (service) / 3600
        labels:
          metric_type: dora

      # Change Failure Rate (percentage)
      - record: dora:change_failure_rate:percent
        expr: |
          (
            sum(increase(deployments_failed_total{environment="production"}[30d])) by (service)
            /
            sum(increase(deployments_total{environment="production"}[30d])) by (service)
          ) * 100
        labels:
          metric_type: dora

      # MTTR (mean time to restore in minutes)
      - record: dora:mttr_minutes:avg
        expr: |
          avg(incident_resolution_time_seconds) by (service) / 60
        labels:
          metric_type: dora

      # DORA Rating Rules
      - alert: DORADeploymentFrequencyLow
        expr: dora:deployment_frequency:7d < 0.14  # less than weekly
        for: 7d
        labels:
          severity: warning
        annotations:
          summary: "Low deployment frequency for {{ $labels.service }}"
          description: "Service {{ $labels.service }} has deployment frequency below weekly threshold"

      - alert: DORALeadTimeHigh
        expr: dora:lead_time_hours:avg > 168  # more than 1 week
        for: 7d
        labels:
          severity: warning
        annotations:
          summary: "High lead time for {{ $labels.service }}"
          description: "Service {{ $labels.service }} has lead time exceeding 1 week"

      - alert: DORAChangeFailureRateHigh
        expr: dora:change_failure_rate:percent > 30
        for: 7d
        labels:
          severity: warning
        annotations:
          summary: "High change failure rate for {{ $labels.service }}"
          description: "Service {{ $labels.service }} has CFR above 30%"

      - alert: DORAMTTRHigh
        expr: dora:mttr_minutes:avg > 1440  # more than 1 day
        for: 7d
        labels:
          severity: warning
        annotations:
          summary: "High MTTR for {{ $labels.service }}"
          description: "Service {{ $labels.service }} has MTTR exceeding 1 day"
```

## Grafana Dashboard Template

```json
{
  "dashboard": {
    "title": "DORA Metrics Dashboard",
    "tags": ["dora", "devops", "metrics"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Deployment Frequency (per day)",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "dora:deployment_frequency:7d{service=\"$service\"}",
            "legendFormat": "Deploys/day"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "orange", "value": 0.033},
                {"color": "yellow", "value": 0.14},
                {"color": "green", "value": 1}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Lead Time for Changes",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 0},
        "targets": [
          {
            "expr": "dora:lead_time_hours:avg{service=\"$service\"}",
            "legendFormat": "Hours"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "h",
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 24},
                {"color": "orange", "value": 168},
                {"color": "red", "value": 720}
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "Change Failure Rate",
        "type": "gauge",
        "gridPos": {"h": 4, "w": 6, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "dora:change_failure_rate:percent{service=\"$service\"}",
            "legendFormat": "CFR %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "max": 100,
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 15},
                {"color": "orange", "value": 30},
                {"color": "red", "value": 45}
              ]
            }
          }
        }
      },
      {
        "id": 4,
        "title": "Mean Time to Restore",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 18, "y": 0},
        "targets": [
          {
            "expr": "dora:mttr_minutes:avg{service=\"$service\"}",
            "legendFormat": "Minutes"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "m",
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 60},
                {"color": "orange", "value": 1440},
                {"color": "red", "value": 10080}
              ]
            }
          }
        }
      },
      {
        "id": 5,
        "title": "Deployment Frequency Trend",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4},
        "targets": [
          {
            "expr": "sum(increase(deployments_total{environment=\"production\", service=\"$service\"}[1d]))",
            "legendFormat": "Daily Deployments"
          }
        ]
      },
      {
        "id": 6,
        "title": "Lead Time Distribution",
        "type": "histogram",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4},
        "targets": [
          {
            "expr": "deployment_lead_time_seconds{service=\"$service\"}",
            "legendFormat": "Lead Time"
          }
        ]
      }
    ],
    "templating": {
      "list": [
        {
          "name": "service",
          "type": "query",
          "query": "label_values(deployments_total, service)",
          "refresh": 2
        }
      ]
    }
  }
}
```

## Database Schema Template

```sql
-- PostgreSQL schema for DORA metrics

-- Deployments table
CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    commit_sha VARCHAR(40) NOT NULL,
    commit_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    deployed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'success',
    is_rollback BOOLEAN DEFAULT FALSE,
    is_hotfix BOOLEAN DEFAULT FALSE,
    pipeline_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_status CHECK (status IN ('success', 'failed', 'cancelled'))
);

CREATE INDEX idx_deployments_service ON deployments(service);
CREATE INDEX idx_deployments_deployed_at ON deployments(deployed_at);
CREATE INDEX idx_deployments_service_env ON deployments(service, environment);

-- Incidents table
CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    incident_id VARCHAR(255) UNIQUE NOT NULL,
    service VARCHAR(255) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title TEXT,
    detected_at TIMESTAMP WITH TIME ZONE NOT NULL,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    deployment_id INTEGER REFERENCES deployments(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_severity CHECK (severity IN ('critical', 'high', 'medium', 'low'))
);

CREATE INDEX idx_incidents_service ON incidents(service);
CREATE INDEX idx_incidents_detected_at ON incidents(detected_at);

-- Materialized view for DORA metrics (refresh daily)
CREATE MATERIALIZED VIEW dora_metrics_daily AS
SELECT
    d.service,
    DATE_TRUNC('day', d.deployed_at) AS date,

    -- Deployment Frequency
    COUNT(*) AS deployments_count,

    -- Lead Time (average hours)
    AVG(EXTRACT(EPOCH FROM (d.deployed_at - d.commit_timestamp)) / 3600) AS avg_lead_time_hours,

    -- Change Failure Rate
    COUNT(*) FILTER (WHERE d.is_rollback OR d.is_hotfix OR d.status = 'failed') AS failed_deployments,
    CASE
        WHEN COUNT(*) > 0
        THEN (COUNT(*) FILTER (WHERE d.is_rollback OR d.is_hotfix OR d.status = 'failed')::FLOAT / COUNT(*) * 100)
        ELSE 0
    END AS change_failure_rate,

    -- MTTR (from incidents linked to deployments)
    AVG(EXTRACT(EPOCH FROM (i.resolved_at - i.detected_at)) / 60) AS avg_mttr_minutes

FROM deployments d
LEFT JOIN incidents i ON i.deployment_id = d.id AND i.resolved_at IS NOT NULL
WHERE d.environment = 'production'
GROUP BY d.service, DATE_TRUNC('day', d.deployed_at);

CREATE UNIQUE INDEX idx_dora_metrics_daily ON dora_metrics_daily(service, date);

-- Function to refresh materialized view
CREATE OR REPLACE FUNCTION refresh_dora_metrics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY dora_metrics_daily;
END;
$$ LANGUAGE plpgsql;
```

## Slack Notification Template

```yaml
# slack-dora-notification.yml (use with GitHub Actions)
- name: Send DORA Metrics to Slack
  uses: slackapi/slack-github-action@v1.24.0
  with:
    channel-id: 'C0123456789'
    payload: |
      {
        "blocks": [
          {
            "type": "header",
            "text": {
              "type": "plain_text",
              "text": "Weekly DORA Metrics Report"
            }
          },
          {
            "type": "section",
            "fields": [
              {
                "type": "mrkdwn",
                "text": "*Deployment Frequency:*\n${{ env.DEPLOY_FREQ }} per day"
              },
              {
                "type": "mrkdwn",
                "text": "*Lead Time:*\n${{ env.LEAD_TIME }} hours"
              },
              {
                "type": "mrkdwn",
                "text": "*Change Failure Rate:*\n${{ env.CFR }}%"
              },
              {
                "type": "mrkdwn",
                "text": "*MTTR:*\n${{ env.MTTR }} minutes"
              }
            ]
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "<${{ env.DASHBOARD_URL }}|View Full Dashboard>"
            }
          }
        ]
      }
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

## Weekly Report Email Template

```html
<!-- dora-weekly-report.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    .metric-card { padding: 20px; margin: 10px; border-radius: 8px; display: inline-block; width: 200px; }
    .elite { background-color: #22c55e; color: white; }
    .high { background-color: #84cc16; color: white; }
    .medium { background-color: #eab308; color: black; }
    .low { background-color: #ef4444; color: white; }
    .metric-value { font-size: 32px; font-weight: bold; }
    .metric-label { font-size: 14px; opacity: 0.8; }
  </style>
</head>
<body>
  <h1>DORA Metrics Weekly Report - {{service}}</h1>
  <p>Period: {{start_date}} to {{end_date}}</p>

  <div class="metric-card {{df_rating}}">
    <div class="metric-label">Deployment Frequency</div>
    <div class="metric-value">{{deployment_frequency}}/day</div>
    <div class="metric-label">Rating: {{df_rating}}</div>
  </div>

  <div class="metric-card {{lt_rating}}">
    <div class="metric-label">Lead Time</div>
    <div class="metric-value">{{lead_time}} hrs</div>
    <div class="metric-label">Rating: {{lt_rating}}</div>
  </div>

  <div class="metric-card {{cfr_rating}}">
    <div class="metric-label">Change Failure Rate</div>
    <div class="metric-value">{{cfr}}%</div>
    <div class="metric-label">Rating: {{cfr_rating}}</div>
  </div>

  <div class="metric-card {{mttr_rating}}">
    <div class="metric-label">MTTR</div>
    <div class="metric-value">{{mttr}} min</div>
    <div class="metric-label">Rating: {{mttr_rating}}</div>
  </div>

  <h2>Trends</h2>
  <img src="{{trend_chart_url}}" alt="DORA Metrics Trends" />

  <h2>Recommendations</h2>
  <ul>
    {{#recommendations}}
    <li>{{.}}</li>
    {{/recommendations}}
  </ul>

  <p><a href="{{dashboard_url}}">View Full Dashboard</a></p>
</body>
</html>
```

---

*Reusable templates for DORA metrics implementation across CI/CD, monitoring, and reporting.*
