# DORA Metrics Templates

Ready-to-use templates for tracking and reporting DORA metrics.

---

## Metrics Collection Templates

### Deployment Event Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Deployment Event",
  "type": "object",
  "required": ["id", "service", "timestamp", "status"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique deployment identifier"
    },
    "service": {
      "type": "string",
      "description": "Service/application name"
    },
    "environment": {
      "type": "string",
      "enum": ["production", "staging", "development"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "status": {
      "type": "string",
      "enum": ["success", "failed", "rolled_back"]
    },
    "commit_sha": {
      "type": "string"
    },
    "commit_timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "pr_number": {
      "type": "integer"
    },
    "pr_merged_at": {
      "type": "string",
      "format": "date-time"
    },
    "deployer": {
      "type": "string"
    },
    "triggered_by": {
      "type": "string",
      "enum": ["manual", "automated", "rollback"]
    },
    "duration_seconds": {
      "type": "integer"
    },
    "tags": {
      "type": "object"
    }
  }
}
```

### Incident Event Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Incident Event",
  "type": "object",
  "required": ["id", "service", "created_at", "severity"],
  "properties": {
    "id": {
      "type": "string"
    },
    "service": {
      "type": "string"
    },
    "severity": {
      "type": "string",
      "enum": ["P1", "P2", "P3", "P4"]
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "acknowledged_at": {
      "type": "string",
      "format": "date-time"
    },
    "resolved_at": {
      "type": "string",
      "format": "date-time"
    },
    "caused_by_deployment": {
      "type": "string",
      "description": "Deployment ID that caused the incident"
    },
    "resolution_type": {
      "type": "string",
      "enum": ["rollback", "fix_forward", "config_change", "infrastructure"]
    },
    "description": {
      "type": "string"
    },
    "root_cause": {
      "type": "string"
    }
  }
}
```

---

## Database Schema Templates

### PostgreSQL Schema

```sql
-- DORA Metrics Database Schema

-- Deployments table
CREATE TABLE deployments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service VARCHAR(255) NOT NULL,
    environment VARCHAR(50) NOT NULL DEFAULT 'production',
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(50) NOT NULL,
    commit_sha VARCHAR(40),
    commit_timestamp TIMESTAMPTZ,
    pr_number INTEGER,
    pr_merged_at TIMESTAMPTZ,
    deployer VARCHAR(255),
    triggered_by VARCHAR(50),
    duration_seconds INTEGER,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_deployments_service ON deployments(service);
CREATE INDEX idx_deployments_timestamp ON deployments(timestamp);
CREATE INDEX idx_deployments_status ON deployments(status);

-- Incidents table
CREATE TABLE incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_id VARCHAR(255),
    service VARCHAR(255) NOT NULL,
    severity VARCHAR(10) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    acknowledged_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    caused_by_deployment_id UUID REFERENCES deployments(id),
    resolution_type VARCHAR(50),
    description TEXT,
    root_cause TEXT,
    metadata JSONB
);

CREATE INDEX idx_incidents_service ON incidents(service);
CREATE INDEX idx_incidents_created_at ON incidents(created_at);
CREATE INDEX idx_incidents_severity ON incidents(severity);

-- Reliability metrics table (time series)
CREATE TABLE reliability_metrics (
    id SERIAL PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    availability_percent DECIMAL(5,2),
    error_rate_percent DECIMAL(5,2),
    latency_p50_ms INTEGER,
    latency_p95_ms INTEGER,
    latency_p99_ms INTEGER,
    request_count BIGINT
);

CREATE INDEX idx_reliability_service_time ON reliability_metrics(service, timestamp);

-- DORA metrics summary (materialized view)
CREATE MATERIALIZED VIEW dora_metrics_weekly AS
SELECT
    service,
    date_trunc('week', timestamp) AS week,
    -- Deployment Frequency
    COUNT(*) AS deployments,
    -- Lead Time (median)
    PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY EXTRACT(EPOCH FROM (timestamp - commit_timestamp)) / 3600
    ) AS lead_time_hours_median,
    -- Change Failure Rate
    COUNT(*) FILTER (WHERE status = 'failed' OR status = 'rolled_back')::DECIMAL
        / NULLIF(COUNT(*), 0) * 100 AS change_failure_rate
FROM deployments
WHERE environment = 'production'
GROUP BY service, date_trunc('week', timestamp);

CREATE UNIQUE INDEX idx_dora_weekly ON dora_metrics_weekly(service, week);

-- MTTR calculation view
CREATE VIEW mttr_by_service AS
SELECT
    service,
    date_trunc('week', created_at) AS week,
    COUNT(*) AS incident_count,
    AVG(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 60) AS mttr_minutes,
    PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY EXTRACT(EPOCH FROM (resolved_at - created_at)) / 60
    ) AS mttr_median_minutes
FROM incidents
WHERE resolved_at IS NOT NULL
GROUP BY service, date_trunc('week', created_at);

-- Refresh materialized view (run periodically)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY dora_metrics_weekly;
```

---

## API Response Templates

### DORA Metrics Summary Response

```json
{
  "period": {
    "start": "{{START_DATE}}",
    "end": "{{END_DATE}}",
    "days": 30
  },
  "metrics": {
    "deployment_frequency": {
      "value": {{DEPLOY_COUNT}},
      "unit": "deployments",
      "per_day": {{DEPLOYS_PER_DAY}},
      "trend": "{{TREND}}",
      "performance_tier": "{{TIER}}"
    },
    "lead_time_for_changes": {
      "value": {{LEAD_TIME_HOURS}},
      "unit": "hours",
      "median": {{LEAD_TIME_MEDIAN}},
      "p95": {{LEAD_TIME_P95}},
      "trend": "{{TREND}}",
      "performance_tier": "{{TIER}}"
    },
    "change_failure_rate": {
      "value": {{CFR_PERCENT}},
      "unit": "percent",
      "failed_deployments": {{FAILED_COUNT}},
      "total_deployments": {{TOTAL_COUNT}},
      "trend": "{{TREND}}",
      "performance_tier": "{{TIER}}"
    },
    "time_to_restore": {
      "value": {{MTTR_MINUTES}},
      "unit": "minutes",
      "median": {{MTTR_MEDIAN}},
      "incidents_count": {{INCIDENT_COUNT}},
      "trend": "{{TREND}}",
      "performance_tier": "{{TIER}}"
    },
    "reliability": {
      "availability": {{AVAILABILITY_PERCENT}},
      "error_rate": {{ERROR_RATE_PERCENT}},
      "slo_compliance": {{SLO_COMPLIANCE}},
      "performance_tier": "{{TIER}}"
    }
  },
  "overall_performance": "{{OVERALL_TIER}}",
  "recommendations": [
    "{{RECOMMENDATION_1}}",
    "{{RECOMMENDATION_2}}"
  ]
}
```

---

## Report Templates

### Weekly DORA Report (Markdown)

```markdown
# DORA Metrics Report

**Period:** {{START_DATE}} - {{END_DATE}}
**Team/Service:** {{SERVICE_NAME}}

## Executive Summary

| Metric | Current | Previous | Change | Tier |
|--------|---------|----------|--------|------|
| Deployment Frequency | {{CURRENT_DF}} | {{PREV_DF}} | {{CHANGE_DF}} | {{TIER_DF}} |
| Lead Time for Changes | {{CURRENT_LT}} | {{PREV_LT}} | {{CHANGE_LT}} | {{TIER_LT}} |
| Change Failure Rate | {{CURRENT_CFR}}% | {{PREV_CFR}}% | {{CHANGE_CFR}} | {{TIER_CFR}} |
| Time to Restore | {{CURRENT_MTTR}} | {{PREV_MTTR}} | {{CHANGE_MTTR}} | {{TIER_MTTR}} |
| Reliability | {{CURRENT_REL}}% | {{PREV_REL}}% | {{CHANGE_REL}} | {{TIER_REL}} |

**Overall Performance:** {{OVERALL_TIER}}

## Deployment Frequency

- **Total Deployments:** {{DEPLOY_COUNT}}
- **Average per Day:** {{DEPLOYS_PER_DAY}}
- **Peak Day:** {{PEAK_DAY}} ({{PEAK_COUNT}} deployments)

### Deployment Breakdown

| Environment | Count | Percentage |
|-------------|-------|------------|
| Production | {{PROD_COUNT}} | {{PROD_PCT}}% |
| Staging | {{STAGE_COUNT}} | {{STAGE_PCT}}% |

## Lead Time for Changes

- **Median:** {{LT_MEDIAN}} hours
- **Average:** {{LT_AVG}} hours
- **P95:** {{LT_P95}} hours

### Lead Time Breakdown

| Stage | Time |
|-------|------|
| Commit to PR | {{TIME_COMMIT_PR}} |
| PR Review | {{TIME_REVIEW}} |
| Merge to Deploy | {{TIME_MERGE_DEPLOY}} |
| **Total** | **{{TIME_TOTAL}}** |

## Change Failure Rate

- **Failed Deployments:** {{FAILED_COUNT}} / {{TOTAL_COUNT}}
- **Rate:** {{CFR_PERCENT}}%
- **Rollbacks:** {{ROLLBACK_COUNT}}

### Failure Categories

| Category | Count |
|----------|-------|
| Pipeline Failure | {{CAT_PIPELINE}} |
| Runtime Error | {{CAT_RUNTIME}} |
| Performance Degradation | {{CAT_PERF}} |
| Security Issue | {{CAT_SECURITY}} |

## Time to Restore Service

- **Incidents:** {{INCIDENT_COUNT}}
- **MTTR (Median):** {{MTTR_MEDIAN}} minutes
- **MTTR (Average):** {{MTTR_AVG}} minutes

### Incidents by Severity

| Severity | Count | Avg MTTR |
|----------|-------|----------|
| P1 | {{P1_COUNT}} | {{P1_MTTR}} |
| P2 | {{P2_COUNT}} | {{P2_MTTR}} |
| P3 | {{P3_COUNT}} | {{P3_MTTR}} |

## Reliability

- **Availability:** {{AVAILABILITY}}%
- **Error Rate:** {{ERROR_RATE}}%
- **SLO Compliance:** {{SLO_COMPLIANCE}}%

## Recommendations

1. {{RECOMMENDATION_1}}
2. {{RECOMMENDATION_2}}
3. {{RECOMMENDATION_3}}

## Action Items

- [ ] {{ACTION_1}}
- [ ] {{ACTION_2}}
- [ ] {{ACTION_3}}

---

*Generated: {{TIMESTAMP}}*
```

---

## Configuration Templates

### DORA Metrics Config (YAML)

```yaml
# dora-metrics-config.yaml
version: "1.0"

organization: "{{ORG_NAME}}"

services:
  - name: "{{SERVICE_NAME}}"
    repository: "{{REPO_URL}}"
    production_branch: "main"
    deployment_environments:
      - production

targets:
  deployment_frequency:
    elite: 7        # 7+ per week
    high: 1         # 1+ per week
    medium: 0.25    # 1+ per month

  lead_time_hours:
    elite: 1
    high: 24
    medium: 168     # 1 week

  change_failure_rate_percent:
    elite: 15
    high: 30
    medium: 45

  mttr_minutes:
    elite: 60
    high: 1440      # 1 day
    medium: 10080   # 1 week

  reliability_percent:
    elite: 99.9
    high: 99.5
    medium: 99.0

data_sources:
  deployments:
    type: "github"
    config:
      owner: "{{GITHUB_OWNER}}"
      repo: "{{GITHUB_REPO}}"
      token_env: "GITHUB_TOKEN"

  incidents:
    type: "pagerduty"
    config:
      service_ids:
        - "{{PAGERDUTY_SERVICE_ID}}"
      token_env: "PAGERDUTY_TOKEN"

  metrics:
    type: "prometheus"
    config:
      url: "{{PROMETHEUS_URL}}"

notifications:
  slack:
    webhook_url_env: "SLACK_WEBHOOK_URL"
    channel: "#dora-metrics"

  weekly_report:
    enabled: true
    day: "monday"
    time: "09:00"
    recipients:
      - "{{EMAIL_1}}"
      - "{{EMAIL_2}}"
```

---

## Terraform Templates

### DORA Metrics Infrastructure

```hcl
# dora-metrics-infra.tf

variable "project_name" {
  default = "dora-metrics"
}

# TimescaleDB for time-series metrics
resource "kubernetes_deployment" "timescaledb" {
  metadata {
    name = "${var.project_name}-db"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "${var.project_name}-db"
      }
    }
    template {
      metadata {
        labels = {
          app = "${var.project_name}-db"
        }
      }
      spec {
        container {
          name  = "timescaledb"
          image = "timescale/timescaledb:latest-pg15"
          port {
            container_port = 5432
          }
          env {
            name  = "POSTGRES_DB"
            value = "dora_metrics"
          }
          env {
            name = "POSTGRES_PASSWORD"
            value_from {
              secret_key_ref {
                name = "${var.project_name}-secrets"
                key  = "db-password"
              }
            }
          }
          volume_mount {
            name       = "data"
            mount_path = "/var/lib/postgresql/data"
          }
        }
        volume {
          name = "data"
          persistent_volume_claim {
            claim_name = "${var.project_name}-db-pvc"
          }
        }
      }
    }
  }
}

# Grafana for dashboards
resource "kubernetes_deployment" "grafana" {
  metadata {
    name = "${var.project_name}-grafana"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "${var.project_name}-grafana"
      }
    }
    template {
      metadata {
        labels = {
          app = "${var.project_name}-grafana"
        }
      }
      spec {
        container {
          name  = "grafana"
          image = "grafana/grafana:latest"
          port {
            container_port = 3000
          }
          env {
            name  = "GF_SECURITY_ADMIN_PASSWORD"
            value_from {
              secret_key_ref {
                name = "${var.project_name}-secrets"
                key  = "grafana-password"
              }
            }
          }
          volume_mount {
            name       = "dashboards"
            mount_path = "/var/lib/grafana/dashboards"
          }
        }
        volume {
          name = "dashboards"
          config_map {
            name = "${var.project_name}-dashboards"
          }
        }
      }
    }
  }
}
```

---

## GitHub Actions Template

### DORA Metrics Collection Workflow

```yaml
# .github/workflows/dora-metrics.yml
name: DORA Metrics Collection

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  collect-metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests python-dateutil

      - name: Collect Deployment Frequency
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/collect_deployments.py \
            --repo ${{ github.repository }} \
            --days 30 \
            --output deployments.json

      - name: Calculate Lead Time
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/calculate_lead_time.py \
            --repo ${{ github.repository }} \
            --days 30 \
            --output lead_time.json

      - name: Collect Incidents
        env:
          PAGERDUTY_TOKEN: ${{ secrets.PAGERDUTY_TOKEN }}
        run: |
          python scripts/collect_incidents.py \
            --service-id ${{ vars.PAGERDUTY_SERVICE_ID }} \
            --days 30 \
            --output incidents.json

      - name: Calculate Metrics
        run: |
          python scripts/calculate_dora_metrics.py \
            --deployments deployments.json \
            --incidents incidents.json \
            --lead-time lead_time.json \
            --output dora_metrics.json

      - name: Upload to Metrics Store
        env:
          METRICS_API_TOKEN: ${{ secrets.METRICS_API_TOKEN }}
        run: |
          curl -X POST "${{ vars.METRICS_API_URL }}/metrics" \
            -H "Authorization: Bearer $METRICS_API_TOKEN" \
            -H "Content-Type: application/json" \
            -d @dora_metrics.json

      - name: Generate Report
        run: |
          python scripts/generate_report.py \
            --metrics dora_metrics.json \
            --template templates/weekly_report.md \
            --output report.md

      - name: Post to Slack
        if: github.event_name == 'schedule'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          python scripts/post_to_slack.py \
            --report report.md \
            --webhook "$SLACK_WEBHOOK_URL"
```

---

## Template Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{{ORG_NAME}}` | Organization name | Acme Corp |
| `{{SERVICE_NAME}}` | Service/application name | api-gateway |
| `{{START_DATE}}` | Report period start | 2025-01-01 |
| `{{END_DATE}}` | Report period end | 2025-01-31 |
| `{{DEPLOY_COUNT}}` | Number of deployments | 45 |
| `{{DEPLOYS_PER_DAY}}` | Average deployments/day | 1.5 |
| `{{LEAD_TIME_HOURS}}` | Lead time in hours | 4.5 |
| `{{CFR_PERCENT}}` | Change failure rate % | 8.5 |
| `{{MTTR_MINUTES}}` | Mean time to restore | 45 |
| `{{AVAILABILITY_PERCENT}}` | Uptime percentage | 99.95 |
| `{{TIER}}` | Performance tier | Elite/High/Medium/Low |
| `{{TREND}}` | Metric trend | improving/stable/declining |

---

## Sources

- [DORA Metrics Four Keys](https://dora.dev/guides/dora-metrics-four-keys/)
- [GitHub Deployments API](https://docs.github.com/en/rest/deployments)
- [PagerDuty Incidents API](https://developer.pagerduty.com/api-reference/)
- [Grafana Dashboard as Code](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/view-dashboard-json-model/)
