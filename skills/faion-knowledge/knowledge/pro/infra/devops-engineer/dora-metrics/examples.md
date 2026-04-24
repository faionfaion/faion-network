# DORA Metrics Examples

Practical examples for measuring, querying, and visualizing DORA metrics.

---

## Data Collection Examples

### Deployment Frequency

#### GitHub Actions Workflow (Capture Deploys)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        run: ./deploy.sh

      - name: Record Deployment
        if: success()
        run: |
          curl -X POST "https://metrics-api.example.com/deployments" \
            -H "Authorization: Bearer ${{ secrets.METRICS_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{
              "service": "${{ github.repository }}",
              "commit": "${{ github.sha }}",
              "timestamp": "${{ github.event.head_commit.timestamp }}",
              "deployer": "${{ github.actor }}",
              "status": "success"
            }'

      - name: Create GitHub Deployment
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.repos.createDeployment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: context.sha,
              environment: 'production',
              auto_merge: false,
              required_contexts: []
            });
```

#### Kubernetes Deployment Tracking

```yaml
# ArgoCD PostSync Hook
apiVersion: batch/v1
kind: Job
metadata:
  name: record-deployment
  annotations:
    argocd.argoproj.io/hook: PostSync
spec:
  template:
    spec:
      containers:
      - name: record
        image: curlimages/curl:latest
        command:
        - sh
        - -c
        - |
          curl -X POST "https://metrics-api.example.com/deployments" \
            -H "Content-Type: application/json" \
            -d "{
              \"service\": \"${APP_NAME}\",
              \"version\": \"${IMAGE_TAG}\",
              \"timestamp\": \"$(date -Iseconds)\",
              \"cluster\": \"${CLUSTER_NAME}\",
              \"namespace\": \"${NAMESPACE}\"
            }"
        env:
        - name: APP_NAME
          value: "myapp"
        - name: IMAGE_TAG
          value: "{{.Values.image.tag}}"
      restartPolicy: Never
```

---

### Lead Time for Changes

#### Git Commit to Deploy Time

```python
# lead_time_calculator.py
import subprocess
import json
from datetime import datetime

def calculate_lead_time(repo_path: str, deploy_sha: str) -> dict:
    """Calculate lead time from first commit to deployment."""

    # Get merge commit info
    merge_info = subprocess.run(
        ["git", "log", "-1", "--format=%H|%aI", deploy_sha],
        cwd=repo_path, capture_output=True, text=True
    )
    deploy_sha, deploy_time = merge_info.stdout.strip().split("|")
    deploy_dt = datetime.fromisoformat(deploy_time)

    # Get first commit in the PR (parent~1..HEAD)
    first_commit = subprocess.run(
        ["git", "log", "--reverse", "--format=%H|%aI", f"{deploy_sha}~10..{deploy_sha}"],
        cwd=repo_path, capture_output=True, text=True
    )

    commits = first_commit.stdout.strip().split("\n")
    if commits and commits[0]:
        first_sha, first_time = commits[0].split("|")
        first_dt = datetime.fromisoformat(first_time)
        lead_time = (deploy_dt - first_dt).total_seconds()
    else:
        lead_time = 0

    return {
        "deploy_sha": deploy_sha,
        "deploy_time": deploy_time,
        "first_commit_time": first_time if commits else deploy_time,
        "lead_time_seconds": lead_time,
        "lead_time_hours": lead_time / 3600
    }

# Example usage
result = calculate_lead_time("/path/to/repo", "abc123")
print(f"Lead time: {result['lead_time_hours']:.2f} hours")
```

#### GitHub API Lead Time Query

```bash
#!/bin/bash
# lead_time.sh - Calculate lead time for merged PRs

REPO="owner/repo"
DAYS=30

# Get merged PRs in last N days
gh pr list --repo $REPO --state merged --limit 100 --json number,mergedAt,commits \
  | jq --argjson days $DAYS '
    [.[] |
      select((.mergedAt | fromdateiso8601) > (now - ($days * 86400))) |
      {
        pr: .number,
        merged_at: .mergedAt,
        first_commit: .commits[0].committedDate,
        lead_time_hours: ((.mergedAt | fromdateiso8601) - (.commits[0].committedDate | fromdateiso8601)) / 3600
      }
    ]'
```

---

### Change Failure Rate

#### Incident-Deployment Correlation

```python
# cfr_calculator.py
from datetime import datetime, timedelta
from typing import List, Dict

def calculate_cfr(
    deployments: List[Dict],
    incidents: List[Dict],
    correlation_window_hours: int = 24
) -> Dict:
    """
    Calculate Change Failure Rate by correlating incidents with deployments.

    Args:
        deployments: List of {timestamp, service, sha}
        incidents: List of {timestamp, service, severity}
        correlation_window_hours: Time window to associate incident with deployment
    """

    window = timedelta(hours=correlation_window_hours)
    failed_deployments = set()

    for incident in incidents:
        incident_time = datetime.fromisoformat(incident["timestamp"])
        service = incident["service"]

        # Find deployments within window before incident
        for deploy in deployments:
            if deploy["service"] != service:
                continue

            deploy_time = datetime.fromisoformat(deploy["timestamp"])

            if 0 <= (incident_time - deploy_time).total_seconds() <= window.total_seconds():
                failed_deployments.add((deploy["sha"], deploy["timestamp"]))

    total_deployments = len(deployments)
    failed_count = len(failed_deployments)

    return {
        "total_deployments": total_deployments,
        "failed_deployments": failed_count,
        "change_failure_rate": (failed_count / total_deployments * 100) if total_deployments > 0 else 0,
        "failed_shas": [sha for sha, _ in failed_deployments]
    }

# Example usage
deployments = [
    {"timestamp": "2025-01-20T10:00:00Z", "service": "api", "sha": "abc123"},
    {"timestamp": "2025-01-21T14:00:00Z", "service": "api", "sha": "def456"},
    {"timestamp": "2025-01-22T09:00:00Z", "service": "api", "sha": "ghi789"},
]

incidents = [
    {"timestamp": "2025-01-21T16:30:00Z", "service": "api", "severity": "P2"},
]

result = calculate_cfr(deployments, incidents)
print(f"CFR: {result['change_failure_rate']:.1f}%")
```

#### PagerDuty Incident Query

```bash
#!/bin/bash
# Query incidents from PagerDuty

START_DATE=$(date -d "30 days ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

curl -s --request GET \
  --url "https://api.pagerduty.com/incidents?since=${START_DATE}&until=${END_DATE}&statuses[]=resolved" \
  --header "Authorization: Token token=${PAGERDUTY_TOKEN}" \
  --header "Content-Type: application/json" \
  | jq '.incidents | group_by(.service.summary) |
      map({
        service: .[0].service.summary,
        incident_count: length,
        avg_resolution_minutes: ([.[].resolved_at, .[].created_at] |
          map(fromdateiso8601) |
          [.[0] - .[1]] | add / length / 60)
      })'
```

---

### Time to Restore Service (MTTR)

#### Incident Resolution Time

```python
# mttr_calculator.py
from datetime import datetime
from typing import List, Dict
import statistics

def calculate_mttr(incidents: List[Dict]) -> Dict:
    """
    Calculate Mean Time to Restore from incident data.

    Args:
        incidents: List of {created_at, resolved_at, severity, service}
    """

    resolution_times = []
    by_severity = {}

    for incident in incidents:
        if not incident.get("resolved_at"):
            continue

        created = datetime.fromisoformat(incident["created_at"])
        resolved = datetime.fromisoformat(incident["resolved_at"])
        duration_minutes = (resolved - created).total_seconds() / 60

        resolution_times.append(duration_minutes)

        severity = incident.get("severity", "unknown")
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(duration_minutes)

    return {
        "total_incidents": len(incidents),
        "resolved_incidents": len(resolution_times),
        "mttr_minutes": statistics.mean(resolution_times) if resolution_times else 0,
        "mttr_median_minutes": statistics.median(resolution_times) if resolution_times else 0,
        "mttr_p95_minutes": sorted(resolution_times)[int(len(resolution_times) * 0.95)] if len(resolution_times) > 20 else max(resolution_times, default=0),
        "by_severity": {
            sev: {
                "count": len(times),
                "mttr_minutes": statistics.mean(times)
            }
            for sev, times in by_severity.items()
        }
    }

# Example
incidents = [
    {"created_at": "2025-01-20T10:00:00Z", "resolved_at": "2025-01-20T10:30:00Z", "severity": "P2"},
    {"created_at": "2025-01-21T14:00:00Z", "resolved_at": "2025-01-21T14:15:00Z", "severity": "P3"},
    {"created_at": "2025-01-22T09:00:00Z", "resolved_at": "2025-01-22T11:00:00Z", "severity": "P1"},
]

result = calculate_mttr(incidents)
print(f"MTTR: {result['mttr_minutes']:.1f} minutes")
```

---

### Reliability Metrics

#### SLO Tracking

```python
# reliability_calculator.py
from datetime import datetime, timedelta
from typing import List, Dict

def calculate_reliability(
    availability_data: List[Dict],  # {timestamp, uptime_percent}
    error_data: List[Dict],         # {timestamp, error_count, total_requests}
    latency_data: List[Dict],       # {timestamp, p50, p95, p99}
    slo_targets: Dict
) -> Dict:
    """Calculate reliability metrics against SLO targets."""

    # Availability
    avg_availability = sum(d["uptime_percent"] for d in availability_data) / len(availability_data)
    availability_met = avg_availability >= slo_targets.get("availability", 99.9)

    # Error rate
    total_errors = sum(d["error_count"] for d in error_data)
    total_requests = sum(d["total_requests"] for d in error_data)
    error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
    error_rate_met = error_rate <= slo_targets.get("error_rate", 1.0)

    # Latency
    avg_p99 = sum(d["p99"] for d in latency_data) / len(latency_data)
    latency_met = avg_p99 <= slo_targets.get("latency_p99_ms", 500)

    return {
        "availability": {
            "value": avg_availability,
            "target": slo_targets.get("availability", 99.9),
            "met": availability_met
        },
        "error_rate": {
            "value": error_rate,
            "target": slo_targets.get("error_rate", 1.0),
            "met": error_rate_met
        },
        "latency_p99": {
            "value": avg_p99,
            "target": slo_targets.get("latency_p99_ms", 500),
            "met": latency_met
        },
        "overall_reliability": availability_met and error_rate_met and latency_met,
        "reliability_score": sum([availability_met, error_rate_met, latency_met]) / 3 * 100
    }
```

---

## Prometheus/Grafana Queries

### Deployment Frequency

```promql
# Deployments per day (using deployment annotations)
sum(increase(deployment_total[1d])) by (service)

# Deployments per week
sum(increase(deployment_total[7d])) by (service)

# Average deployments per day over 30 days
avg_over_time(sum(increase(deployment_total[1d]))[30d:1d])
```

### Change Failure Rate

```promql
# CFR from deployment success/failure
sum(deployment_total{status="failed"}) / sum(deployment_total) * 100

# CFR per service
sum by (service) (deployment_total{status="failed"})
/ sum by (service) (deployment_total) * 100

# CFR trend (7-day rolling)
sum(increase(deployment_total{status="failed"}[7d]))
/ sum(increase(deployment_total[7d])) * 100
```

### Time to Restore

```promql
# Average incident duration
avg(incident_duration_seconds) / 60

# MTTR by severity
avg by (severity) (incident_duration_seconds) / 60

# MTTR trend (30-day rolling average)
avg_over_time(avg(incident_duration_seconds)[30d:1d]) / 60
```

### Reliability

```promql
# Availability (from up metric)
avg_over_time(up{job="myapp"}[30d]) * 100

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m])) * 100

# Latency P99
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# SLO compliance (availability > 99.9%)
(avg_over_time(up{job="myapp"}[30d]) > 0.999) * 100
```

---

## Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "DORA Metrics Dashboard",
    "panels": [
      {
        "title": "Deployment Frequency",
        "type": "stat",
        "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "sum(increase(deployment_total[7d]))",
          "legendFormat": "Deployments/Week"
        }],
        "options": {
          "colorMode": "value",
          "graphMode": "area"
        },
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 1},
                {"color": "green", "value": 7}
              ]
            }
          }
        }
      },
      {
        "title": "Lead Time for Changes",
        "type": "stat",
        "gridPos": {"x": 6, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "avg(lead_time_hours)",
          "legendFormat": "Hours"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "h",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 24},
                {"color": "red", "value": 168}
              ]
            }
          }
        }
      },
      {
        "title": "Change Failure Rate",
        "type": "gauge",
        "gridPos": {"x": 12, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "sum(deployment_total{status=\"failed\"}) / sum(deployment_total) * 100"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 0,
            "max": 100,
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 15},
                {"color": "red", "value": 30}
              ]
            }
          }
        }
      },
      {
        "title": "Time to Restore (MTTR)",
        "type": "stat",
        "gridPos": {"x": 18, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "avg(incident_duration_seconds) / 60"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "m",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 60},
                {"color": "red", "value": 1440}
              ]
            }
          }
        }
      },
      {
        "title": "Reliability (Availability)",
        "type": "gauge",
        "gridPos": {"x": 0, "y": 4, "w": 6, "h": 4},
        "targets": [{
          "expr": "avg_over_time(up{job=\"myapp\"}[30d]) * 100"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 95,
            "max": 100,
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 99},
                {"color": "green", "value": 99.9}
              ]
            }
          }
        }
      },
      {
        "title": "Deployment Frequency Trend",
        "type": "timeseries",
        "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8},
        "targets": [{
          "expr": "sum(increase(deployment_total[1d])) by (service)",
          "legendFormat": "{{service}}"
        }]
      },
      {
        "title": "Lead Time Trend",
        "type": "timeseries",
        "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8},
        "targets": [{
          "expr": "avg(lead_time_hours) by (service)",
          "legendFormat": "{{service}}"
        }]
      }
    ]
  }
}
```

---

## CLI Commands for Quick Metrics

### GitHub CLI

```bash
# Deployment frequency (GitHub Deployments)
gh api repos/{owner}/{repo}/deployments --jq 'length'

# Recent deployments
gh api repos/{owner}/{repo}/deployments \
  --jq '.[] | {id, ref, created_at, environment}'

# PR lead time (merged PRs in last 30 days)
gh pr list --state merged --limit 50 --json number,createdAt,mergedAt \
  | jq '[.[] | {
      pr: .number,
      created: .createdAt,
      merged: .mergedAt,
      hours: ((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 3600
    }] |
    {
      avg_hours: (map(.hours) | add / length),
      median_hours: (sort_by(.hours) | .[length/2 | floor].hours)
    }'

# Workflow failure rate
gh run list --limit 100 --json conclusion \
  | jq 'group_by(.conclusion) |
    map({conclusion: .[0].conclusion, count: length}) |
    (map(select(.conclusion == "failure").count)[0] // 0) /
    (map(.count) | add) * 100 |
    "Failure rate: \(.)%"'
```

### GitLab CLI

```bash
# Deployment frequency
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/{id}/deployments?per_page=100" \
  | jq 'length'

# Pipeline success rate
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/{id}/pipelines?per_page=100" \
  | jq 'group_by(.status) |
    map({status: .[0].status, count: length})'
```

---

## Sources

- [DORA Official Metrics Guide](https://dora.dev/guides/dora-metrics-four-keys/)
- [GitHub REST API Deployments](https://docs.github.com/en/rest/deployments)
- [Prometheus Querying Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/)
