# DORA Metrics Examples

## Deployment Frequency Tracking

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Deploy Application
        run: ./deploy.sh

      - name: Record Deployment Event
        if: success()
        run: |
          curl -X POST "${{ secrets.METRICS_ENDPOINT }}/deployments" \
            -H "Content-Type: application/json" \
            -d '{
              "service": "${{ github.repository }}",
              "environment": "production",
              "commit_sha": "${{ github.sha }}",
              "deployed_at": "${{ github.event.head_commit.timestamp }}",
              "status": "success"
            }'
```

### GitLab CI

```yaml
# .gitlab-ci.yml
deploy_production:
  stage: deploy
  environment:
    name: production
    url: https://app.example.com
  script:
    - ./deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  after_script:
    - |
      curl -X POST "$METRICS_ENDPOINT/deployments" \
        -H "Content-Type: application/json" \
        -d "{
          \"service\": \"$CI_PROJECT_NAME\",
          \"environment\": \"production\",
          \"commit_sha\": \"$CI_COMMIT_SHA\",
          \"deployed_at\": \"$(date -Iseconds)\",
          \"pipeline_id\": \"$CI_PIPELINE_ID\"
        }"
```

## Lead Time Calculation

### Prometheus Query

```promql
# Average lead time in hours (last 7 days)
avg(
  deployment_timestamp - commit_timestamp
) by (service) / 3600

# Lead time percentiles
histogram_quantile(0.50,
  sum(rate(lead_time_seconds_bucket[7d])) by (le, service)
)

histogram_quantile(0.95,
  sum(rate(lead_time_seconds_bucket[7d])) by (le, service)
)
```

### Python Calculation

```python
from datetime import datetime
from typing import List, Dict
import statistics

def calculate_lead_time(deployments: List[Dict]) -> Dict:
    """
    Calculate lead time metrics from deployment data.

    Each deployment dict should have:
    - commit_timestamp: ISO datetime string
    - deployment_timestamp: ISO datetime string
    """
    lead_times = []

    for deploy in deployments:
        commit_time = datetime.fromisoformat(deploy['commit_timestamp'])
        deploy_time = datetime.fromisoformat(deploy['deployment_timestamp'])
        lead_time_hours = (deploy_time - commit_time).total_seconds() / 3600
        lead_times.append(lead_time_hours)

    if not lead_times:
        return {"error": "No deployments"}

    return {
        "mean_hours": statistics.mean(lead_times),
        "median_hours": statistics.median(lead_times),
        "p95_hours": statistics.quantiles(lead_times, n=20)[18] if len(lead_times) >= 20 else max(lead_times),
        "min_hours": min(lead_times),
        "max_hours": max(lead_times),
        "sample_size": len(lead_times)
    }
```

## Change Failure Rate

### Database Schema

```sql
-- Deployments table
CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    commit_sha VARCHAR(40) NOT NULL,
    deployed_at TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'success',
    is_rollback BOOLEAN DEFAULT FALSE,
    is_hotfix BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Change failure rate query
SELECT
    service,
    DATE_TRUNC('week', deployed_at) AS week,
    COUNT(*) FILTER (WHERE is_rollback OR is_hotfix) AS failed_deployments,
    COUNT(*) AS total_deployments,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_rollback OR is_hotfix) / COUNT(*),
        2
    ) AS change_failure_rate
FROM deployments
WHERE environment = 'production'
  AND deployed_at >= NOW() - INTERVAL '30 days'
GROUP BY service, DATE_TRUNC('week', deployed_at)
ORDER BY week DESC;
```

### API Endpoint

```python
from fastapi import FastAPI, Query
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/metrics/change-failure-rate")
async def get_change_failure_rate(
    service: str = Query(...),
    days: int = Query(30, ge=1, le=365)
):
    """Calculate change failure rate for a service."""

    start_date = datetime.utcnow() - timedelta(days=days)

    # Query deployments
    total = await db.deployments.count({
        "service": service,
        "environment": "production",
        "deployed_at": {"$gte": start_date}
    })

    failed = await db.deployments.count({
        "service": service,
        "environment": "production",
        "deployed_at": {"$gte": start_date},
        "$or": [
            {"is_rollback": True},
            {"is_hotfix": True},
            {"caused_incident": True}
        ]
    })

    rate = (failed / total * 100) if total > 0 else 0

    return {
        "service": service,
        "period_days": days,
        "total_deployments": total,
        "failed_deployments": failed,
        "change_failure_rate": round(rate, 2),
        "rating": classify_cfr(rate)
    }

def classify_cfr(rate: float) -> str:
    if rate <= 15:
        return "elite"
    elif rate <= 30:
        return "high"
    elif rate <= 45:
        return "medium"
    return "low"
```

## MTTR Tracking

### Incident Integration (PagerDuty)

```python
import requests
from datetime import datetime

def fetch_pagerduty_incidents(api_key: str, service_id: str, since: str):
    """Fetch incidents from PagerDuty API."""

    headers = {
        "Authorization": f"Token token={api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        "https://api.pagerduty.com/incidents",
        headers=headers,
        params={
            "service_ids[]": service_id,
            "since": since,
            "statuses[]": "resolved"
        }
    )

    incidents = response.json()["incidents"]

    mttr_data = []
    for incident in incidents:
        created = datetime.fromisoformat(incident["created_at"].replace("Z", "+00:00"))
        resolved = datetime.fromisoformat(incident["resolved_at"].replace("Z", "+00:00"))
        mttr_minutes = (resolved - created).total_seconds() / 60

        mttr_data.append({
            "incident_id": incident["id"],
            "title": incident["title"],
            "severity": incident["urgency"],
            "created_at": incident["created_at"],
            "resolved_at": incident["resolved_at"],
            "mttr_minutes": mttr_minutes
        })

    return mttr_data
```

### Grafana Dashboard JSON

```json
{
  "panels": [
    {
      "title": "Mean Time to Restore (MTTR)",
      "type": "timeseries",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "avg(incident_resolution_time_seconds) by (service) / 60",
          "legendFormat": "{{service}} (minutes)"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "m",
          "thresholds": {
            "mode": "absolute",
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
      "title": "Deployment Frequency",
      "type": "stat",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum(increase(deployments_total{environment=\"production\"}[7d]))",
          "legendFormat": "Deployments (7d)"
        }
      ]
    },
    {
      "title": "Change Failure Rate",
      "type": "gauge",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum(deployments_failed_total) / sum(deployments_total) * 100",
          "legendFormat": "CFR %"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "max": 100,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": 0},
              {"color": "yellow", "value": 15},
              {"color": "orange", "value": 30},
              {"color": "red", "value": 45}
            ]
          }
        }
      }
    }
  ]
}
```

## Complete Metrics Service

### FastAPI Service

```python
# dora_metrics_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import asyncpg

app = FastAPI(title="DORA Metrics Service")

class DeploymentEvent(BaseModel):
    service: str
    environment: str
    commit_sha: str
    commit_timestamp: datetime
    deployed_at: datetime
    is_rollback: bool = False
    is_hotfix: bool = False

class IncidentEvent(BaseModel):
    incident_id: str
    service: str
    severity: str
    detected_at: datetime
    resolved_at: Optional[datetime] = None

@app.post("/events/deployment")
async def record_deployment(event: DeploymentEvent):
    """Record a deployment event."""
    await db.execute("""
        INSERT INTO deployments
        (service, environment, commit_sha, commit_timestamp, deployed_at, is_rollback, is_hotfix)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """, event.service, event.environment, event.commit_sha,
       event.commit_timestamp, event.deployed_at, event.is_rollback, event.is_hotfix)
    return {"status": "recorded"}

@app.post("/events/incident")
async def record_incident(event: IncidentEvent):
    """Record an incident event."""
    await db.execute("""
        INSERT INTO incidents (incident_id, service, severity, detected_at, resolved_at)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (incident_id) DO UPDATE SET resolved_at = $5
    """, event.incident_id, event.service, event.severity,
       event.detected_at, event.resolved_at)
    return {"status": "recorded"}

@app.get("/metrics/dora/{service}")
async def get_dora_metrics(service: str, days: int = 30):
    """Get all DORA metrics for a service."""

    start_date = datetime.utcnow() - timedelta(days=days)

    # Deployment Frequency
    df_result = await db.fetchrow("""
        SELECT COUNT(*) as count
        FROM deployments
        WHERE service = $1 AND environment = 'production'
          AND deployed_at >= $2
    """, service, start_date)
    deployment_frequency = df_result['count'] / days

    # Lead Time
    lt_result = await db.fetchrow("""
        SELECT
            AVG(EXTRACT(EPOCH FROM (deployed_at - commit_timestamp))) as avg_seconds,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (deployed_at - commit_timestamp))) as median_seconds
        FROM deployments
        WHERE service = $1 AND environment = 'production'
          AND deployed_at >= $2
    """, service, start_date)

    # Change Failure Rate
    cfr_result = await db.fetchrow("""
        SELECT
            COUNT(*) FILTER (WHERE is_rollback OR is_hotfix) as failed,
            COUNT(*) as total
        FROM deployments
        WHERE service = $1 AND environment = 'production'
          AND deployed_at >= $2
    """, service, start_date)
    cfr = (cfr_result['failed'] / cfr_result['total'] * 100) if cfr_result['total'] > 0 else 0

    # MTTR
    mttr_result = await db.fetchrow("""
        SELECT AVG(EXTRACT(EPOCH FROM (resolved_at - detected_at))) / 60 as avg_minutes
        FROM incidents
        WHERE service = $1 AND resolved_at IS NOT NULL
          AND detected_at >= $2
    """, service, start_date)

    return {
        "service": service,
        "period_days": days,
        "metrics": {
            "deployment_frequency": {
                "value": round(deployment_frequency, 2),
                "unit": "per_day",
                "rating": classify_df(deployment_frequency)
            },
            "lead_time": {
                "mean_hours": round(lt_result['avg_seconds'] / 3600, 2) if lt_result['avg_seconds'] else None,
                "median_hours": round(lt_result['median_seconds'] / 3600, 2) if lt_result['median_seconds'] else None,
                "rating": classify_lt(lt_result['avg_seconds'] / 3600) if lt_result['avg_seconds'] else None
            },
            "change_failure_rate": {
                "value": round(cfr, 2),
                "unit": "percent",
                "rating": classify_cfr(cfr)
            },
            "mttr": {
                "value": round(mttr_result['avg_minutes'], 2) if mttr_result['avg_minutes'] else None,
                "unit": "minutes",
                "rating": classify_mttr(mttr_result['avg_minutes']) if mttr_result['avg_minutes'] else None
            }
        }
    }

def classify_df(deploys_per_day: float) -> str:
    if deploys_per_day >= 1:
        return "elite"
    elif deploys_per_day >= 1/7:  # weekly
        return "high"
    elif deploys_per_day >= 1/30:  # monthly
        return "medium"
    return "low"

def classify_lt(hours: float) -> str:
    if hours < 1:
        return "elite"
    elif hours < 24 * 7:  # 1 week
        return "high"
    elif hours < 24 * 30 * 6:  # 6 months
        return "medium"
    return "low"

def classify_cfr(rate: float) -> str:
    if rate <= 15:
        return "elite"
    elif rate <= 30:
        return "high"
    elif rate <= 45:
        return "medium"
    return "low"

def classify_mttr(minutes: float) -> str:
    if minutes < 60:
        return "elite"
    elif minutes < 60 * 24:  # 1 day
        return "high"
    elif minutes < 60 * 24 * 7:  # 1 week
        return "medium"
    return "low"
```

## Four Keys Open Source Setup

### Docker Compose

```yaml
# docker-compose.yml for Google Four Keys
version: '3.8'

services:
  fourkeys-parser:
    image: gcr.io/four-keys/event-parser:latest
    environment:
      - PROJECT_NAME=my-project
      - PARSERS=github,pagerduty
    ports:
      - "8080:8080"

  fourkeys-bq-worker:
    image: gcr.io/four-keys/bq-worker:latest
    environment:
      - PROJECT_NAME=my-project
      - BIGQUERY_DATASET=four_keys
    depends_on:
      - fourkeys-parser

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/dashboards:/var/lib/grafana/dashboards
      - ./grafana/provisioning:/etc/grafana/provisioning
```

---

*Examples for implementing DORA metrics tracking across different tools and platforms.*
