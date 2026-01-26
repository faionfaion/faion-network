# Prometheus Monitoring Checklists

## Initial Setup Checklist

### Prometheus Installation

- [ ] Choose deployment method (Helm, Operator, Docker)
- [ ] Configure storage class and retention
- [ ] Set resource limits (CPU, memory)
- [ ] Configure external labels for federation
- [ ] Enable remote write for long-term storage
- [ ] Set up ServiceAccount and RBAC
- [ ] Configure network policies

### Alertmanager Setup

- [ ] Deploy Alertmanager (3 replicas for HA)
- [ ] Configure receivers (Slack, PagerDuty, email)
- [ ] Define routing rules by severity
- [ ] Set up inhibition rules
- [ ] Configure silences mechanism
- [ ] Test notification delivery
- [ ] Create alert templates

### Grafana Integration

- [ ] Deploy Grafana with persistence
- [ ] Add Prometheus data source
- [ ] Import baseline dashboards
- [ ] Configure authentication (SSO/LDAP)
- [ ] Set up dashboard provisioning
- [ ] Configure alerting integration
- [ ] Add Loki data source (if using)

## CI/CD Pipeline Monitoring Checklist

### Jenkins

- [ ] Install Prometheus Metrics Plugin
- [ ] Verify `/prometheus` endpoint accessible
- [ ] Create ServiceMonitor/scrape config
- [ ] Import Jenkins dashboard (ID: 9964)
- [ ] Set up alerts for build failures
- [ ] Monitor executor queue length
- [ ] Track build duration trends

### GitLab CI

- [ ] Deploy GitLab CI Pipelines Exporter
- [ ] Configure GitLab API token
- [ ] Select projects to monitor
- [ ] Create ServiceMonitor
- [ ] Import GitLab CI dashboard (ID: 10620)
- [ ] Set up pipeline failure alerts
- [ ] Monitor runner capacity

### GitHub Actions

- [ ] Set up Pushgateway
- [ ] Add metrics push to workflow files
- [ ] Track workflow duration
- [ ] Monitor success/failure rates
- [ ] Create custom dashboard
- [ ] Set up alerts for failures

### ArgoCD

- [ ] Enable metrics endpoint (port 8082)
- [ ] Create ServiceMonitor
- [ ] Import ArgoCD dashboard
- [ ] Monitor sync status
- [ ] Alert on failed syncs
- [ ] Track application health

## Application Instrumentation Checklist

### General

- [ ] Choose client library (Python, Node.js, Go, Java)
- [ ] Define metric naming convention
- [ ] Instrument HTTP endpoints (latency, count, errors)
- [ ] Add business metrics
- [ ] Expose `/metrics` endpoint
- [ ] Add health check endpoint
- [ ] Document all custom metrics

### Python (FastAPI/Django)

- [ ] Install `prometheus_client`
- [ ] Create metrics registry
- [ ] Add request duration histogram
- [ ] Add request counter with labels
- [ ] Add in-progress gauge
- [ ] Create `/metrics` endpoint
- [ ] Add middleware for automatic tracking

### Node.js (Express/Fastify)

- [ ] Install `prom-client`
- [ ] Enable default metrics
- [ ] Add custom counters/histograms
- [ ] Create metrics middleware
- [ ] Expose `/metrics` route
- [ ] Handle graceful shutdown

### Go

- [ ] Import `prometheus/client_golang`
- [ ] Register metrics
- [ ] Add HTTP handler for `/metrics`
- [ ] Use promhttp middleware
- [ ] Add build info metric

## PromQL Query Checklist

### Request Metrics

- [ ] Request rate: `sum(rate(http_requests_total[5m]))`
- [ ] Error rate: `sum(rate(http_requests_total{status=~"5.."}[5m]))`
- [ ] Error percentage: error_rate / total_rate * 100
- [ ] P50 latency: `histogram_quantile(0.50, ...)`
- [ ] P90 latency: `histogram_quantile(0.90, ...)`
- [ ] P99 latency: `histogram_quantile(0.99, ...)`

### Resource Metrics

- [ ] CPU usage: `rate(container_cpu_usage_seconds_total[5m])`
- [ ] Memory usage: `container_memory_working_set_bytes`
- [ ] Memory percentage: working_set / limit * 100
- [ ] Disk usage: `node_filesystem_avail_bytes`
- [ ] Network I/O: `rate(container_network_*_bytes_total[5m])`

### Kubernetes Metrics

- [ ] Pod restarts: `increase(kube_pod_container_status_restarts_total[1h])`
- [ ] Deployment replicas: `kube_deployment_status_replicas_*`
- [ ] Node status: `kube_node_status_condition`
- [ ] PVC usage: `kubelet_volume_stats_*`

## Alert Configuration Checklist

### Alert Rule Quality

- [ ] Use `for` clause (5-15m minimum)
- [ ] Include severity label
- [ ] Add team/service labels for routing
- [ ] Write descriptive summary
- [ ] Include detailed description with `{{ $value }}`
- [ ] Add runbook_url annotation
- [ ] Test in staging environment

### Common Alerts

- [ ] High error rate (>5% for 5m)
- [ ] High latency (P99 > threshold for 10m)
- [ ] Pod restarts (>3 in 1h)
- [ ] High memory usage (>85% for 15m)
- [ ] CPU throttling (>25% for 15m)
- [ ] Deployment unavailable
- [ ] PVC near capacity (>80%)

### Alertmanager Routing

- [ ] Route critical alerts to PagerDuty
- [ ] Route warnings to Slack
- [ ] Group alerts by alertname + namespace
- [ ] Set appropriate repeat intervals
- [ ] Configure inhibition for cascading alerts
- [ ] Test routing with test alerts

## Performance Optimization Checklist

### Query Performance

- [ ] Create recording rules for dashboard queries
- [ ] Avoid high cardinality labels
- [ ] Use label matchers to scope queries
- [ ] Limit time range in dashboards
- [ ] Use `rate()` over `irate()` for alerts
- [ ] Pre-aggregate with recording rules

### Storage Optimization

- [ ] Set appropriate retention (15-30 days typical)
- [ ] Configure retention size limit
- [ ] Use remote write for long-term
- [ ] Drop unnecessary metrics via relabeling
- [ ] Monitor Prometheus memory usage
- [ ] Use compaction settings appropriately

### Scraping Optimization

- [ ] Use appropriate scrape intervals
- [ ] Set scrape timeouts correctly
- [ ] Drop unused metrics via metric_relabel_configs
- [ ] Use sample limits per target
- [ ] Monitor scrape duration and failures

## Security Checklist

- [ ] Enable TLS for Prometheus endpoints
- [ ] Configure authentication (basic auth or OAuth)
- [ ] Use network policies to restrict access
- [ ] Secure Alertmanager webhook URLs
- [ ] Rotate API tokens regularly
- [ ] Audit access to metrics endpoints
- [ ] Mask sensitive label values

## Maintenance Checklist

### Regular Tasks

- [ ] Review and update alert thresholds
- [ ] Clean up unused recording rules
- [ ] Update dashboards for new services
- [ ] Review high cardinality metrics
- [ ] Check disk usage trends
- [ ] Verify backup procedures
- [ ] Test disaster recovery

### Monitoring Prometheus

- [ ] Prometheus up: `up{job="prometheus"}`
- [ ] Scrape failures: `prometheus_target_scrape_pool_sync_total`
- [ ] Rule evaluation: `prometheus_rule_evaluation_failures_total`
- [ ] TSDB health: `prometheus_tsdb_*`
- [ ] Memory usage: `process_resident_memory_bytes`
- [ ] Query latency: `prometheus_engine_query_duration_seconds`
