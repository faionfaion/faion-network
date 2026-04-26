# Grafana Setup LLM Prompts

## Overview

AI-assisted prompts for Grafana setup, configuration, troubleshooting, and optimization tasks.

---

## Installation & Setup Prompts

### Docker Compose Setup

```
Create a Docker Compose configuration for a Grafana monitoring stack with:
- Grafana (latest stable version)
- Prometheus for metrics
- Loki for logs
- Grafana Alloy for data collection

Requirements:
- Persistent storage for all services
- Provisioning directory structure for dashboards and data sources
- Environment variables for sensitive configuration
- Health checks for all services
- Resource limits appropriate for [development/production]

Target environment: [describe infrastructure]
```

### Kubernetes Helm Deployment

```
Generate Helm values.yaml for deploying Grafana on Kubernetes with:
- [N] replicas for high availability
- PostgreSQL database backend (external)
- Ingress with TLS via cert-manager
- OAuth authentication via [provider: Keycloak/Okta/Azure AD]
- Persistent volume for plugins

Cluster: [EKS/GKE/AKS/on-prem]
Existing services: [list existing services in cluster]
```

### High Availability Setup

```
Design a high availability Grafana deployment for production:
- Target availability: 99.9%
- Expected concurrent users: [N]
- Geographic distribution: [single region/multi-region]

Include:
1. Database configuration (PostgreSQL HA)
2. Load balancer setup
3. Alerting HA configuration
4. Shared storage requirements
5. Disaster recovery plan
```

---

## Configuration Prompts

### Data Source Provisioning

```
Create Grafana data source provisioning YAML for:
- Primary: [Prometheus/Mimir/Cortex] at [URL]
- Logs: [Loki/Elasticsearch] at [URL]
- Traces: [Tempo/Jaeger] at [URL]
- Database: [PostgreSQL/MySQL] for application queries

Requirements:
- Enable alerting on metrics data source
- Configure derived fields for log-to-trace correlation
- Set appropriate timeout and connection limits
- Use environment variables for credentials
```

### Dashboard Provisioning

```
Set up dashboard provisioning for Grafana with:
- Folder structure: [Infrastructure, Applications, Business, SLOs]
- Update interval: [N] seconds
- Disable UI editing for production dashboards
- Enable UI editing for development dashboards

Source: [Git repository/Local files/S3 bucket]
```

### Authentication Configuration

```
Configure Grafana authentication with [OAuth provider]:
- Provider: [Keycloak/Okta/Azure AD/Google/GitHub]
- Role mapping:
  - Admin group: [group name]
  - Editor group: [group name]
  - Default role: Viewer
- Enable auto user provisioning
- Sync team memberships

Provider details: [OIDC endpoints, client info]
```

### Alerting Configuration

```
Set up Grafana alerting for [application/infrastructure]:

Alert requirements:
1. [Alert 1: e.g., High CPU > 80% for 5 minutes]
2. [Alert 2: e.g., Error rate > 1% for 2 minutes]
3. [Alert 3: e.g., P99 latency > 500ms for 5 minutes]

Notification channels:
- Critical: [PagerDuty/Opsgenie]
- Warning: [Slack channel]
- Info: [Email distribution list]

Include:
- Alert rules in provisioning format
- Contact points configuration
- Notification policies with routing
- Mute timings for maintenance windows
```

---

## Dashboard Creation Prompts

### Application Dashboard

```
Create a Grafana dashboard for monitoring [application name]:

Metrics available:
- HTTP requests: http_requests_total{method, path, status}
- Latency: http_request_duration_seconds_bucket{method, path}
- Active connections: http_active_connections
- Custom: [list custom metrics]

Dashboard requirements:
- Overview row with key stats (RPS, error rate, P99 latency)
- Traffic analysis (requests by endpoint, status codes)
- Latency distribution (heatmap and percentiles)
- Resource usage (CPU, memory per pod)
- Variables: namespace, service, time range

Output format: [JSON/Grafonnet]
```

### Infrastructure Dashboard

```
Create a Grafana dashboard for Kubernetes cluster monitoring:

Data sources:
- Prometheus with kube-state-metrics
- Node exporter metrics

Panels needed:
1. Cluster overview (nodes, pods, deployments status)
2. Resource utilization (CPU, memory, disk)
3. Network traffic (ingress/egress)
4. Pod status and restarts
5. PersistentVolume usage
6. Top resource consumers

Variables: cluster, namespace, node
Alerts: Include inline alert definitions for critical metrics
```

### SLO Dashboard

```
Create an SLO dashboard for [service name]:

SLO definitions:
- Availability: [99.9%] measured by successful requests
- Latency: [95%] of requests under [200ms]
- Error budget: Show remaining budget over [30 days]

Include:
- Current SLO status (met/not met)
- Error budget burn rate
- Burn rate alerts (fast burn, slow burn)
- Historical SLO compliance
- Time to error budget exhaustion
```

### Grafonnet Dashboard

```
Generate a Grafonnet (Jsonnet) dashboard for [use case]:

Requirements:
- Use latest Grafonnet library syntax
- Include template variables for [variables]
- Organize panels in logical rows
- Set appropriate panel sizes and positions
- Include annotations for deployments

Metrics: [list PromQL queries needed]
```

---

## Migration Prompts

### Grafana Agent to Alloy Migration

```
Help migrate from Grafana Agent to Grafana Alloy:

Current setup:
- Agent mode: [Static/Flow/Operator]
- Configuration: [paste current config or describe]
- Deployment: [Docker/Kubernetes/systemd]
- Targets being scraped: [describe]
- Remote write destinations: [list]

Generate:
1. Equivalent Alloy configuration
2. Migration steps with zero downtime
3. Validation checklist
4. Rollback plan
```

### Dashboard JSON to Grafonnet

```
Convert this Grafana dashboard JSON to Grafonnet:

[Paste JSON or describe dashboard]

Requirements:
- Use latest Grafonnet library
- Parameterize data source
- Extract common patterns into local variables
- Add comments explaining complex queries
```

### Legacy Alert to Unified Alerting

```
Migrate legacy Grafana alerts to Unified Alerting:

Current alerts:
[Describe or paste legacy alert definitions]

Requirements:
- Maintain same alerting behavior
- Configure in provisioning format (YAML)
- Set up contact points for [notification channels]
- Define appropriate notification policies
```

---

## Troubleshooting Prompts

### Performance Issues

```
Diagnose Grafana performance issues:

Symptoms:
- [Describe symptoms: slow dashboards, high memory, etc.]

Environment:
- Grafana version: [version]
- Deployment: [Docker/Kubernetes/VM]
- Database: [SQLite/PostgreSQL/MySQL]
- Number of dashboards: [N]
- Concurrent users: [N]

Provide:
1. Diagnostic queries to run
2. Key metrics to check
3. Common causes and solutions
4. Configuration optimizations
```

### Data Source Connectivity

```
Troubleshoot Grafana data source connection issues:

Data source: [type and URL]
Error message: [paste error]
Network setup: [describe network topology]

Grafana deployment: [Docker/Kubernetes/VM]
Data source deployment: [same network/different network/cloud]

Help identify:
1. Root cause analysis steps
2. Network debugging commands
3. Configuration fixes
4. Proxy/firewall considerations
```

### Alerting Issues

```
Debug Grafana alerting problems:

Issue: [alerts not firing/too many alerts/notification failures]

Setup:
- Alerting version: [Legacy/Unified]
- Alert rule: [paste rule or describe]
- Expected behavior: [describe]
- Actual behavior: [describe]

Provide:
1. Diagnostic steps
2. Common misconfigurations
3. Query validation approach
4. Notification troubleshooting
```

---

## Optimization Prompts

### Query Optimization

```
Optimize this Grafana/PromQL query for better performance:

Query: [paste query]
Dashboard refresh: [interval]
Time range typically used: [range]
Data volume: [describe cardinality]

Suggest:
1. Query rewrites for efficiency
2. Recording rules if beneficial
3. Appropriate step/resolution settings
4. Caching recommendations
```

### Dashboard Optimization

```
Optimize this Grafana dashboard for performance:

[Describe dashboard or paste JSON]

Issues:
- Load time: [current load time]
- Number of panels: [N]
- Refresh interval: [interval]

Provide:
1. Panel consolidation suggestions
2. Query optimization recommendations
3. Caching configuration
4. Best practices for large dashboards
```

### Resource Optimization

```
Optimize Grafana resource usage:

Current resources:
- CPU: [usage]
- Memory: [usage]
- Storage: [usage]

Deployment: [describe]
User load: [concurrent users]
Dashboard count: [N]
Data source count: [N]

Recommend:
1. Resource limit adjustments
2. Configuration tuning
3. Database optimization
4. Caching strategies
```

---

## Security Prompts

### Security Hardening

```
Create a security hardening checklist for Grafana:

Deployment: [Docker/Kubernetes/VM]
Environment: [production/staging]
Compliance requirements: [SOC2/HIPAA/PCI/etc.]

Include:
1. Authentication hardening
2. Authorization (RBAC) configuration
3. Network security measures
4. Secrets management
5. Audit logging setup
6. TLS/SSL configuration
```

### RBAC Configuration

```
Design Grafana RBAC for this organization structure:

Teams:
- [Team 1]: Needs access to [dashboards/folders]
- [Team 2]: Needs access to [dashboards/folders]
- Platform team: Full admin access
- External viewers: Read-only specific dashboards

Requirements:
- Least privilege principle
- Data source permissions
- Dashboard folder permissions
- API access controls
```

---

## Integration Prompts

### CI/CD Integration

```
Set up Grafana dashboard CI/CD pipeline:

Requirements:
- Source: Dashboards in Git repository
- Validation: Schema validation before deploy
- Deployment: Automatic sync to Grafana
- Environments: [dev, staging, prod]

Tools available: [GitHub Actions/GitLab CI/Jenkins]

Generate:
1. Pipeline configuration
2. Dashboard validation script
3. Deployment strategy (with rollback)
4. Environment-specific variable handling
```

### Terraform Integration

```
Create Terraform configuration for Grafana:

Resources to manage:
- Data sources: [list]
- Folders: [list]
- Dashboards: [list or "from files"]
- Alert rules: [list]
- Users/teams: [describe]

Provider: grafana/grafana
State backend: [S3/GCS/Azure/local]

Include:
1. Provider configuration
2. Resource definitions
3. Variable definitions
4. Output values
```

---

## Prompt Templates

### General Template

```
[Task description]

Context:
- Grafana version: [version]
- Deployment type: [Docker/Kubernetes/VM]
- Environment: [dev/staging/prod]
- Existing setup: [describe]

Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

Constraints:
- [Constraint 1]
- [Constraint 2]

Expected output:
- [Format: YAML/JSON/HCL/etc.]
- [Include: comments/documentation]
```

### Debugging Template

```
Debug [issue type] in Grafana:

Symptoms:
- [Symptom 1]
- [Symptom 2]

Environment details:
- Grafana version: [version]
- Deployment: [type]
- Recent changes: [describe]

Error messages:
[Paste relevant errors]

What I've tried:
1. [Attempted solution 1]
2. [Attempted solution 2]

Help me:
1. Identify root cause
2. Provide step-by-step fix
3. Prevent recurrence
```
